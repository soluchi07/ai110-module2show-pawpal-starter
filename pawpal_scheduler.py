"""
PawPal+ Scheduler Classes

Implements the core classes for the pet care planning system:
- Task: Represents a pet care activity
- Pet: Stores pet information and preferences
- PetOwner: Stores owner information and availability
- PlanItem: Represents a scheduled task
- Scheduler: Orchestrates task scheduling based on constraints
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


def _time_to_minutes(value: Optional[object]) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if ":" in text:
            hours_str, minutes_str = text.split(":", 1)
            if hours_str.isdigit() and minutes_str.isdigit():
                return int(hours_str) * 60 + int(minutes_str)
    return None


class Task:
    """Represents a pet care task."""

    def __init__(
        self,
        title: str,
        task_type: str,
        duration_minutes: int,
        priority: str,
        time_window: Tuple[int, int] = (0, 1440),
        notes: str = "",
        start_time: Optional[object] = None,
    ):
        """
        Initialize a Task.

        Args:
            title: Display name of the task
            task_type: Category (e.g., 'walk', 'feed', 'groom')
            duration_minutes: How long the task takes
            priority: 'low', 'medium', or 'high'
            time_window: (start_minutes, end_minutes) in 24h format, default (0, 1440) for all day
            notes: Additional details about the task
            start_time: Optional scheduled start time (minutes or HH:MM)
        """
        self.title = title
        self.task_type = task_type
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.time_window = time_window
        self.notes = notes
        self.start_time = _time_to_minutes(start_time)

    def validate(self) -> bool:
        """Validate task constraints."""
        if not self.title:
            return False
        if not (1 <= self.duration_minutes <= 1440):
            return False
        if self.priority not in ["low", "medium", "high"]:
            return False
        if self.time_window[0] >= self.time_window[1]:
            return False
        if self.start_time is None:
            return True
        return 0 <= self.start_time < 1440

    def get_details(self) -> Dict:
        """Return task details as a dictionary."""
        return {
            "title": self.title,
            "type": self.task_type,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "time_window": self.time_window,
            "start_time": self.start_time,
            "notes": self.notes,
        }

    def __repr__(self) -> str:
        return f"Task('{self.title}', {self.duration_minutes}min, {self.priority})"


class Pet:
    """Represents a pet with its characteristics and preferences."""

    def __init__(self, name: str, species: str, needs: Optional[List[str]] = None):
        """
        Initialize a Pet.

        Args:
            name: Pet's name
            species: 'dog', 'cat', or 'other'
            needs: List of pet's needs (e.g., ['exercise', 'feeding', 'socialization'])
        """
        self.name = name
        self.species = species
        self.needs = needs or []
        self.preferences: Dict[str, str] = {}

    def add_preference(self, key: str, value: str) -> None:
        """Add or update a preference for this pet."""
        self.preferences[key] = value

    def get_preferences(self) -> Dict[str, str]:
        """Return all preferences for this pet."""
        return self.preferences.copy()

    def __repr__(self) -> str:
        return f"Pet('{self.name}', {self.species})"


class PetOwner:
    """Represents a pet owner with availability and preferences."""

    def __init__(self, name: str, availability: Tuple[int, int] = (0, 1440)):
        """
        Initialize a PetOwner.

        Args:
            name: Owner's name
            availability: (start_minutes, end_minutes) in 24h format when owner is available
        """
        self.name = name
        self.availability = availability
        self.preferences: Dict[str, str] = {}

    def add_preference(self, key: str, value: str) -> None:
        """Add or update a preference for this owner."""
        self.preferences[key] = value

    def get_preferences(self) -> Dict[str, str]:
        """Return all preferences for this owner."""
        return self.preferences.copy()

    def __repr__(self) -> str:
        return f"PetOwner('{self.name}')"


@dataclass
class PlanItem:
    """Represents a scheduled task in the daily plan."""

    task: Task
    scheduled_time: int  # Minutes from start of day (0-1440)
    duration_minutes: int
    reason: str = ""  # Explanation for why/when this task was scheduled

    def get_summary(self) -> str:
        """Return a readable summary of this scheduled item."""
        hours = self.scheduled_time // 60
        minutes = self.scheduled_time % 60
        time_str = f"{hours:02d}:{minutes:02d}"
        return f"{time_str} - {self.task.title} ({self.duration_minutes}min)"

    def __repr__(self) -> str:
        return f"PlanItem('{self.task.title}' at {self.scheduled_time}min)"


class Scheduler:
    """
    Orchestrates pet care task scheduling.

    Accepts tasks and generates a daily plan based on:
    - Pet needs and preferences
    - Owner availability and preferences
    - Task priorities and time windows
    """

    def __init__(self):
        """Initialize an empty scheduler."""
        self.tasks: List[Task] = []
        self.pet: Optional[Pet] = None
        self.owner: Optional[PetOwner] = None

    def add_task(self, task: Task) -> bool:
        """
        Add a task to the scheduler.

        Args:
            task: Task object to add

        Returns:
            True if task was added, False if validation failed
        """
        if not task.validate():
            return False
        self.tasks.append(task)
        return True

    def set_pet(self, pet: Pet) -> None:
        """Set the pet for this scheduler."""
        self.pet = pet

    def set_owner(self, owner: PetOwner) -> None:
        """Set the owner for this scheduler."""
        self.owner = owner

    def generate_plan(self) -> List[PlanItem]:
        """
        Generate a daily schedule for all tasks.

        Scheduling logic:
        1. Sort tasks by priority (high > medium > low)
        2. Schedule each task within its time window
        3. Ensure scheduled time fits within owner's availability
        4. Return ordered list of PlanItem objects

        Returns:
            List of PlanItem objects representing the daily schedule
        """
        if not self.pet or not self.owner:
            return []

        if not self.tasks:
            return []

        # Sort tasks by priority (high=3, medium=2, low=1) and duration
        priority_map = {"high": 3, "medium": 2, "low": 1}
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (priority_map.get(t.priority, 1), t.duration_minutes),
            reverse=True,
        )

        plan: List[PlanItem] = []
        current_time = self.owner.availability[0]
        owner_end = self.owner.availability[1]

        for task in sorted_tasks:
            task_start = task.time_window[0]
            task_end = task.time_window[1]

            # Find the earliest valid start time within task's time window
            # and owner's availability
            earliest_start = max(current_time, task_start)
            latest_end = min(owner_end, task_end)

            # Check if there's enough time to fit this task
            if earliest_start + task.duration_minutes <= latest_end:
                plan_item = PlanItem(
                    task=task,
                    scheduled_time=earliest_start,
                    duration_minutes=task.duration_minutes,
                    reason=(
                        "Scheduled during available window "
                        f"({task.priority} priority)"
                    ),
                )
                plan.append(plan_item)
                current_time = earliest_start + task.duration_minutes
            else:
                # Task couldn't fit; note it in a reason but don't schedule
                plan_item = PlanItem(
                    task=task,
                    scheduled_time=-1,  # Sentinel value: not scheduled
                    duration_minutes=task.duration_minutes,
                    reason="No available time slot",
                )
                plan.append(plan_item)

        return plan

    def __repr__(self) -> str:
        return (
            f"Scheduler({len(self.tasks)} tasks, pet={self.pet}, owner={self.owner})"
        )
