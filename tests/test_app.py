from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]

    # restore state for later tests/logical consistency in the in-memory app
    client.post(f"/activities/{activity_name}/signup?email={email}")
