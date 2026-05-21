def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_happy_path(client):
    email = "teststudent@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup?email=teststudent@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_activity_returns_400_for_duplicate(client):
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup?email=teststudent@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_happy_path(client):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_remove_participant_returns_404_for_missing_participant(client):
    response = client.delete("/activities/Chess%20Club/participants/notfound@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_remove_participant_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/participants/teststudent@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
