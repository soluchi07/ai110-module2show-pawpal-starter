"""Demo script for PawPal+ core classes."""

from pawpal_system import Owner, Pet, Task, Scheduler


def _format_time(minutes: int) -> str:
	hours, mins = divmod(minutes, 60)
	return f"{hours:02d}:{mins:02d}"


def main() -> None:
	owner = Owner(name="Jordan")

	pet_1 = Pet(name="Mochi", species="dog")
	pet_2 = Pet(name="Luna", species="cat")

	pet_1.add_task(
		Task(
			description="Morning walk",
			start_time="08:00",
			duration_minutes=30,
			frequency="daily",
		)
	)
	pet_1.add_task(
		Task(
			description="Breakfast",
			start_time="08:30",
			duration_minutes=15,
			frequency="daily",
		)
	)
	pet_2.add_task(
		Task(
			description="Play time",
			start_time="15:00",
			duration_minutes=20,
			frequency="daily",
		)
	)

	owner.add_pet(pet_1)
	owner.add_pet(pet_2)

	scheduler = Scheduler(owner=owner)
	plan = scheduler.build_daily_plan(include_completed=False)

	print("Today's Schedule")
	print("----------------")
	for pet, task in plan:
		if task.start_time is None:
			time_label = "Anytime"
		else:
			time_label = _format_time(task.start_time)
		print(
			f"{time_label} - {pet.name}: {task.description} "
			f"({task.duration_minutes} min, {task.frequency})"
		)


if __name__ == "__main__":
	main()
