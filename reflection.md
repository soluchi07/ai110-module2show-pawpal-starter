# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Initial UML: a small set of core classes centered on scheduling flow: `Scheduler` orchestrates, `Task` represents a care activity, and `PetOwner`/`Pet` hold profile data used by the planner. I modeled the flow as: create task → enrich with pet/owner info → generate/display plan.
- Classes and responsibilities:
    - `Task`: store task details (type, time window, duration, priority).
    - `Pet`: store pet info (species, needs, preferences).
    - `PetOwner`: store owner info (availability, preferences).
    - `Scheduler`: accept tasks, apply constraints/preferences from `Pet` and `PetOwner`, and produce a plan for display.

**b. Design changes**

Yes, several design changes were made during implementation to address bottlenecks and missing relationships:

- **Added Priority Enum**: Introduced a `Priority` enum class to enforce valid priority values ("low", "medium", "high") instead of accepting any string. This prevents runtime errors from typos and improves type safety.

- **Enhanced Task validation**: Expanded `Task.validate()` to check for empty titles, negative durations, invalid priorities, backwards time windows (end before start), and out-of-range times (outside 0-1440 minutes). This catches configuration errors early.

- **Added PetOwner → Pet relationship**: Added an optional `pet` field to `PetOwner` to represent the "owns" relationship shown in the UML. This makes the ownership explicit and allows for future features like accessing pet preferences through the owner.

- **Changed add_task() return type**: Modified `Scheduler.add_task()` from `None` to `bool` so callers can detect when a task fails validation instead of silently ignoring invalid tasks.

- **Added PlanItem.reason field**: Added a `reason: str` field to `PlanItem` to explain why each task was scheduled at its time (or why it couldn't be scheduled). This provides transparency in the scheduling decisions.

- **Added conflict detection logic**: Implemented `_check_time_overlap()` helper method and modified `generate_plan()` to detect and prevent overlapping task schedules. The scheduler now maintains a list of occupied time slots and finds non-conflicting windows.

- **Added task removal methods**: Added `remove_task()` and `clear_tasks()` methods to `Scheduler` because you could add tasks but never remove them, limiting flexibility during testing and updates.

 **Added validation in generate_plan()**: Changed `generate_plan()` to raise `ValueError` if pet or owner is not set, rather than silently returning an empty list. This gives clearer error messages when the scheduler is misconfigured.

- **Improved priority sorting**: Added `_get_priority_value()` helper to convert priority strings to numeric values for consistent sorting. Tasks are now sorted by priority first, then by duration (longer tasks scheduled first to maximize utilization).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
