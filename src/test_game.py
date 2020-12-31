import os
from fastapi.testclient import TestClient
from unittest import mock
import main

client = TestClient(main.app)
dummy_test_game = "MODEL_PATH_tictactoe"
dummy_test_model = "models/_for_test/tictactoe/model.checkpoint"

@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_info():
    response = client.get("/game/tictactoe")
    assert response.status_code == 200
    
@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_info_with_wrong_name():
    response = client.get("/game/baseball")
    assert response.status_code == 404

@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_game_start():
    response = client.get("/game/tictactoe/1000")
    assert response.status_code == 200
    
@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_info_with_wrong_name():
    response = client.get("/game/baseball/1000")
    assert response.status_code == 404

@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_action_random():
    response = client.put("/game/tictactoe/1000/action?opponent=random", json={
        "steps":[]
    })
    assert response.status_code == 200

@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_action_with_wrong_game():
    response = client.put("/game/baseball/1000/action?opponent=expert", json={
        "steps":[]
    })
    assert response.status_code == 404
    
@mock.patch.dict(os.environ, {dummy_test_game: dummy_test_model})
def test_action_with_wrong_opponent():
    response = client.put("/game/tictactoe/1000/action?opponent=ai", json={
        "steps":[]
    })
    assert response.status_code == 404
