from urllib.parse import quote


def test_signup_successfully_adds_participant(client):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        f"/activities/{quote('Unknown Club')}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    first = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    second = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Student already signed up for this activity"
