import os
from fastapi.testclient import TestClient
from unittest import mock
import main

client = TestClient(main.app)
dummy_test_game = "MODEL_PATH_tictactoe"
dummy_test_model = "submodules/muzero-general/results/tictactoe/2020-12-31--00-31-12/model.checkpoint"

@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_read_main():
    response = client.post("/game/tictactoe/random?seed=1000", json={
        "steps":[]
    })
    assert response.status_code == 200

@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_use_wrong_game():
    response = client.post("/game/baseball/expert?seed=1000", json={
        "steps":[]
    })
    assert response.status_code == 404
    
@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_use_wrong_opponent():
    response = client.post("/game/tictactoe/ai?seed=1000", json={
        "steps":[]
    })
    assert response.status_code == 404
