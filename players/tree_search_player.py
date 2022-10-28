import random
<<<<<<< HEAD
import threading

from tree_search import SearchTree
from tree_search import min_max_tree_search
from state_generator import next_state_for_action, transform_state
import time


class TreeSearchPlayer():
<<<<<<< HEAD
    def __init__(self):
        self.search_tree = SearchTree()
=======
from heuristic_baseline_functions.one_step_lookahead import sample_best_minmax_action
from state_generator import next_state_for_action, transform_state
from state_reward import state_reward


class OneStepLookaheadPlayer():

    def __init__(self):
        self.rewards = {
            'death': -1000,
            'death_by_head_collision': -700,
            'opponent_death': 100,
            'distance_to_food_when_hungry': -5,
            'distance_to_food_when_small': -1,
            'board_domination': 2
        }
>>>>>>> cc13b4f (Fix new tree search files)

    def info(self):
        return {
            "apiversion": "1",
            "author": "Barbora",
            "color": "#3352FF",
            "head": "default",  # TODO: Choose head
            "tail": "default",  # TODO: Choose tail
        }

    def move(self, game_state):
        # move is called on every turn and returns your next move
        # Valid moves are "up", "down", "left", or "right"
<<<<<<< HEAD
        timeout_start = time.time()
        timeout = 0.25
        print('turn ', game_state['turn'])
        game_state = transform_state(game_state)
        #print(f"game state: {game_state}")
        self.search_tree.set_root_state(game_state, timeout_start, timeout)
        action = min_max_tree_search(self.search_tree, timeout_start, timeout)

        return {"move": action}
=======

  def __init__(self):
    self.rewards = {
      'death': -1000,
      'death_by_head_collision': -700,
      'opponent_death': 100,
      'distance_to_food_when_hungry': -5,
      'distance_to_food_when_small': -1,
      'board_domination': 2
    }

  def info(self):
    return {
      "apiversion": "1",
      "author": "Barbora",
      "color": "#3352FF",
      "head": "default",  # TODO: Choose head
      "tail": "default",  # TODO: Choose tail
    }

  def move(self, game_state):
    # move is called on every turn and returns your next move
    # Valid moves are "up", "down", "left", or "right"

    print('turn ', game_state['turn'])
    print(game_state)
    game_state = transform_state(game_state)
    print(game_state)
    action_values = sample_best_minmax_action(game_state, self.rewards)

    next_move = sorted(action_values, key=action_values.get, reverse=True)[0]
    #print(action_values, next_move)

    return {"move": next_move}
>>>>>>> b1eb4a6 (Add reachable area heuristic)
=======

        print('turn ', game_state['turn'])
        print(game_state)
        game_state = transform_state(game_state)
        print(game_state)
        action_values = sample_best_minmax_action(game_state, self.rewards)

        next_move = sorted(
            action_values, key=action_values.get, reverse=True)[0]
        #print(action_values, next_move)

        return {"move": next_move}
>>>>>>> cc13b4f (Fix new tree search files)
