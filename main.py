"""Demo script for PawPal+ core classes."""

from pawpal_system import PetOwner, Pet, Task, Scheduler


def _format_time(minutes: int) -> str:
	hours, mins = divmod(minutes, 60)
	return f"{hours:02d}:{mins:02d}"


def main() -> None:
	owner = PetOwner(name="Jordan", availability=(480, 1320))

	pet = Pet(name="Mochi", species="dog")

	scheduler = Scheduler()
	scheduler.set_pet(pet)
	scheduler.set_owner(owner)

	# Create some recurring tasks
	task_morning_walk = Task(
		title="Morning walk",
		task_type="walk",
		duration_minutes=30,
		priority="high",
		time_window=(480, 600),
		start_time="08:00",
		completed=False,
		frequency="daily",
	)
	scheduler.add_task(task_morning_walk)

	task_breakfast = Task(
		title="Breakfast",
		task_type="feed",
		duration_minutes=15,
		priority="high",
		time_window=(510, 600),
		start_time="08:30",
		completed=False,
		frequency="daily",
	)
	scheduler.add_task(task_breakfast)

	# One-time task
	task_play = Task(
		title="Play time",
		task_type="play",
		duration_minutes=20,
		priority="medium",
		time_window=(900, 1020),
		start_time="15:00",
		completed=False,
		frequency=None,
	)
	scheduler.add_task(task_play)

	# Weekly task
	task_grooming = Task(
		title="Grooming session",
		task_type="grooming",
		duration_minutes=45,
		priority="medium",
		time_window=(1020, 1200),
		start_time="17:00",
		completed=False,
		frequency="weekly",
	)
	scheduler.add_task(task_grooming)

	# CONFLICTING TASK: Overlaps with breakfast (08:30-08:45)
	# This task starts at 08:40 and runs 20 minutes, so it overlaps with breakfast
	task_medication = Task(
		title="Medication time",
		task_type="medical",
		duration_minutes=20,
		priority="high",
		time_window=(500, 700),
		start_time="08:40",  # This overlaps with breakfast (08:30-08:45)
		completed=False,
		frequency=None,
	)
	scheduler.add_task(task_medication)

	print("=" * 60)
	print("INITIAL TASK LIST")
	print("=" * 60)
	print(f"Total tasks: {len(scheduler.tasks)}\n")
	for i, task in enumerate(scheduler.tasks, 1):
		freq_info = f" ({task.frequency})" if task.frequency else " (one-time)"
		print(f"  {i}. {task}{freq_info}")

	# Check for scheduling conflicts
	print("\n" + "=" * 60)
	print("CONFLICT DETECTION")
	print("=" * 60)
	conflicts = scheduler.detect_scheduling_conflicts()
	
	if conflicts:
		print(f"\n{len(conflicts)} conflict(s) detected:\n")
		for warning in conflicts:
			print(f"  {warning}")
	else:
		print("\n✓ No scheduling conflicts detected!")


if __name__ == "__main__":
	main()
