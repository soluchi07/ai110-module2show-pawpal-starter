# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

PawPal+ implements several sophisticated algorithms to optimize pet care scheduling:

### 1. Greedy Priority-Based Scheduling
The core `generate_plan()` algorithm uses a greedy approach to build optimal daily schedules:
- **Time Complexity**: O(n² log n) for n tasks
- **Strategy**: Schedules high-priority rigid tasks first, then fills gaps with flexible tasks
- **Considerations**: Owner availability, task time windows, dependencies, and pet species needs
- **Process**: Sorts tasks by dynamic priority and duration, then attempts to schedule each in the best available time slot

### 2. Dynamic Priority Calculation
Tasks receive priority scores that adapt based on urgency:
- **Base Priority**: High (3.0), Medium (2.0), Low (1.0)
- **Urgency Boost**: Up to +1.0 when deadline is within 120 minutes
- **Formula**: `priority_value + (1.0 - time_until_deadline / 120.0)`
- **Time Complexity**: O(1)
- Ensures critical deadlines are never missed by elevating priority as time runs out

### 3. Dependency Management
Enforces task ordering constraints (e.g., "Give medication" must follow "Feed pet"):
- **Validation**: `_check_dependencies()` verifies all prerequisites are met before scheduling
- **Time Complexity**: O(n) per check
- Automatically defers tasks with unsatisfied dependencies

### 4. Gap-Filling Algorithm
Maximizes schedule efficiency by utilizing free time:
- **Process**: Identifies gaps ≥15 minutes between rigid tasks
- **Strategy**: Fits flexible tasks into available gaps within their time windows
- **Time Complexity**: O(n log n + g·f) where g=gaps, f=flexible tasks
- Ensures no wasted time while respecting task constraints

### 5. Conflict Detection
Identifies overlapping tasks with an optimized algorithm:
- **Method**: `detect_scheduling_conflicts()` uses sorted comparison
- **Time Complexity**: O(n log n) with early exit optimization
- **Features**: 
  - Sorts tasks by start time for efficient comparison
  - Early termination when no more overlaps are possible
  - Returns human-readable warnings with exact overlap duration
- **Behavior**: Non-blocking warnings (never crashes the scheduler)

### 6. Incremental Time Slot Search
Finds optimal scheduling times with flexibility:
- **Method**: `_find_best_time()` attempts earliest fit, then searches in 15-minute increments
- **Search Depth**: Up to 120 minutes ahead
- **Time Complexity**: O(k·s) where k=attempts (max 8), s=occupied slots
- Balances preference for early scheduling with conflict avoidance

### 7. Recurring Task Management
Automates routine care with intelligent task regeneration:
- **Frequencies**: Daily and weekly recurrence patterns
- **Auto-Regeneration**: `mark_task_complete()` creates next occurrence when task is completed
- **Time Complexity**: O(1) for task regeneration
- Perfect for feeding schedules, walks, medication, and grooming

### 8. Task Organization Utilities
Provides flexible task management:
- **Sorting**: `sort_by_time()` orders tasks chronologically (O(n log n))
- **Filtering**: `filter_tasks()` by completion status and pet name
- **Validation**: Built-in constraint checking on all tasks

## Smarter Scheduling

PawPal+ now includes advanced scheduling features:

### Recurring Tasks
- **Daily & Weekly Tasks**: Mark tasks with `frequency="daily"` or `frequency="weekly"`
- **Auto-Regeneration**: When a recurring task is marked complete, a new instance is automatically created for the next occurrence
- Perfect for routine care like feeding, walks, and medication

### Task Management
- **Sort by Time**: `sort_by_time()` method returns tasks in chronological order
- **Smart Filtering**: `filter_tasks()` allows filtering by:
  - Completion status (completed/incomplete)
  - Pet name (for multi-pet households)
- **Completion Tracking**: Built-in `completed` attribute on all tasks

### Conflict Detection
- **Lightweight Warnings**: `detect_scheduling_conflicts()` identifies overlapping tasks without crashing
- **Optimized Algorithm**: 
  - Sorts tasks by start time (O(n log n))
  - Early exit optimization reduces unnecessary comparisons
  - Returns human-readable warning messages with exact overlap duration
- **Proactive Prevention**: Catches scheduling conflicts before they become problems

### Performance Optimizations
- Helper method `_tasks_overlap()` for cleaner, reusable overlap logic
- Greedy scheduling algorithm balances speed with effectiveness
- Gap-filling for flexible tasks maximizes schedule utilization

All core scheduling methods now include comprehensive docstrings with algorithm explanations and complexity analysis.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### 📸 Demo
<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>