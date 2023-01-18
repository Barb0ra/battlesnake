import random
import threading
import joblib
import time

from players.one_step_lookahead_player import OneStepLookaheadPlayer
from bayesian_snake_logic.tree_search import SearchTree
from bayesian_snake_logic.tree_search import min_max_tree_search
from bayesian_snake_logic.state_generator import next_state_for_action, transform_state



class TreeSearchPlayer():
    def __init__(self, params, game_type, game_map, hazard_damage):
        self.search_tree = SearchTree()
        self.tree_min_depth = params[0]
        self.tree_max_depth = params[1]
        self.tree_iterations_per_depth = params[2]
        self.discounting_factor = params[3]
        self.mean_or_lcb = params[4]
        self.game_type = game_type
        self.game_map = game_map
        self.hazard_damage = hazard_damage
        self.log_state_values = params[5]
        # load value function
        if params[6] == 'basic':
            self.value_fucntion = 'basic'
        else:
            self.value_fucntion = joblib.load('learning/value_functions/' + params[6])

    def info(self):
        return {
            "apiversion": "1",
            "author": "Barbora",
            "color": "#3352FF",
            "head": "smart-caterpillar",
            "tail": "replit-notmark",
        }

    def move(self, game_state):
        # move is called on every turn and returns your next move
        # Valid moves are "up", "down", "left", or "right"
        timeout_start = time.time()
        timeout = 0.4
        game_state = transform_state(
            game_state, self.game_type, self.game_map, self.hazard_damage)
        self.search_tree.set_root_state(game_state, timeout_start, timeout,
                                        self.mean_or_lcb, self.game_type, self.game_map, self.hazard_damage, self.value_fucntion)
        action = min_max_tree_search(self.search_tree, timeout_start, timeout, self.tree_min_depth, self.tree_max_depth,
                                     self.tree_iterations_per_depth, self.discounting_factor, self.mean_or_lcb, self.game_type, self.game_map, self.hazard_damage, self.log_state_values, self.value_fucntion)
        return {"move": action}
