"""PostgreSQL + PostGIS storage for world metadata and POIs."""

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from geoalchemy2 import Geography


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""


class WorldRecord(Base):
    """Database record for a generated world."""

    __tablename__ = "worlds"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    hdf5_path = Column(Text, nullable=False)  # Path to HDF5 file
    parameters = Column(JSON, nullable=False)  # WorldParameters as JSON
    world_metadata = Column(JSON)  # Additional metadata (renamed to avoid SQLAlchemy conflict)
    generation_time_seconds = Column(Float)

    # Relationships
    pois = relationship("POI", back_populates="world", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<World(id={self.id}, name='{self.name}')>"


class POI(Base):
    """Point of Interest on a world."""

    __tablename__ = "pois"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    world_id = Column(PG_UUID(as_uuid=True), ForeignKey("worlds.id"), nullable=False)
    poi_type = Column(String(50), nullable=False, index=True)  # 'mountain', 'settlement', etc.
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)  # PostGIS geography
    mesh_point_index = Column(Integer, nullable=False)  # Index in mesh.points
    name = Column(String(255), nullable=False)
    description = Column(Text)
    properties = Column(JSON)  # Flexible attributes (elevation, temperature, etc.)
    importance = Column(Float, default=0.5, index=True)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    world = relationship("WorldRecord", back_populates="pois")

    def __repr__(self) -> str:
        return f"<POI(id={self.id}, type='{self.poi_type}', name='{self.name}')>"


