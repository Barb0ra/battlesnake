# Bayesian Reinforcement Learning for Battlesnake run manual

## Launching Bayesian and Baseline players with different parameters
To launch a player server according to your needs, use the *run server* function in `server.py`. You will need to specify the following set of parameters:
* port number - the port number on which the server will be launched
* player name - which type of player you want to launch. The options are:
    * `tree_search_player` - the Bayesian player
    * `one_step_lookahead`
    * `heuristic`
    * `random`

* player parameters - a list of parameters for the player. If you are launching a baseline player, this list will be empty. For a Bayesian player, the parameters are:
    * minimum tree depth (int)
    * maximum tree depth (int)
    * number of tree iterations per depth (int)
    * discounting factor (float) between 0 and 1
    * action-picking strategy (string) - the options are `mean`, `lcb`, `lcb_ucb`
    * whether to log state values for learning (bool) - only use this is you are training a value function
    * value function - either write `basic` or specify the name of a GP model saved in `learning/value_functions/`

* game type - write `wrapped` or `standard`
* game map - write `islands_and_bridges` or `royale`
* hazard damage - the amount of damage that hazards do to the snake (int) - usually will be 100

## Simulating games locally

To simulate games locally, you will need to build a game engine file following these instructions: https://github.com/BattlesnakeOfficial/rules.

Once you have the game engine file, you can pass its location as an argument to `run_games` in `learning/run_games.py`. The other parameters will allow you to decide how many games to simulate and which players to use. The players are specified in a dictionary format such as:

``` python
snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [7, 7, 50, 0.9, 'mean', False, 'basic']}, 
          {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]

```