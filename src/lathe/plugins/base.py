"""Base classes and interfaces for the plugin system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable



@dataclass
class PluginMetadata:
    """Metadata describing a plugin."""

    name: str
    version: str
    dependencies: list[str] = field(default_factory=list)
    description: str = ""
    author: str = ""


class PluginResult:
    """Result returned by a plugin execution."""

    def __init__(self, success: bool, message: str = "", data: dict[str, Any] | None = None):
        self.success = success
        self.message = message
        self.data = data or {}


class SimulationPlugin(ABC):
    """Base class for all simulation plugins.

    Simulation plugins modify the world state by adding or updating
    data layers (elevation, temperature, etc.).
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""

    @abstractmethod
    async def execute(
        self,
        world: "World",
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> PluginResult:
        """Execute the simulation.

        Args:
            world: World object to modify
            params: Plugin-specific parameters
            progress_callback: Optional callback for progress updates.
                               Called with (progress: 0.0-1.0, message: str)

        Returns:
            PluginResult indicating success/failure
        """

    def validate_params(self, params: dict[str, Any]) -> tuple[bool, str]:
        """Validate parameters before execution.

        Args:
            params: Parameters to validate

        Returns:
            Tuple of (valid: bool, error_message: str)
        """
        return True, ""

    def get_required_data_layers(self) -> list[str]:
        """Return list of data layers this plugin requires.

        For example, climate simulation might require 'elevation' and 'insolation'.

        Returns:
            List of required data layer names
        """
        return []

    def get_produced_data_layers(self) -> list[str]:
        """Return list of data layers this plugin produces.

        For example, terrain generation produces 'elevation'.

        Returns:
            List of produced data layer names
        """
        return []


class AnalysisPlugin(ABC):
    """Base class for analysis plugins.

    Analysis plugins examine the world state and extract information
    (e.g., POI detection) without modifying the world.
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""

    @abstractmethod
    async def analyze(
        self,
        world: "World",
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> PluginResult:
        """Analyze the world.

        Args:
            world: World object to analyze
            params: Plugin-specific parameters
            progress_callback: Optional callback for progress updates

        Returns:
            PluginResult with analysis data
        """

    def validate_params(self, params: dict[str, Any]) -> tuple[bool, str]:
        """Validate parameters before execution."""
        return True, ""

    def get_required_data_layers(self) -> list[str]:
        """Return list of data layers this plugin requires."""
        return []
