"""FastAPI server for world generation and management."""

import asyncio
from typing import Any
from uuid import UUID

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from lathe.analysis.poi_detector import POIDetectorPlugin
from lathe.core.engine import WorldGenerationEngine
from lathe.core.events import Event, EventType, get_global_emitter
from lathe.models.world import WorldParameters
from lathe.plugins.terrain.generator import TerrainGeneratorPlugin
from lathe.plugins.tectonics.simulator import TectonicsSimulatorPlugin
from lathe.storage.mesh_store import MeshStore
from lathe.storage.metadata_store import MetadataStore

# Pydantic models for API


class WorldGenerationRequest(BaseModel):
    """Request to generate a new world."""

    name: str = Field(default="", description="World name (auto-generated if empty)")
    radius: int = Field(default=6378100, description="World radius in meters")
    recursion: int = Field(default=6, ge=1, le=10, description="Mesh detail level")
    seed: int = Field(default=0, description="Random seed (0 for random)")
    ocean_percent: float = Field(default=0.55, ge=0.0, le=1.0)
    zmax: int = Field(default=9567, description="Maximum elevation in meters")
    zmin: int = Field(default=-9567, description="Minimum elevation in meters")
    pipeline: list[str] = Field(default=["terrain", "tectonics"], description="Generation pipeline")
    terrain_params: dict[str, Any] = Field(default_factory=dict)
    tectonics_params: dict[str, Any] = Field(default_factory=dict)


class WorldResponse(BaseModel):
    """Response with world information."""

    world_id: str
    name: str
    status: str
    progress: float = 0.0
    num_points: int | None = None
    data_layers: list[str] = []
    metadata: dict[str, Any] = {}


class POIAnalysisRequest(BaseModel):
    """Request to analyze POIs on a world."""

    detect_mountains: bool = True
    detect_valleys: bool = True
    detect_coastlines: bool = True
    detect_settlements: bool = True
    detect_viewpoints: bool = True
    min_importance: float = Field(default=0.5, ge=0.0, le=1.0)


class POIResponse(BaseModel):
    """Response with POI information."""

    id: str
    type: str
    name: str
    location: tuple[float, float, float]
    mesh_index: int
    properties: dict[str, Any]
    importance: float


# Create FastAPI app
app = FastAPI(
    title="Lathe World Generation API",
    description="API for generating and managing procedural worlds",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
engine = WorldGenerationEngine(max_workers=4)
mesh_store = MeshStore(storage_dir="./data/worlds")
metadata_store = MetadataStore(database_url="postgresql://localhost/lathe")

# Register plugins
engine.register_plugin(TerrainGeneratorPlugin())
engine.register_plugin(TectonicsSimulatorPlugin())
engine.register_plugin(POIDetectorPlugin())

# Track active generation tasks
active_tasks: dict[UUID, dict[str, Any]] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        metadata_store.create_tables()
    except Exception as e:
        print(f"Database initialization warning: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Lathe World Generation API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/worlds/generate",
            "list": "/worlds",
            "get": "/worlds/{world_id}",
            "analyze": "/worlds/{world_id}/analyze",
        },
    }


@app.post("/worlds/generate", response_model=WorldResponse)
async def generate_world(request: WorldGenerationRequest):
    """Start world generation.

    This creates a background task and returns immediately.
    Use WebSocket or polling to track progress.
    """
    # Create world parameters
    params = WorldParameters(
        name=request.name,
        radius=request.radius,
        recursion=request.recursion,
        seed=request.seed,
        ocean_percent=request.ocean_percent,
        zmax=request.zmax,
        zmin=request.zmin,
    )

    # Prepare plugin parameters
    plugin_params = {
        "terrain": request.terrain_params,
        "tectonics": request.tectonics_params,
    }

    # Create generation task
    async def generation_task(params, pipeline, plugin_params):
        try:
            # Generate world
            world = await engine.generate_world(
                params=params,
                pipeline=pipeline,
                plugin_params=plugin_params,
            )

            # Save to HDF5
            hdf5_path = mesh_store.save_world(world)

            # Save metadata to PostgreSQL
            metadata_store.save_world_metadata(
                world_id=world.id,
                name=world.params.name,
                hdf5_path=str(hdf5_path),
                parameters=params.__dict__,
                metadata=world.metadata,
            )

            # Update task status
            active_tasks[world.id]["status"] = "completed"
            active_tasks[world.id]["world"] = world

        except Exception as e:
            active_tasks[world.id]["status"] = "failed"
            active_tasks[world.id]["error"] = str(e)

    # Create world ID
    world_id = UUID(int=0)  # Will be replaced by actual world ID
    task = asyncio.create_task(generation_task(params, request.pipeline, plugin_params))

    # This is a hack - we need to get the world ID from the task
    # In production, you'd generate the UUID first and pass it to World
    # For now, we'll use a placeholder

    return WorldResponse(
        world_id="pending",
        name=request.name,
        status="generating",
        progress=0.0,
    )