class MetadataStore:
    """Manages storage and retrieval of world metadata and POIs using PostgreSQL."""

    def __init__(self, database_url: str = "postgresql://localhost/lathe"):
        """Initialize the metadata store.

        Args:
            database_url: PostgreSQL connection URL
                         Format: postgresql://user:password@host:port/database
        """
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        """Create database tables if they don't exist."""
        Base.metadata.create_all(self.engine)

    def drop_tables(self) -> None:
        """Drop all tables (use with caution!)."""
        Base.metadata.drop_all(self.engine)

    def save_world_metadata(
        self,
        world_id: UUID,
        name: str,
        hdf5_path: str,
        parameters: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> WorldRecord:
        """Save world metadata to database.

        Args:
            world_id: World UUID
            name: World name
            hdf5_path: Path to HDF5 file
            parameters: World generation parameters
            metadata: Additional metadata

        Returns:
            Created WorldRecord
        """
        session = self.Session()
        try:
            world_record = WorldRecord(
                id=world_id,
                name=name,
                hdf5_path=hdf5_path,
                parameters=parameters,
                world_metadata=metadata or {},
                generation_time_seconds=metadata.get("generation_time_seconds", 0.0) if metadata else 0.0,
            )

            session.add(world_record)
            session.commit()
            session.refresh(world_record)

            return world_record

        finally:
            session.close()

    def get_world_metadata(self, world_id: UUID) -> WorldRecord | None:
        """Get world metadata from database.

        Args:
            world_id: World UUID

        Returns:
            WorldRecord or None if not found
        """
        session = self.Session()
        try:
            return session.query(WorldRecord).filter(WorldRecord.id == world_id).first()
        finally:
            session.close()

    def list_worlds(self, limit: int = 100, offset: int = 0) -> list[WorldRecord]:
        """List all worlds in database.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of WorldRecords
        """
        session = self.Session()
        try:
            return (
                session.query(WorldRecord)
                .order_by(WorldRecord.created_at.desc())
                .limit(limit)
                .offset(offset)
                .all()
            )
        finally:
            session.close()

    def delete_world(self, world_id: UUID) -> bool:
        """Delete world metadata and all associated POIs.

        Args:
            world_id: World UUID

        Returns:
            True if deleted, False if not found
        """
        session = self.Session()
        try:
            world = session.query(WorldRecord).filter(WorldRecord.id == world_id).first()
            if world:
                session.delete(world)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def add_poi(
        self,
        world_id: UUID,
        poi_id: UUID,
        poi_type: str,
        location: tuple[float, float, float],  # (x, y, z) in 3D space
        mesh_point_index: int,
        name: str,
        description: str = "",
        properties: dict[str, Any] | None = None,
        importance: float = 0.5,
    ) -> POI:
        """Add a POI to the database.

        Args:
            world_id: World UUID
            poi_id: POI UUID
            poi_type: Type of POI ('mountain', 'settlement', etc.)
            location: 3D coordinates (x, y, z)
            mesh_point_index: Index in mesh.points array
            name: POI name
            description: POI description
            properties: Additional properties
            importance: Importance score (0.0 to 1.0)

        Returns:
            Created POI
        """
        session = self.Session()
        try:
            # Convert 3D coordinates to lat/lon for PostGIS
            # For now, we'll use a simple projection
            # In production, you'd want proper 3D coordinate conversion
            lat, lon = self._xyz_to_latlon(location)

            # Create WKT point for PostGIS
            point_wkt = f"POINT({lon} {lat})"

            poi = POI(
                id=poi_id,
                world_id=world_id,
                poi_type=poi_type,
                location=point_wkt,
                mesh_point_index=mesh_point_index,
                name=name,
                description=description,
                properties=properties or {},
                importance=importance,
            )

            session.add(poi)
            session.commit()
            session.refresh(poi)

            return poi

        finally:
            session.close()

    def get_pois(
        self,
        world_id: UUID,
        poi_type: str | None = None,
        min_importance: float | None = None,
        limit: int = 1000,
    ) -> list[POI]:
        """Get POIs for a world.

        Args:
            world_id: World UUID
            poi_type: Filter by POI type (None for all)
            min_importance: Minimum importance score
            limit: Maximum number of results

        Returns:
            List of POIs
        """
        session = self.Session()
        try:
            query = session.query(POI).filter(POI.world_id == world_id)

            if poi_type:
                query = query.filter(POI.poi_type == poi_type)

            if min_importance is not None:
                query = query.filter(POI.importance >= min_importance)

            return query.order_by(POI.importance.desc()).limit(limit).all()

        finally:
            session.close()

    def get_nearby_pois(
        self,
        world_id: UUID,
        location: tuple[float, float, float],
        radius_km: float = 100.0,
        limit: int = 100,
    ) -> list[POI]:
        """Get POIs near a location using PostGIS spatial query.

        Args:
            world_id: World UUID
            location: Center point (x, y, z)
            radius_km: Search radius in kilometers
            limit: Maximum number of results

        Returns:
            List of nearby POIs
        """
        session = self.Session()
        try:
            lat, lon = self._xyz_to_latlon(location)
            point_wkt = f"POINT({lon} {lat})"

            # PostGIS distance query
            query = (
                session.query(POI)
                .filter(POI.world_id == world_id)
                .filter(
                    # ST_DWithin uses meters for geography type
                    POI.location.ST_DWithin(point_wkt, radius_km * 1000)
                )
                .order_by(POI.location.ST_Distance(point_wkt))
                .limit(limit)
            )

            return query.all()

        finally:
            session.close()

    def delete_poi(self, poi_id: UUID) -> bool:
        """Delete a POI.

        Args:
            poi_id: POI UUID

        Returns:
            True if deleted, False if not found
        """
        session = self.Session()
        try:
            poi = session.query(POI).filter(POI.id == poi_id).first()
            if poi:
                session.delete(poi)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def _xyz_to_latlon(self, xyz: tuple[float, float, float]) -> tuple[float, float]:
        """Convert 3D Cartesian coordinates to latitude/longitude.

        This is a simplified conversion. In production, you'd want to use
        proper spherical coordinate conversion.

        Args:
            xyz: (x, y, z) coordinates

        Returns:
            (latitude, longitude) in degrees
        """
        import math

        x, y, z = xyz

        # Convert to spherical coordinates
        r = math.sqrt(x**2 + y**2 + z**2)
        lat = math.degrees(math.asin(z / r)) if r > 0 else 0.0
        lon = math.degrees(math.atan2(y, x))

        return lat, lon
