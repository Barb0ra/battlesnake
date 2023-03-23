# Bayesian Reinforcement Learning for Battlesnake
Welcome to Barbora's level 4 project about Bayesian Reinforcement Learning for Battlesnake!

Find out more about Battlesnake at https://play.battlesnake.com/

This repository contains code for a Battlesnake AI that uses Bayesian Reinforcement Learning to learn the best strategy for the game. Using the provided infrastructure, you can host a battlesnake server, simulate games locally using diffent baseline player combinations, run experiments, and train a new value function.

## Directory structure

* `bayesian_snake_logic/` - contains the code necessary for the Bayesian player, such as the tree search, the value function, the future state generator, and feature computation.
* `heuristic_baseline_function/` - contains the logic necessary to make the baseline players work.
* `players/` - contains the classes for the different players. There are four different baseline players (refer to the dissertation for a description of each), and the Bayesian player in `tree_search_player.py`.
* `server.py` - is the Flask server used when launching battlesnake players.
* `learning/` - contains everything assonciated with local game simulation and value function training. It also contains the best trained model (Gaussian process with a linear kernel) for the value function.

## Run instructions

To launch a Bayesian player with the best possible parameters and value function on http://localhost:8000, simply run `python main.py`. The server will load the GP value function and be ready to receive requests.

For detailed information of how to change parameter values, launch baseline players, and simulate games, refer to `manual.md`



## Requirements

```
* Python 3.7
* Packages: listed in `requirements.txt` 
* go 1.10.7 (if you want to simulate games locally)
```

