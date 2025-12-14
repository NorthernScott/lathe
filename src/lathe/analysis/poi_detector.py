"""Point of Interest (POI) detection analysis plugin."""

import asyncio
import random
from typing import Any, Callable
from uuid import uuid4

import numpy as np
from scipy.signal import find_peaks

from lathe.models.world import World
from lathe.plugins.base import AnalysisPlugin, PluginMetadata, PluginResult


class POIData:
    """Represents a detected Point of Interest."""

    def __init__(
        self,
        poi_type: str,
        location: tuple[float, float, float],
        mesh_index: int,
        name: str,
        properties: dict[str, Any],
        importance: float,
    ):
        self.id = uuid4()
        self.poi_type = poi_type
        self.location = location
        self.mesh_index = mesh_index
        self.name = name
        self.properties = properties
        self.importance = importance

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "type": self.poi_type,
            "location": self.location,
            "mesh_index": self.mesh_index,
            "name": self.name,
            "properties": self.properties,
            "importance": self.importance,
        }


class POIDetectorPlugin(AnalysisPlugin):
    """Detects points of interest on a generated world."""

    # Name lists for generating POI names
    MOUNTAIN_PREFIXES = ["Mount", "Peak", "Summit", "Ridge", "Crest"]
    MOUNTAIN_SUFFIXES = ["Heights", "Massif", "Range", "Spire", "Crown"]

    SETTLEMENT_PREFIXES = ["New", "Old", "East", "West", "North", "South"]
    SETTLEMENT_TYPES = ["Haven", "Port", "Bay", "Valley", "Dale", "Crossing", "Landing"]

    VIEWPOINT_NAMES = ["Vista", "Overlook", "Prospect", "Outlook", "Viewpoint", "Lookout"]

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="poi_detector",
            version="1.0.0",
            dependencies=[],
            description="Detects interesting points on the world surface",
            author="Lathe",
        )

    def get_required_data_layers(self) -> list[str]:
        return ["elevation", "landforms"]

    async def analyze(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> PluginResult:
        """Detect POIs on the world.

        Args:
            world: World to analyze
            params: Analysis parameters:
                - detect_mountains (bool): Detect mountain peaks (default: True)
                - detect_valleys (bool): Detect valleys (default: True)
                - detect_coastlines (bool): Detect notable coastlines (default: True)
                - detect_settlements (bool): Detect habitable areas (default: True)
                - detect_viewpoints (bool): Detect scenic viewpoints (default: True)
                - min_importance (float): Minimum importance to include (default: 0.5)
            progress_callback: Optional progress callback

        Returns:
            PluginResult with POI data
        """
        if progress_callback:
            progress_callback(0.0, "Starting POI detection")

        # Run detection in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._detect_pois_sync,
            world,
            params,
            progress_callback,
        )

        if progress_callback:
            progress_callback(1.0, "POI detection complete")

        return result

    def _detect_pois_sync(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None,
    ) -> PluginResult:
        """Synchronous POI detection (runs in thread pool)."""
        pois: list[POIData] = []
        min_importance = params.get("min_importance", 0.5)

        detectors = [
            ("mountains", params.get("detect_mountains", True), self._detect_mountains),
            ("valleys", params.get("detect_valleys", True), self._detect_valleys),
            ("coastlines", params.get("detect_coastlines", True), self._detect_coastlines),
            ("settlements", params.get("detect_settlements", True), self._detect_settlements),
            ("viewpoints", params.get("detect_viewpoints", True), self._detect_viewpoints),
        ]

        active_detectors = [(name, func) for name, enabled, func in detectors if enabled]
        total_detectors = len(active_detectors)

        for idx, (name, detector_func) in enumerate(active_detectors):
            if progress_callback:
                progress = idx / total_detectors
                progress_callback(progress, f"Detecting {name}")

            detected = detector_func(world)
            pois.extend(detected)

        # Filter by importance
        pois = [poi for poi in pois if poi.importance >= min_importance]

        if progress_callback:
            progress_callback(0.95, f"Found {len(pois)} POIs")

        return PluginResult(
            success=True,
            message=f"Detected {len(pois)} points of interest",
            data={"pois": [poi.to_dict() for poi in pois], "count": len(pois)},
        )

    def _detect_mountains(self, world: World) -> list[POIData]:
        """Detect mountain peaks."""
        elevations = world.get_data_layer("elevation")
        if elevations is None:
            return []

        pois = []

        # Find local maxima
        peaks, properties = find_peaks(
            elevations,
            prominence=1000,  # At least 1000m prominence
            distance=20,  # At least 20 points apart
        )

        for idx in peaks:
            elevation = elevations[idx]

            # Only include high mountains
            if elevation > 2000:  # > 2000m
                importance = min(elevation / 9000, 1.0)  # Normalize to 0-1

                pois.append(
                    POIData(
                        poi_type="mountain",
                        location=tuple(world.mesh.points[idx]),
                        mesh_index=int(idx),
                        name=self._generate_mountain_name(),
                        properties={
                            "elevation": float(elevation),
                            "prominence": float(properties["prominences"][list(peaks).index(idx)]),
                        },
                        importance=importance,
                    )
                )

        return pois

    def _detect_valleys(self, world: World) -> list[POIData]:
        """Detect deep valleys."""
        elevations = world.get_data_layer("elevation")
        if elevations is None:
            return []

        pois = []

        # Find local minima (invert elevations)
        valleys, properties = find_peaks(
            -elevations,
            prominence=500,  # At least 500m depth
            distance=20,
        )

        for idx in valleys:
            elevation = elevations[idx]

            # Only include significant valleys (but above sea level)
            if 0 < elevation < 500:
                importance = 1.0 - (elevation / 500)

                pois.append(
                    POIData(
                        poi_type="valley",
                        location=tuple(world.mesh.points[idx]),
                        mesh_index=int(idx),
                        name=f"{random.choice(['Deep', 'Great', 'Hidden'])} Valley",
                        properties={
                            "elevation": float(elevation),
                            "depth": float(properties["prominences"][list(valleys).index(idx)]),
                        },
                        importance=importance,
                    )
                )

        return pois

    def _detect_coastlines(self, world: World) -> list[POIData]:
        """Detect notable coastline features."""
        elevations = world.get_data_layer("elevation")
        landforms = world.get_data_layer("landforms")

        if elevations is None or landforms is None:
            return []

        pois = []

        # Find points near sea level with high elevation variance nearby
        for idx in range(0, len(elevations), 100):  # Sample every 100th point
            if abs(elevations[idx]) < 100:  # Near sea level
                # Check neighbors
                neighbors = world.get_neighbors(idx, radius=5000)  # 5km
                if len(neighbors) > 5:
                    land_count = np.sum(landforms[neighbors])
                    ocean_count = len(neighbors) - land_count

                    # Interesting coastline if mix of land and ocean
                    if land_count > 0 and ocean_count > 0:
                        ratio = min(land_count, ocean_count) / max(land_count, ocean_count)
                        if ratio > 0.3:  # Significant mix
                            pois.append(
                                POIData(
                                    poi_type="coastline",
                                    location=tuple(world.mesh.points[idx]),
                                    mesh_index=int(idx),
                                    name=f"{random.choice(['Cape', 'Bay', 'Cove', 'Peninsula'])}",
                                    properties={
                                        "elevation": float(elevations[idx]),
                                        "land_ocean_ratio": float(ratio),
                                    },
                                    importance=ratio,
                                )
                            )

        return pois

    def _detect_settlements(self, world: World) -> list[POIData]:
        """Detect potential settlement locations."""
        elevations = world.get_data_layer("elevation")
        landforms = world.get_data_layer("landforms")

        if elevations is None or landforms is None:
            return []

        pois = []

        # Criteria for good settlement locations:
        # - Moderate elevation (not too high, not too low)
        # - On land
        # - Relatively flat area nearby

        habitable_mask = (
            (elevations > 50) &  # Above sea level with margin
            (elevations < 1500) &  # Not too high
            (landforms > 0.5)  # On land
        )

        habitable_indices = np.where(habitable_mask)[0]

        # Sample every Nth habitable point to avoid too many settlements
        sample_step = max(len(habitable_indices) // 50, 1)

        for idx in habitable_indices[::sample_step]:
            # Calculate habitability score
            neighbors = world.get_neighbors(idx, radius=10000)  # 10km
            if len(neighbors) > 10:
                elevation_variance = np.var(elevations[neighbors])

                # Prefer flatter areas
                flatness = 1.0 / (1.0 + elevation_variance / 10000)

                # Prefer moderate elevations
                elevation_score = 1.0 - abs(elevations[idx] - 500) / 1000

                habitability = (flatness + elevation_score) / 2

                if habitability > 0.6:
                    pois.append(
                        POIData(
                            poi_type="settlement",
                            location=tuple(world.mesh.points[idx]),
                            mesh_index=int(idx),
                            name=self._generate_settlement_name(),
                            properties={
                                "elevation": float(elevations[idx]),
                                "habitability": float(habitability),
                                "flatness": float(flatness),
                            },
                            importance=habitability,
                        )
                    )

        return pois

    def _detect_viewpoints(self, world: World) -> list[POIData]:
        """Detect scenic viewpoints."""
        elevations = world.get_data_layer("elevation")
        if elevations is None:
            return []

        pois = []

        # Sample points
        for idx in range(0, len(elevations), 200):  # Every 200th point
            if elevations[idx] > 500:  # Must be reasonably high
                neighbors = world.get_neighbors(idx, radius=15000)  # 15km
                if len(neighbors) > 10:
                    height_advantage = elevations[idx] - np.mean(elevations[neighbors])
                    elevation_variance = np.var(elevations[neighbors])

                    # Good viewpoint: high relative to surroundings with varied terrain
                    if height_advantage > 300 and elevation_variance > 50000:
                        scenic_score = min(
                            (height_advantage / 1000) * (elevation_variance / 200000),
                            1.0,
                        )

                        if scenic_score > 0.5:
                            pois.append(
                                POIData(
                                    poi_type="viewpoint",
                                    location=tuple(world.mesh.points[idx]),
                                    mesh_index=int(idx),
                                    name=f"{random.choice(self.VIEWPOINT_NAMES)}",
                                    properties={
                                        "elevation": float(elevations[idx]),
                                        "height_advantage": float(height_advantage),
                                        "scenic_score": float(scenic_score),
                                    },
                                    importance=scenic_score,
                                )
                            )

        return pois

    def _generate_mountain_name(self) -> str:
        """Generate a random mountain name."""
        if random.random() < 0.5:
            return f"{random.choice(self.MOUNTAIN_PREFIXES)} {random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'])}"
        else:
            return f"The {random.choice(self.MOUNTAIN_SUFFIXES)}"

    def _generate_settlement_name(self) -> str:
        """Generate a random settlement name."""
        if random.random() < 0.3:
            return f"{random.choice(self.SETTLEMENT_PREFIXES)} {random.choice(self.SETTLEMENT_TYPES)}"
        else:
            return f"{random.choice(self.SETTLEMENT_TYPES)}"
