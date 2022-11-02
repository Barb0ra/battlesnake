import random
import threading

from tree_search import SearchTree
from tree_search import monte_carlo_tree_search
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
    #print('turn ', game_state['turn'])
    game_state = transform_state(game_state)
    self.search_tree.set_root_state(game_state)

    threading.Thread(target=monte_carlo_tree_search, args=(self.search_tree, timeout_start)).start()
    # next_move = monte_carlo_tree_search(self.search_tree, timeout_start)
    #print(action_values, next_move)
    while time.time() - timeout_start < 0.2:  
      pass
    
    return {"move": self.search_tree.root_state.max_action.action}
