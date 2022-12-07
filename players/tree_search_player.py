import random
import threading

from tree_search import SearchTree
from tree_search import min_max_tree_search
from state_generator import next_state_for_action, transform_state
import time


class TreeSearchPlayer():
    def __init__(self, params):
        self.search_tree = SearchTree()
        self.tree_min_depth = params[0]
        self.tree_max_depth = params[1]
        self.tree_iterations_per_depth = params[2]
        self.discounting_factor = params[3]
        self.mean_or_lcb = params[4]

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
        timeout_start = time.time()
        timeout = 0.25
        #print('turn ', game_state['turn'])
        game_state = transform_state(game_state)
        #print(f"game state: {game_state}")
        self.search_tree.set_root_state(game_state, timeout_start, timeout, self.mean_or_lcb)
        action = min_max_tree_search(self.search_tree, timeout_start, timeout, self.tree_min_depth, self.tree_max_depth, self.tree_iterations_per_depth, self.discounting_factor, self.mean_or_lcb)

        return {"move": action}
