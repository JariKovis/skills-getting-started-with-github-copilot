from urllib.parse import quote

import src.app as app_module


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Gym Class"
    existing_email = app_module.activities[activity_name]["participants"][0]

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "message" in payload
    assert existing_email not in app_module.activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange

    # Act
    response = client.delete(
        f"/activities/{quote('Unknown Club', safe='')}/participants",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload


def test_unregister_non_member_returns_404(client):
    # Arrange
    activity_name = "Science Club"
    missing_email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload
