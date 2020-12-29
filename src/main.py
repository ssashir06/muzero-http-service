from typing import Optional
from fastapi import Body, FastAPI
from self_play_replicate import SelfPlayReplicate
from muzero.games.abstract_game import AbstractGame
from muzero.games import scorefour
from replication import Replication

app = FastAPI()
#checkpoint = None

@app.post("/game/{game_name}")
def calculate_game_step(game_name: str, seed: int, replication: Replication):
    replicate: SelfPlayReplicate = None
    game_module = scorefour # FIXME: Use game_name

    checkpoint = None
    if checkpoint is None:
        file_name = 'src/submodules/muzero_general/results/scorefour/2020-12-28--19-27-14/model.checkpoint'
        replicate = SelfPlayReplicate(game_module, seed, checkpoint_file=file_name)
        checkpoint = replicate.checkpoint
    else:
        replicate = SelfPlayReplicate(game_module, seed, checkpoint=checkpoint)

    replicate_buffer = [
        (step.action, step.root, step.player) for step in replication.steps
    ]
    replicate.replicate_game(replicate_buffer)

    action, done = replicate.add_action(0, 0, "expert")

    return {
        "replication": [{
            'action': action,
            'root': root,
            'player': player,
        } for (action, root, player) in replicate.get_replicate_buffer()],
        "action": action,
        "done": done,
    }