@app.get("/worlds", response_model=list[WorldResponse])
async def list_worlds(limit: int = 100, offset: int = 0):
    """List all generated worlds."""
    worlds = mesh_store.list_worlds()

    return [
        WorldResponse(
            world_id=w["world_id"],
            name=w["name"],
            status="completed",
            progress=1.0,
            num_points=w["num_points"],
            data_layers=w["data_layers"],
        )
        for w in worlds
    ]


@app.get("/worlds/{world_id}", response_model=WorldResponse)
async def get_world(world_id: UUID):
    """Get information about a specific world."""
    info = mesh_store.get_world_info(world_id)

    if not info:
        raise HTTPException(status_code=404, detail="World not found")

    return WorldResponse(
        world_id=info["world_id"],
        name=info["name"],
        status="completed",
        progress=1.0,
        num_points=info["num_points"],
        data_layers=info["data_layers"],
        metadata=info["metadata"],
    )


@app.delete("/worlds/{world_id}")
async def delete_world(world_id: UUID):
    """Delete a world and all associated data."""
    # Delete from mesh store
    mesh_deleted = mesh_store.delete_world(world_id)

    # Delete from metadata store
    metadata_deleted = metadata_store.delete_world(world_id)

    if not mesh_deleted and not metadata_deleted:
        raise HTTPException(status_code=404, detail="World not found")

    return {"status": "deleted", "world_id": str(world_id)}


@app.post("/worlds/{world_id}/analyze", response_model=dict[str, Any])
async def analyze_world(world_id: UUID, request: POIAnalysisRequest):
    """Run POI analysis on a world."""
    # Load world
    try:
        world = mesh_store.load_world(world_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="World not found")

    # Run analysis
    results = await engine.analyze_world(
        world=world,
        analyzers=["poi_detector"],
        analyzer_params={
            "poi_detector": {
                "detect_mountains": request.detect_mountains,
                "detect_valleys": request.detect_valleys,
                "detect_coastlines": request.detect_coastlines,
                "detect_settlements": request.detect_settlements,
                "detect_viewpoints": request.detect_viewpoints,
                "min_importance": request.min_importance,
            }
        },
    )

    # Save POIs to database
    if "poi_detector" in results:
        poi_data = results["poi_detector"].data
        if "pois" in poi_data:
            for poi in poi_data["pois"]:
                metadata_store.add_poi(
                    world_id=world_id,
                    poi_id=UUID(poi["id"]),
                    poi_type=poi["type"],
                    location=tuple(poi["location"]),
                    mesh_point_index=poi["mesh_index"],
                    name=poi["name"],
                    properties=poi["properties"],
                    importance=poi["importance"],
                )

    return results["poi_detector"].data if "poi_detector" in results else {}


@app.get("/worlds/{world_id}/pois", response_model=list[POIResponse])
async def get_pois(
    world_id: UUID,
    poi_type: str | None = None,
    min_importance: float = 0.0,
    limit: int = 1000,
):
    """Get POIs for a world."""
    pois = metadata_store.get_pois(
        world_id=world_id,
        poi_type=poi_type,
        min_importance=min_importance,
        limit=limit,
    )

    return [
        POIResponse(
            id=str(poi.id),
            type=poi.poi_type,
            name=poi.name,
            location=(0.0, 0.0, 0.0),  # Would need to convert from PostGIS
            mesh_index=poi.mesh_point_index,
            properties=poi.properties,
            importance=poi.importance,
        )
        for poi in pois
    ]


@app.get("/worlds/{world_id}/mesh/{layer}")
async def get_mesh_layer(world_id: UUID, layer: str):
    """Get a specific mesh data layer."""
    data = mesh_store.get_data_layer(world_id, layer)

    if data is None:
        raise HTTPException(status_code=404, detail=f"Layer '{layer}' not found")

    # Convert to list for JSON serialization
    return {"layer": layer, "data": data.tolist(), "length": len(data)}


@app.websocket("/ws/worlds/{world_id}")
async def websocket_progress(websocket: WebSocket, world_id: str):
    """WebSocket endpoint for real-time progress updates."""
    await websocket.accept()

    # Subscribe to events
    emitter = get_global_emitter()
    progress_data = {"progress": 0.0, "message": "Starting..."}

    def event_handler(event: Event):
        if event.type == EventType.PLUGIN_PROGRESS:
            progress_data["progress"] = event.data.get("progress", 0.0)
            progress_data["message"] = event.message

    emitter.subscribe(EventType.PLUGIN_PROGRESS, event_handler)

    try:
        while True:
            # Send progress updates
            await websocket.send_json(progress_data)
            await asyncio.sleep(0.5)

            # Check if generation is complete
            if progress_data["progress"] >= 1.0:
                break

    except WebSocketDisconnect:
        pass
    finally:
        emitter.unsubscribe(EventType.PLUGIN_PROGRESS, event_handler)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
