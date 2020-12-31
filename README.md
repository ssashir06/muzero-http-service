# MuZero http service

## Purpose

This program is created to use MuZero's game steps by another program.
Mainly board games are supposed to be used.

## Notices

- This program provides http service to see MuZero's action.
- This program uses [MuZero General](https://github.com/werner-duvaud/muzero-general/)'s code in a submodule's directory.
- This program uses a code based on MuZero's one.
    - [self_play_replicate.py](src/self_play_replicate.py) is like self_play.py
  
# How to build and run

## Requirements

- Docker for Desktop

## Build

1. `git clone https://github.com/ssashir06/muzero-http-service.git`
2. `cd muzero-http-service`
3. `git submodule init`
4. `git submodule update --remote`
5. `docker-compose up --build`

## Run Tic-Tac-Toe's program

1. Open http://127.0.0.1:8000/docs to see a page of Swagger.
1. Try to use `/game/{game_name}`
    - :point_right: This method shows basic info for the specified game. It includes action_space and players data.
    1. Fill `game_name` as `tictactoe`
1. Try to use `/game/{game_name}/{seed}`
    - :point_right: This method shows the initial state of the game based on specified random seed.
    1. Fill `game_name` as `tictactoe`
    1. Fill `seed` as `1000`
1. Try to use `/game/{game_name}/{seed}/action` for the 1st game step
    - :point_right: This method creates a step for the game, and shows the step's result.
    1. Fill `game_name` as `tictactoe`
    1. Fill `seed` as `1000`
    1. Fill `opponent` as `self`
    1. Copy the `steps` in the `Response body` for the 2nd game step.

```json
[
  {
    "action": 3,
    "root": null,
    "next": 1
  }
]
```

5. Try to use `/game/{game_name}/{seed}/action` for the 2nd game step
    - :point_right: This method creates a step for the game, and shows the step's result.
    1. Fill `game_name` as `tictactoe`
    1. Fill `seed` as `1000`
    1. Fill `opponent` as `self`
    1. Paste `steps` of the 1st game step to the `Request body`

```json
{
  "steps": [
    {
      "action": 3,
      "root": null,
      "next": 1
    }
  ]
}
```

# Customize

This program uses the following things to use tic-tac-toe.
Another game can be used by adding or changing these things by editing [docker-compose.yml](docker-compose.yml) file.

- Checkpoint model file
    - :point_right: `./models/_for_test/tictactoe/model.checkpoint:/app/models/tictactoe/model.checkpoint`
    - The checkpoint model file is located by this config.
- Environment variable
    - :point_right: `MODEL_PATH_tictactoe=models/tictactoe/model.checkpoint`
    - The checkpoint model file can be referenced by the program by this config. 
    - The variable name is having the format of `MODEL_PATH_{game_name}`.
