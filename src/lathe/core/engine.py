"""Core world generation engine with plugin orchestration."""

import asyncio
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Callable
import os

import networkx as nx

from lathe.core.events import EventEmitter, EventType, get_global_emitter
from lathe.models.world import World, WorldParameters
from lathe.plugins.base import AnalysisPlugin, PluginResult, SimulationPlugin


class PipelineExecutionError(Exception):
    """Raised when pipeline execution fails."""


class WorldGenerationEngine:
    """Core engine for orchestrating world generation.

    The engine:
    - Manages plugin registration
    - Resolves plugin dependencies
    - Executes plugins in correct order
    - Handles parallelization where possible
    - Reports progress via events
    """

    def __init__(
        self,
        worker_count: int | None = None,
        event_emitter: EventEmitter | None = None,
    ):
        """Initialize the engine.

        Args:
            max_workers: Maximum number of threads for parallel execution.
                If None, defaults to half the CPU count (minimum 1).
            event_emitter: Event emitter for progress reporting (uses global if None)
        """
        self.simulation_plugins: dict[str, SimulationPlugin] = {}
        self.analysis_plugins: dict[str, AnalysisPlugin] = {}

        # Calculate default worker count based on available threads
        self.workers = (
            worker_count
            if worker_count is not None
            else max(1, (os.cpu_count() or 1) // 2)
        )

        self.thread_pool = ThreadPoolExecutor(max_workers=self.workers)
        self.emitter = (
            event_emitter if event_emitter is not None else get_global_emitter()
        )

    def register_plugin(self, plugin: SimulationPlugin | AnalysisPlugin) -> None:
        """Register a plugin.

        Args:
            plugin: Plugin to register
        """
        if isinstance(plugin, SimulationPlugin):
            self.simulation_plugins[plugin.metadata.name] = plugin
        elif isinstance(plugin, AnalysisPlugin):
            self.analysis_plugins[plugin.metadata.name] = plugin
        else:
            msg = f"Unknown plugin type: {type(plugin)}"
            raise TypeError(msg)

    def get_plugin(self, name: str) -> SimulationPlugin | AnalysisPlugin | None:
        """Get a registered plugin by name.

        Args:
            name: Plugin name

        Returns:
            Plugin instance or None if not found
        """
        return self.simulation_plugins.get(name) or self.analysis_plugins.get(name)

    def list_plugins(self) -> list[str]:
        """List all registered plugin names."""
        return list(self.simulation_plugins.keys()) + list(self.analysis_plugins.keys())

    async def generate_world(
        self,
        params: WorldParameters | None = None,
        pipeline: list[str] | None = None,
        plugin_params: dict[str, dict[str, Any]] | None = None,
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> World:
        """Generate a complete world by running a plugin pipeline.

        Args:
            params: World generation parameters
            pipeline: Ordered list of plugin names to execute
            plugin_params: Parameters for each plugin {plugin_name: {param: value}}
            progress_callback: Optional callback for progress updates

        Returns:
            Generated World object

        Raises:
            PipelineExecutionError: If pipeline execution fails
        """
        # Create world
        world = World(params or WorldParameters())

        # Use default pipeline if none provided
        if pipeline is None:
            pipeline = ["terrain", "tectonics"]

        plugin_params = plugin_params or {}

        # Emit start event
        self.emitter.emit(
            EventType.GENERATION_STARTED,
            f"Starting world generation: {world.params.name or world.id}",
            world_id=str(world.id),
            pipeline=pipeline,
        )

        start_time = datetime.now(timezone.utc)

        try:
            # Build dependency graph
            graph = self._build_dependency_graph(pipeline)

            # Validate all dependencies are satisfied
            self._validate_dependencies(graph, pipeline)

            # Get execution plan (handles parallelization)
            execution_plan = self._plan_execution(graph, pipeline)

            # Execute plan
            total_steps = len(execution_plan)
            for step_idx, step in enumerate(execution_plan):
                overall_progress = step_idx / total_steps

                if progress_callback:
                    progress_callback(
                        overall_progress, f"Step {step_idx + 1}/{total_steps}"
                    )

                if isinstance(step, list):
                    # Parallel execution of independent plugins
                    await self._execute_parallel(world, step, plugin_params)
                else:
                    # Sequential execution
                    await self._execute_plugin(world, step, plugin_params.get(step, {}))

            # Mark generation as complete
            world.metadata["generation_complete"] = True
            world.metadata["pipeline_steps"] = pipeline
            world.metadata["created_at"] = start_time.isoformat()
            world.metadata["generation_time_seconds"] = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds()

            if progress_callback:
                progress_callback(1.0, "Generation complete")

            self.emitter.emit(
                EventType.GENERATION_COMPLETED,
                f"World generation complete: {world.params.name or world.id}",
                world_id=str(world.id),
                generation_time=world.metadata["generation_time_seconds"],
            )

            return world

        except Exception as e:
            self.emitter.emit(
                EventType.GENERATION_FAILED,
                f"World generation failed: {e}",
                world_id=str(world.id),
                error=str(e),
            )
            raise PipelineExecutionError(f"Pipeline execution failed: {e}") from e

    async def analyze_world(
        self,
        world: World,
        analyzers: list[str],
        analyzer_params: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Run analysis plugins on a world.

        Args:
            world: World to analyze
            analyzers: List of analyzer plugin names
            analyzer_params: Parameters for each analyzer

        Returns:
            Dictionary of analysis results {analyzer_name: result}
        """
        analyzer_params = analyzer_params or {}
        results = {}

        self.emitter.emit(
            EventType.ANALYSIS_STARTED,
            f"Starting analysis with {len(analyzers)} analyzers",
            world_id=str(world.id),
            analyzers=analyzers,
        )

        for analyzer_name in analyzers:
            analyzer = self.analysis_plugins.get(analyzer_name)
            if not analyzer:
                self.emitter.emit(
                    EventType.WARNING,
                    f"Analyzer '{analyzer_name}' not found, skipping",
                )
                continue

            # Validate parameters
            params = analyzer_params.get(analyzer_name, {})
            valid, error_msg = analyzer.validate_params(params)
            if not valid:
                self.emitter.emit(
                    EventType.ERROR,
                    f"Invalid parameters for {analyzer_name}: {error_msg}",
                )
                continue

            # Execute analyzer
            result = await analyzer.analyze(
                world,
                params,
                self._make_progress_callback(analyzer_name),
            )

            results[analyzer_name] = result

        self.emitter.emit(
            EventType.ANALYSIS_COMPLETED,
            f"Analysis complete with {len(results)} results",
            world_id=str(world.id),
        )

        return results

    async def _execute_plugin(
        self,
        world: World,
        plugin_name: str,
        params: dict[str, Any],
    ) -> PluginResult:
        """Execute a single plugin.

        Args:
            world: World to modify
            plugin_name: Name of plugin to execute
            params: Plugin parameters

        Returns:
            PluginResult

        Raises:
            PipelineExecutionError: If plugin execution fails
        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            msg = f"Plugin '{plugin_name}' not found"
            raise PipelineExecutionError(msg)

        # Validate parameters
        valid, error_msg = plugin.validate_params(params)
        if not valid:
            msg = f"Invalid parameters for {plugin_name}: {error_msg}"
            raise PipelineExecutionError(msg)

        # Check required data layers
        required = plugin.get_required_data_layers()
        missing = [layer for layer in required if not world.has_data_layer(layer)]
        if missing:
            msg = f"Plugin {plugin_name} requires missing data layers: {missing}"
            raise PipelineExecutionError(msg)

        # Emit start event
        self.emitter.emit(
            EventType.PLUGIN_STARTED,
            f"Starting plugin: {plugin_name}",
            plugin=plugin_name,
            world_id=str(world.id),
        )

        # Execute plugin
        try:
            result = await plugin.execute(
                world,
                params,
                self._make_progress_callback(plugin_name),
            )

            if not result.success:
                raise PipelineExecutionError(
                    f"Plugin {plugin_name} failed: {result.message}"
                )

            self.emitter.emit(
                EventType.PLUGIN_COMPLETED,
                f"Plugin complete: {plugin_name} - {result.message}",
                plugin=plugin_name,
                world_id=str(world.id),
            )

            return result

        except Exception as e:
            self.emitter.emit(
                EventType.PLUGIN_FAILED,
                f"Plugin failed: {plugin_name} - {e}",
                plugin=plugin_name,
                world_id=str(world.id),
                error=str(e),
            )
            raise

    async def _execute_parallel(
        self,
        world: World,
        plugin_names: list[str],
        plugin_params: dict[str, dict[str, Any]],
    ) -> list[PluginResult]:
        """Execute multiple plugins in parallel.

        Args:
            world: World to modify
            plugin_names: List of plugin names to execute
            plugin_params: Parameters for each plugin

        Returns:
            List of PluginResults
        """
        tasks = [
            self._execute_plugin(world, name, plugin_params.get(name, {}))
            for name in plugin_names
        ]
        return await asyncio.gather(*tasks)

    def _build_dependency_graph(self, pipeline: list[str]) -> nx.DiGraph:
        """Build dependency graph from plugin dependencies.

        Args:
            pipeline: List of plugin names

        Returns:
            Directed graph of dependencies
        """
        graph = nx.DiGraph()

        for plugin_name in pipeline:
            plugin = self.get_plugin(plugin_name)
            if not plugin:
                continue

            graph.add_node(plugin_name)

            # Add edges for dependencies
            for dep in plugin.metadata.dependencies:
                if dep in pipeline:
                    graph.add_edge(dep, plugin_name)  # dep -> plugin

        return graph

    def _validate_dependencies(self, graph: nx.DiGraph, pipeline: list[str]) -> None:
        """Validate that all dependencies are satisfied.

        Args:
            graph: Dependency graph
            pipeline: List of plugin names

        Raises:
            PipelineExecutionError: If dependencies are invalid
        """
        # Check for cycles
        if not nx.is_directed_acyclic_graph(graph):
            cycles = list(nx.simple_cycles(graph))
            msg = f"Circular dependencies detected: {cycles}"
            raise PipelineExecutionError(msg)

        # Check for missing dependencies
        for plugin_name in pipeline:
            plugin = self.get_plugin(plugin_name)
            if not plugin:
                continue

            missing = [
                dep for dep in plugin.metadata.dependencies if dep not in pipeline
            ]
            if missing:
                msg = f"Plugin {plugin_name} has unmet dependencies: {missing}"
                raise PipelineExecutionError(msg)

    def _plan_execution(
        self, graph: nx.DiGraph, pipeline: list[str]
    ) -> list[str | list[str]]:
        """Plan execution order with parallelization.

        Returns a list where each element is either:
        - A single plugin name (sequential execution)
        - A list of plugin names (parallel execution)

        Args:
            graph: Dependency graph
            pipeline: List of plugin names

        Returns:
            Execution plan
        """
        # Group plugins by their level in the dependency tree
        levels: dict[int, list[str]] = defaultdict(list)

        for node in nx.topological_sort(graph):
            # Find the maximum level of all predecessors
            predecessors = list(graph.predecessors(node))
            if predecessors:
                level = (
                    max(self._get_node_level(levels, pred) for pred in predecessors) + 1
                )
            else:
                level = 0

            levels[level].append(node)

        # Build execution plan
        plan: list[str | list[str]] = []
        for level in sorted(levels.keys()):
            plugins_at_level = levels[level]
            if len(plugins_at_level) == 1:
                plan.append(plugins_at_level[0])
            else:
                plan.append(plugins_at_level)

        return plan

    def _get_node_level(self, levels: dict[int, list[str]], node: str) -> int:
        """Get the level of a node in the levels dict."""
        for level, nodes in levels.items():
            if node in nodes:
                return level
        return 0

    def _make_progress_callback(self, plugin_name: str) -> Callable[[float, str], None]:
        """Create a progress callback for a plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Progress callback function
        """

        def callback(progress: float, message: str) -> None:
            self.emitter.emit(
                EventType.PLUGIN_PROGRESS,
                message,
                plugin=plugin_name,
                progress=progress,
            )

        return callback
