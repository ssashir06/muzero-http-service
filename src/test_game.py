from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_read_main():
    response = client.post("/game/scorefour?seed=1000", json={
        "steps":[]
    })
    assert response.status_code == 200
    print(response.json())