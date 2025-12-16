import pytest
from fitness_app.models import Exercise, SessionSet


@pytest.mark.django_db
def test_add_exercise(client):
    response = client.post(
        "/exercise/add/",
        {
            "name": "Bench Press",
            "muscle_group": "Chest",
        },
    )

    assert Exercise.objects.filter(name="Bench Press").exists()


@pytest.mark.django_db
def test_add_session_set(client):
    # create exercise
    exercise = Exercise.objects.create(name="Squat", muscle_group="Legs")

    response = client.post(
        "/log/",
        {
            "exercise": exercise.id,
            "performed_at": "2025-01-01",
            "weight": "185",
            "reps": "5",
        },
    )

    session = SessionSet.objects.first()
    assert session.exercise == exercise
    assert session.weight == 185.0
    assert session.reps == 5
