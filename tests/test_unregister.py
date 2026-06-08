from urllib.parse import quote


def test_unregister_removes_participant(client):
    activity_name = "Chess Club"
    email = "removable.student@mergington.edu"

    signup = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    unregister = client.delete(
        f"/activities/{quote(activity_name)}/unregister",
        params={"email": email},
    )

    assert signup.status_code == 200
    assert unregister.status_code == 200
    assert unregister.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        f"/activities/{quote('Unknown Club')}/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_student_not_registered(client):
    response = client.delete(
        f"/activities/{quote('Chess Club')}/unregister",
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
