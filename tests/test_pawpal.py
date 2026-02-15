"""Basic tests for PawPal+ core classes."""

from pawpal_system import Pet, Task


def test_task_validation_and_details() -> None:
	"""Task validation returns true for valid inputs."""
	task = Task(
		title="Check water",
		task_type="other",
		duration_minutes=5,
		priority="medium",
		time_window=(540, 600),
		start_time="09:00",
	)

	assert task.validate() is True
	details = task.get_details()
	assert details["title"] == "Check water"
	assert details["start_time"] == 540


def test_pet_preferences() -> None:
	"""Pets store and return preferences."""
	pet = Pet(name="Mochi", species="dog")
	pet.add_preference("favorite_time", "morning")

	preferences = pet.get_preferences()
	assert preferences["favorite_time"] == "morning"
