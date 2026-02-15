"""
PawPal+ System - Class Skeletons

Skeleton classes based on UML design for the pet care planning system.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from enum import Enum


class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Represents a pet care task."""
    
    type: str
    title: str
    notes: str
    time_window: Tuple[int, int]
    duration_minutes: int
    priority: str
    
    def validate(self) -> bool:
        """Validate task constraints."""
        if not self.title or not self.title.strip():
            return False
        if self.duration_minutes <= 0:
            return False
        if self.priority not in [p.value for p in Priority]:
            return False
        if self.time_window[0] >= self.time_window[1]:
            return False
        return self.time_window[0] >= 0 and self.time_window[1] <= 1440
    
    def get_details(self) -> dict:
        """Return task details as a dictionary."""
        return {
            "type": self.type,
            "title": self.title,
            "notes": self.notes,
            "time_window": self.time_window,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority
        }


@dataclass
class Pet:
    """Represents a pet with its characteristics and preferences."""
    
    name: str
    species: str
    needs: List[str] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)
    
    def add_preference(self, key: str, value: str) -> None:
        """Add or update a preference for this pet."""
        self.preferences[key] = value
    
    def get_preferences(self) -> Dict[str, str]:
        """Return all preferences for this pet."""
        return self.preferences.copy()


@dataclass
class PetOwner:
    """Represents a pet owner with availability and preferences."""
    
    name: str
    availability: Tuple[int, int]
    preferences: Dict[str, str] = field(default_factory=dict)
    pet: Optional['Pet'] = None  # Relationship: owner owns pet
    
    def add_preference(self, key: str, value: str) -> None:
        """Add or update a preference for this owner."""
        self.preferences[key] = value
    
    def get_preferences(self) -> Dict[str, str]:
        """Return all preferences for this owner."""
        return self.preferences.copy()


@dataclass
class PlanItem:
    """Represents a scheduled task in the daily plan."""
    
    task: Task
    scheduled_time: int  # -1 if task couldn't be scheduled
    duration_minutes: int
    reason: str = ""  # Explanation for scheduling decision
    
    def get_summary(self) -> str:
        """Return a readable summary of this scheduled item."""
        if self.scheduled_time < 0:
            return f"[Not scheduled] {self.task.title} - {self.reason}"
        hours = self.scheduled_time // 60
        minutes = self.scheduled_time % 60
        time_str = f"{hours:02d}:{minutes:02d}"
        return f"{time_str} - {self.task.title} ({self.duration_minutes}min) - {self.reason}"


class Scheduler:
    """
    Orchestrates pet care task scheduling.
    
    Manages tasks and generates daily plans based on constraints.
    """
    
    def __init__(self):
        """Initialize an empty scheduler."""
        self.tasks: List[Task] = []
        self.pet: Optional[Pet] = None
        self.owner: Optional[PetOwner] = None
    
    def add_task(self, task: Task) -> bool:
        """Add a task to the scheduler.
        
        Returns:
            True if task was added successfully, False if validation failed.
        """
        if not task.validate():
            return False
        self.tasks.append(task)
        return True
    
    def remove_task(self, task: Task) -> bool:
        """Remove a task from the scheduler.
        
        Returns:
            True if task was removed, False if task not found.
        """
        if task in self.tasks:
            self.tasks.remove(task)
            return True
        return False
    
    def clear_tasks(self) -> None:
        """Remove all tasks from the scheduler."""
        self.tasks.clear()
    
    def set_pet(self, pet: Pet) -> None:
        """Set the pet for this scheduler."""
        self.pet = pet
    
    def set_owner(self, owner: PetOwner) -> None:
        """Set the owner for this scheduler."""
        self.owner = owner
    
    def _check_time_overlap(self, start1: int, dur1: int, start2: int, dur2: int) -> bool:
        """Check if two time slots overlap.
        
        Returns:
            True if there is overlap, False otherwise.
        """
        end1 = start1 + dur1
        end2 = start2 + dur2
        return start1 < end2 and start2 < end1
    
    def _get_priority_value(self, priority: str) -> int:
        """Convert priority string to numeric value for sorting."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(priority, 0)
    
    def generate_plan(self) -> List[PlanItem]:
        """Generate a daily schedule for all tasks.
        
        Raises:
            ValueError: If pet or owner is not set.
        
        Returns:
            List of PlanItem objects (scheduled and unscheduled).
        """
        if self.pet is None or self.owner is None:
            raise ValueError("Both pet and owner must be set before generating a plan")
        
        if not self.tasks:
            return []
        
        # Sort tasks by priority (high > medium > low), then by duration
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (self._get_priority_value(t.priority), -t.duration_minutes),
            reverse=True
        )
        
        plan: List[PlanItem] = []
        scheduled_slots: List[Tuple[int, int]] = []  # (start_time, duration)
        
        owner_start = self.owner.availability[0]
        owner_end = self.owner.availability[1]
        
        for task in sorted_tasks:
            task_start = max(task.time_window[0], owner_start)
            task_end = min(task.time_window[1], owner_end)
            
            # Check if task window overlaps with owner availability
            if task_start >= task_end:
                plan.append(PlanItem(
                    task=task,
                    scheduled_time=-1,
                    duration_minutes=task.duration_minutes,
                    reason="Task time window outside owner availability"
                ))
                continue
            
            # Try to find a non-overlapping time slot
            scheduled = False
            current_time = task_start
            
            while current_time + task.duration_minutes <= task_end:
                # Check for conflicts with already scheduled tasks
                has_conflict = False
                for scheduled_start, scheduled_dur in scheduled_slots:
                    if self._check_time_overlap(current_time, task.duration_minutes, 
                                               scheduled_start, scheduled_dur):
                        has_conflict = True
                        # Move to end of conflicting task
                        current_time = scheduled_start + scheduled_dur
                        break
                
                if not has_conflict:
                    # Found a valid slot
                    plan.append(PlanItem(
                        task=task,
                        scheduled_time=current_time,
                        duration_minutes=task.duration_minutes,
                        reason=f"Scheduled ({task.priority} priority)"
                    ))
                    scheduled_slots.append((current_time, task.duration_minutes))
                    scheduled = True
                    break
            
            if not scheduled:
                plan.append(PlanItem(
                    task=task,
                    scheduled_time=-1,
                    duration_minutes=task.duration_minutes,
                    reason="No available time slot without conflicts"
                ))
        
        return plan
