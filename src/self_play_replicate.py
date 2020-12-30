import torch
import numpy
import random
from games.abstract_game import AbstractGame
from self_play import GameHistory, MCTS, SelfPlay
from models import MuZeroNetwork

class SelfPlayReplicate():
    def __init__(
        self, game_module, seed: int, checkpoint_file: str = None, checkpoint: dict = None
    ):
        self.game: AbstractGame = game_module.Game(seed)
        self.config = game_module.MuZeroConfig()
        self.game_history: GameHistory = None
        self.checkpoint = checkpoint
        self.done = False

        # Fix random generator seed
        numpy.random.seed(seed)
        torch.manual_seed(seed)
        random.seed(seed)

        # Load model
        if self.checkpoint is None:
            self.checkpoint = torch.load(checkpoint_file)
        
        # Initialize network
        self.model = MuZeroNetwork(self.config)
        self.model.set_weights(self.checkpoint["weights"])
        self.model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        self.model.eval()
        
    def replicate_game(
        self, replicate_buffer: list
    ) -> None:
        """
        Play one game with actions based on the Monte Carlo tree search at each moves.
        """
        self.game_history = GameHistory()
        observation = self.game.reset()
        self.game_history.action_history.append(0)
        self.game_history.observation_history.append(observation)
        self.game_history.reward_history.append(0)
        self.game_history.to_play_history.append(self.game.to_play())

        with torch.no_grad():
            # Replicate previous actions from history
            for (action, root, player) in replicate_buffer:
                if self.done:
                    raise ValueError("Status is already 'done' but there still another step.")
                observation, reward, self.done = self.game.step(action)
                
                self.game_history.store_search_statistics(root, self.config.action_space)

                # Next batch
                self.game_history.action_history.append(action)
                self.game_history.observation_history.append(observation)
                self.game_history.reward_history.append(reward)
                self.game_history.to_play_history.append(self.game.to_play())
                
                assert(player == self.game.to_play()), f"Expected player number is wrong. Expected {player} but got {self.game.to_play()}"

    def add_action(
        self, opponent: str, temperature: float = 0, temperature_threshold: float = 0, human_action: int = None
    ) -> (int, str):
        with torch.no_grad():
            if self.done:
                raise ValueError("Status is already 'done' but there still another step.")
            if len(self.game_history.action_history) > self.config.max_moves:
                raise ValueError("Number of steps are already over the max moves.")

            stacked_observations = self.game_history.get_stacked_observations(
                -1,
                self.config.stacked_observations,
            )

            # Choose the action
            action = None
            if opponent == "self":
                root, mcts_info = MCTS(self.config).run(
                    self.model,
                    stacked_observations,
                    self.game.legal_actions(),
                    self.game.to_play(),
                    True,
                )
                action = SelfPlay.select_action(
                    root,
                    temperature
                    if not temperature_threshold
                    or len(self.game_history.action_history) < temperature_threshold
                    else 0,
                )
            elif opponent == "random":
                action, root = int(numpy.random.choice(self.game.legal_actions())), None
            elif opponent == "expert":
                action, root = self.game.expert_agent(), None
            elif opponent == "human":
                action, root = human_action, None
            else:
                raise ValueError(
                    'Wrong argument: "opponent" argument should be "self", "human", "expert" or "random"'
                )

            if action is None or not action in self.game.legal_actions():
                if (opponent == "human"):
                    raise ValueError(f"Requested action '{action}' is illegal in this game.")
                else:
                    raise Exception(f"Calculated action '{action}' by '{opponent}' is illegal in this game.")
            observation, reward, self.done = self.game.step(action)

            self.game_history.store_search_statistics(root, self.config.action_space)

            # Next batch
            self.game_history.action_history.append(action)
            self.game_history.observation_history.append(observation)
            self.game_history.reward_history.append(reward)
            self.game_history.to_play_history.append(self.game.to_play())

            return action, self.game.action_to_string(action)
    
    def get_history_buffer(self) -> list:
        return [
            (
                self.game_history.action_history[i],
                self.game_history.root_values[i - 1],
                self.game_history.to_play_history[i]
            ) for i in range(1, min(
                len(self.game_history.action_history), 
                len(self.game_history.root_values) + 1,
                len(self.game_history.to_play_history)
            ))
        ]
