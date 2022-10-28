import random
from battlesnake.tree_search import monte_carlo_tree_search
from tree_search import sample_best_minmax_action
from state_generator import next_state_for_action, transform_state


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

    print('turn ', game_state['turn'])
    game_state = transform_state(game_state)

    next_move = monte_carlo_tree_search(game_state)
    #print(action_values, next_move)

    return {"move": next_move}
