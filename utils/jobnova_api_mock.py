import json
from fastapi.testclient import TestClient
from utils.fastapi_app import app, get_db_session

client = TestClient(app)

# loading user request
with open('./json_dumps/ai_json.json', 'r') as f:
    ai_jobs = json.load(f)
# loading database
with open('./json_dumps/jobs_database.json', 'r') as f:
    mock_jobs = json.load(f)

def override_get_db_session():
    return mock_jobs

def test_my_function_api():

    app.dependency_overrides[get_db_session] = override_get_db_session

    response = client.post("/recommendations", json=ai_jobs)

    assert response.status_code == 200

    response = response.json()

    assert len(response) == 10 # counting jobs found

    return response
