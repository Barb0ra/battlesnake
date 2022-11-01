import random
from tree_search import monte_carlo_tree_search
from state_generator import next_state_for_action, transform_state
import time


class TreeSearchPlayer():

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
#    print('turn ', game_state['turn'])
    game_state = transform_state(game_state)

    next_move = monte_carlo_tree_search(game_state, timeout_start)
    #print(action_values, next_move)

    return {"move": next_move}
