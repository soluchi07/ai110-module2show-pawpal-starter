"""
PawPal+ System - Core Classes

Implementation for Task, Pet, Owner, and Scheduler.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Iterable, Tuple


def _time_to_minutes(value: Optional[object]) -> Optional[int]:
    """Convert HH:MM strings or minutes to total minutes."""
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


@dataclass
class Task:
    """Represents a single pet care activity."""

    description: str
    start_time: Optional[int]
    duration_minutes: int
    frequency: str
    completed: bool = False

    def __post_init__(self) -> None:
        """Normalize start_time to minutes when needed."""
        if self.start_time is not None and not isinstance(self.start_time, int):
            self.start_time = _time_to_minutes(self.start_time)

    def validate(self) -> bool:  # sourcery skip: assign-if-exp, reintroduce-else
        """Validate task fields."""
        if not self.description or not self.description.strip():
            return False
        if not self.frequency or not self.frequency.strip():
            return False
        if not (1 <= self.duration_minutes <= 1440):
            return False
        if self.start_time is None:
            return True
        return 0 <= self.start_time < 1440

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def reschedule(self, new_time: Optional[object]) -> bool:
        """Update the task start time, accepting minutes or HH:MM strings."""
        minutes = _time_to_minutes(new_time)
        if minutes is None:
            return False
        if not (0 <= minutes < 1440):
            return False
        self.start_time = minutes
        return True

    def get_details(self) -> Dict[str, object]:
        """Return task details as a dictionary."""
        return {
            "description": self.description,
            "start_time": self.start_time,
            "duration_minutes": self.duration_minutes,
            "frequency": self.frequency,
            "completed": self.completed,
        }


@dataclass
class Pet:
    """Stores pet details and its task list."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)
    details: Dict[str, str] = field(default_factory=dict)

    def add_task(self, task: Task) -> bool:
        """Add a task if it is valid."""
        if not task.validate():
            return False
        self.tasks.append(task)
        return True

    def remove_task(self, task: Task) -> bool:
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)
            return True
        return False

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return this pet's tasks."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]

    def add_detail(self, key: str, value: str) -> None:
        """Add or update a pet detail (e.g., age, breed)."""
        self.details[key] = value


@dataclass
class Owner:
    """Manages multiple pets and provides access to all tasks."""

    name: str
    pets: List[Pet] = field(default_factory=list)
    contact: Optional[str] = None

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> bool:
        """Remove a pet from this owner."""
        if pet in self.pets:
            self.pets.remove(pet)
            return True
        return False

    def get_pet(self, name: str) -> Optional[Pet]:  # sourcery skip: use-next
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return all tasks across all pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Optional[Owner] = None):
        self.owner = owner

    def set_owner(self, owner: Owner) -> None:
        """Attach an owner to this scheduler."""
        self.owner = owner

    def _iter_tasks(self, include_completed: bool) -> Iterable[Tuple[Pet, Task]]:
        """Yield pet-task pairs across the owner's pets."""
        # sourcery skip: for-append-to-extend
        if self.owner is None:
            return []
        pairs: List[Tuple[Pet, Task]] = []
        for pet in self.owner.pets:
            for task in pet.get_tasks(include_completed=include_completed):
                pairs.append((pet, task))
        return pairs

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return all tasks across pets."""
        if self.owner is None:
            return []
        return self.owner.get_all_tasks(include_completed=include_completed)

    def organize_tasks(self, include_completed: bool = True) -> List[Tuple[Pet, Task]]:
        """Return tasks sorted by start time, then pet name, then description."""
        pairs = list(self._iter_tasks(include_completed=include_completed))
        return sorted(
            pairs,
            key=lambda item: (
                item[1].start_time is None,
                item[1].start_time if item[1].start_time is not None else 0,
                item[0].name.lower(),
                item[1].description.lower(),
            ),
        )

    def build_daily_plan(self, include_completed: bool = False) -> List[Tuple[Pet, Task]]:
        """Create an ordered plan of tasks for the day."""
        return self.organize_tasks(include_completed=include_completed)

    def mark_task_complete(self, pet_name: str, description: str) -> bool:
        """Mark the first matching task as completed."""
        if self.owner is None:
            return False
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return False
        for task in pet.tasks:
            if task.description == description:
                task.mark_complete()
                return True
        return False
