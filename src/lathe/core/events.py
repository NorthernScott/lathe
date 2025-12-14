"""Event system for progress reporting and notifications."""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable


class EventType(Enum):
    """Types of events that can be emitted."""

    GENERATION_STARTED = "generation_started"
    GENERATION_COMPLETED = "generation_completed"
    GENERATION_FAILED = "generation_failed"
    PLUGIN_STARTED = "plugin_started"
    PLUGIN_PROGRESS = "plugin_progress"
    PLUGIN_COMPLETED = "plugin_completed"
    PLUGIN_FAILED = "plugin_failed"
    ANALYSIS_STARTED = "analysis_started"
    ANALYSIS_COMPLETED = "analysis_completed"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


@dataclass
class Event:
    """Represents an event in the system."""

    def __init__(
        self,
        event_type: EventType,
        message: str,
        timestamp: datetime = datetime.now(timezone.utc),
        **kwargs,
    ):
        self.type: EventType = event_type
        self.message: str = message
        self.timestamp: datetime = timestamp
        self.data: dict[str, Any] = kwargs


class EventEmitter:
    """Event emitter for publishing events to subscribers."""

    def __init__(self):
        self._subscribers: dict[EventType, list[Callable[[Event], None]]] = {}
        self._global_subscribers: list[Callable[[Event], None]] = []

    def subscribe(
        self,
        event_type: EventType | None,
        callback: Callable[[Event], None],
    ) -> None:
        """Subscribe to events.

        Args:
            event_type: Type of event to subscribe to (None for all events)
            callback: Function to call when event occurs
        """
        if event_type is None:
            self._global_subscribers.append(callback)
        else:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)

    def unsubscribe(
        self,
        event_type: EventType | None,
        callback: Callable[[Event], None],
    ) -> None:
        """Unsubscribe from events.

        Args:
            event_type: Type of event to unsubscribe from (None for all events)
            callback: Callback function to remove
        """
        if event_type is None:
            if callback in self._global_subscribers:
                self._global_subscribers.remove(callback)
        else:
            if (
                event_type in self._subscribers
                and callback in self._subscribers[event_type]
            ):
                self._subscribers[event_type].remove(callback)

    def emit(
        self,
        event_type: EventType,
        message: str,
        timestamp: datetime = datetime.now(timezone.utc),
        **kwargs,
    ) -> None:
        """Emit an event to all subscribers.

        Args:
            event_type: Type of event
            message: Event message
            timestamp: Event timestamp in UTC
            **kwargs: Additional event data
        """
        event = Event(event_type, message, timestamp, **kwargs)

        # Notify global subscribers
        for callback in self._global_subscribers:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event subscriber: {e}")

        # Notify type-specific subscribers
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event subscriber: {e}")


class ProgressTracker:
    """Helper class for tracking and reporting progress."""

    def __init__(
        self,
        emitter: EventEmitter,
        plugin_name: str,
        total_steps: int = 100,
    ):
        self.emitter = emitter
        self.plugin_name = plugin_name
        self.total_steps = total_steps
        self.current_step = 0

    def update(self, step: int | None = None, message: str = "") -> None:
        """Update progress.

        Args:
            step: Current step (if None, increments by 1)
            message: Progress message
        """
        if step is not None:
            self.current_step = step
        else:
            self.current_step += 1

        progress = min(self.current_step / self.total_steps, 1.0)

        self.emitter.emit(
            EventType.PLUGIN_PROGRESS,
            message or f"{self.plugin_name}: {progress:.1%}",
            plugin=self.plugin_name,
            progress=progress,
            step=self.current_step,
            total_steps=self.total_steps,
        )

    def set_total_steps(self, total: int) -> None:
        """Update total steps."""
        self.total_steps = total

    def complete(self, message: str = "") -> None:
        """Mark as complete."""
        self.current_step = self.total_steps
        self.emitter.emit(
            EventType.PLUGIN_COMPLETED,
            message or f"{self.plugin_name}: Complete",
            plugin=self.plugin_name,
            progress=1.0,
        )


# Global event emitter instance
_global_emitter: EventEmitter | None = None


def get_global_emitter() -> EventEmitter:
    """Get the global event emitter instance."""
    global _global_emitter
    if _global_emitter is None:
        _global_emitter = EventEmitter()
    return _global_emitter


def set_global_emitter(emitter: EventEmitter) -> None:
    """Set the global event emitter instance."""
    global _global_emitter
    _global_emitter = emitter
