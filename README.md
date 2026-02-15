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
