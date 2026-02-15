"""Basic tests for PawPal+ core classes."""

from pawpal_system import Pet, Task


def test_task_completion() -> None:
	"""Task completion updates the completed status."""
	task = Task(
		description="Check water",
		start_time="09:00",
		duration_minutes=5,
		frequency="daily",
	)

	assert task.completed is False
	task.mark_complete()
	assert task.completed is True


def test_pet_task_addition_increases_count() -> None:
	"""Adding a task to a pet increments its task count."""
	pet = Pet(name="Mochi", species="dog")
	task = Task(
		description="Morning walk",
		start_time="08:00",
		duration_minutes=30,
		frequency="daily",
	)

	initial_count = len(pet.tasks)
	added = pet.add_task(task)

	assert added is True
	assert len(pet.tasks) == initial_count + 1
