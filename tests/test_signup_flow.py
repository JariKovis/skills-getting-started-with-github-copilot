from urllib.parse import quote

import src.app as app_module


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "message" in payload
    assert new_email in app_module.activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange

    # Act
    response = client.post(
        f"/activities/{quote('Unknown Club', safe='')}/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Programming Class"
    existing_email = app_module.activities[activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    payload = response.json()
    assert "detail" in payload


def test_signup_when_activity_is_full_returns_400(client):
    # Arrange
    activity_name = "Robotics Lab"
    app_module.activities[activity_name] = {
        "description": "Hands-on robotics activities",
        "schedule": "Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 1,
        "participants": ["filled@mergington.edu"],
    }

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": "next@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    payload = response.json()
    assert "detail" in payload
