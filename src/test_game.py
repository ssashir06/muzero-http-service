import os
from fastapi.testclient import TestClient
from unittest import mock
import main

client = TestClient(main.app)
dummy_test_model = "submodules/muzero-general/results/scorefour/2020-12-28--19-27-14/model.checkpoint"

@mock.patch.dict(os.environ, {"MODEL_PATH_scorefour": dummy_test_model})
def test_read_main():
    response = client.post("/game/scorefour/expert?seed=1000", json={
        "steps":[]
    })
    assert response.status_code == 200

@mock.patch.dict(os.environ, {"MODEL_PATH_scorefour": dummy_test_model})
def test_use_wrong_game():
    response = client.post("/game/baseball/expert?seed=1000", json={
        "steps":[]
    })
    assert response.status_code == 404
    
@mock.patch.dict(os.environ, {"MODEL_PATH_scorefour": dummy_test_model})
def test_use_wrong_opponent():
    response = client.post("/game/scorefour/ai?seed=1000", json={
        "steps":[]
    })
    assert response.status_code == 404
