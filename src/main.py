import importlib
import re
import hashlib
import os
from typing import Optional
from fastapi import Body, FastAPI, HTTPException
from muzero.games.abstract_game import AbstractGame
from muzero.games import scorefour
from self_play_replicate import SelfPlayReplicate
from replication import Replication

app = FastAPI()

def get_hash_for_model(file_name: str) -> str:
    h = hashlib.md5()
    with open(file_name, 'rb') as f:
        fb = f.read()
        while len(fb) > 0:
            h.update(fb)
            fb = f.read()

    return h.hexdigest()

@app.post("/game/{game_name}/{opponent}")
def calculate_game_step(
    game_name: str, opponent: str, 
    replication: Replication,
    human_action: Optional[int] = None, seed: Optional[int] = None,
    temperature: Optional[float] = 0, temperature_threshold: Optional[float] = 0,
    preffered_model_hash: Optional[str] = None
):
    if not opponent in ['self', 'random', 'expert', 'human']:
        raise HTTPException(status_code=404, detail=f"The opponent '{opponent}' is invalid.")

    if (opponent == 'human' and human_action is None 
        or opponent != 'human' and human_action is not None
        ):
        raise HTTPException(status_code=400, detail=f"The opponent is '{opponent}', but human_action is '{human_action}'.")

    if not re.match('^[a-zA-Z][a-zA-Z0-9_]*$', game_name):
        raise HTTPException(status_code=404, detail=f"The game_name '{game_name}' is invalid.")
    
    try:
        game_module = importlib.import_module("muzero.games." + game_name)
    except ModuleNotFoundError as err:
        raise HTTPException(status_code=404, detail=f"The game_name '{game_name}' is not found.")

    file_name = os.getenv(f"MODEL_PATH_{game_name}")
    if file_name is None or not os.path.isfile(file_name):
        raise HTTPException(status_code=404, detail=f"The model for game_name '{game_name}' is not found.")

    actual_hash = get_hash_for_model(file_name)
    if preffered_model_hash is not None and actual_hash != preffered_model_hash:
        raise HTTPException(status_code=400, detail=f"Prefferd hash code is wrong. hash was '{actual_hash}'.")

    replicate = SelfPlayReplicate(game_module, seed, checkpoint_file=file_name)
    checkpoint = replicate.checkpoint

    try:
        replicate_buffer = [
            (step['action'], step['root'], step['player']) for step in replication.steps
        ]
    except TypeError:
        raise HTTPException(status_code=400, detail=f"Cannot perse the replica steps")
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Cannot perse the replica steps")

    if not all([
        action in replicate.config.action_space
        and (root is None or isinstance(root, float) or isinstance(root, int))
        and player in replicate.config.players
        for (action, root, player) in replicate_buffer
    ]):
        raise HTTPException(status_code=400, detail=f"The replica steps are including wrong value(s).")

    try:
        replicate.replicate_game(replicate_buffer)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=f"An error occurred while replicating game history: {err}")

    try:
        action, action_str = replicate.add_action(
            opponent,
            temperature=temperature, temperature_threshold=temperature_threshold,
            human_action=human_action)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=f"An error occurred while processing action: {err}")
    
    return {
        "model_hash": actual_hash,
        "action": {
            "number": action,
            "text": action_str,
        },
        "done": replicate.done,
        "steps": [{
            'action': action,
            'root': root,
            'player': player,
        } for (action, root, player) in replicate.get_history_buffer()],
    }
