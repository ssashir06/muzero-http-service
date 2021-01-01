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

## Build and run

1. `git clone https://github.com/ssashir06/muzero-http-service.git`
2. `cd muzero-http-service`
3. `git submodule init`
4. `git submodule update --remote`
5. `docker-compose up --build`

## Play Tic-Tac-Toe by using sample UI application

1. Open http://localhost:8888 to open a sample UI application.
2. Click the "Reset" button.
3. Click the "self" button to see the MuZero's action.
4. Click the "expert" or the "random" button to see another action.
5. Click a number at the "Actions:" label or a cell in the board to select human action. 

## Play Tic-Tac-Toe by using Swagger

1. Open http://localhost:8000/docs to see a page of Swagger.
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

This program uses tic-tac-toe's module in the [models](models) directory.
Another game's model can be used by adding or changing these things by editing [docker-compose.yml](docker-compose.yml) file.

- Environment variable
    - :point_right: `MODEL_PATH_tictactoe=./models/_for_test/tictactoe/model.checkpoint` in [docker-compose.yml](docker-compose.yml)
    - The checkpoint model file can be referenced by the program by this environment variable. 
    - A new environment variable having the format of `MODEL_PATH_{game_name}`.
