import random
import threading

from tree_search import SearchTree
from tree_search import min_max_tree_search
from state_generator import next_state_for_action, transform_state
import time


class TreeSearchPlayer():
    def __init__(self):
        self.search_tree = SearchTree()

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
        timeout = 0.2
        print('turn ', game_state['turn'])
        game_state = transform_state(game_state)
        #print(f"game state: {game_state}")
        self.search_tree.set_root_state(game_state, timeout_start, timeout)
        action = min_max_tree_search(self.search_tree, timeout_start, timeout)

        return {"move": action}
