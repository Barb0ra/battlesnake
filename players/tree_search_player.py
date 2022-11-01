import random
from battlesnake.tree_search import SearchTree
from tree_search import monte_carlo_tree_search
from state_generator import next_state_for_action, transform_state
import time


class TreeSearchPlayer():
  def __init__(self, game_state):
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
#    print('turn ', game_state['turn'])
    game_state = transform_state(game_state)
    self.serach_tree.set_root_state(game_state)

    next_move = monte_carlo_tree_search(self.search_tree, timeout_start)
    #print(action_values, next_move)

    return {"move": next_move}

#state = {'height': 11, 'width': 11, 'food': {(6, 7), (9, 8), (6, 6), (1, 6), (1, 9)}, 'hazards': {(4, 0), (5, 4), (5, 1), (5, 7), (9, 5), (5, 10), (10, 0), (10, 6), (0, 5), (1, 0), (10, 9), (6, 5), (4, 5), (5, 0), (5, 6), (5, 3), (5, 9), (9, 10), (0, 1), (10, 5), (0, 4), (0, 10), (1, 5), (6, 10), (3, 5), (4, 10), (9, 0), (5, 5), (0, 0), (10, 4), (10, 1), (0, 9), (0, 6), (10, 10), (1, 10), (6, 0), (7, 5)}, 'snake_heads': [(2, 9), (2, 4)], 'snake_bodies': [[(2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (6, 9), (7, 9), (7, 10)], [(3, 4), (4, 4), (4, 3), (4, 2), (5, 2), (6, 2), (6, 1), (7, 1), (7, 2), (7, 3)]], 'snake_lengths': [9, 11], 'snake_healths': [95, 90]}
#state['snake_heads'][0], state['snake_heads'][1] = state['snake_heads'][1], state['snake_heads'][0]
#state['snake_bodies'][0], state['snake_bodies'][1] = state['snake_bodies'][1], state['snake_bodies'][0]
#state['snake_lengths'][0], state['snake_lengths'][1] = state['snake_lengths'][1], state['snake_lengths'][0]
#state['snake_healths'][0], state['snake_healths'][1] = state['snake_healths'][1], state['snake_healths'][0]
#
#player = TreeSearchPlayer()
#player.move(state)
#print(monte_carlo_tree_search(state, time.time()))
