from tree_search import SearchTree, monte_carlo_tree_search 
import time

state = {'height': 11, 'width': 11, 'food': {(8, 8), (0, 8), (10, 2), (2, 2)}, 'hazards': {(4, 0), (5, 4), (5, 1), (5, 7), (9, 5), (5, 10), (10, 0), (10, 6), (0, 5), (1, 0), (10, 9), (6, 5), (4, 5), (5, 0), (5, 6), (5, 3), (5, 9), (9, 10), (0, 1), (10, 5), (0, 4), (0, 10), (1, 5), (6, 10), (3, 5), (4, 10), (9, 0), (5, 5), (0, 0), (10, 4), (10, 1), (0, 9), (0, 6), (10, 10), (1, 10), (6, 0), (7, 5)}, 'snake_heads': [(1, 9), (9, 1), (4, 2), (9, 9)], 'snake_bodies': [[(1, 8), (1, 7)], [(9, 2), (9, 3)], [(4, 1), (3, 1)], [(9, 8), (9, 7)]], 'snake_lengths': [3, 3, 3, 3], 'snake_healths': [98, 98, 98, 98]}
#state['snake_heads'][0], state['snake_heads'][1] = state['snake_heads'][1], state['snake_heads'][0]
#state['snake_bodies'][0], state['snake_bodies'][1] = state['snake_bodies'][1], state['snake_bodies'][0]
#state['snake_lengths'][0], state['snake_lengths'][1] = state['snake_lengths'][1], state['snake_lengths'][0]
#state['snake_healths'][0], state['snake_healths'][1] = state['snake_healths'][1], state['snake_healths'][0]

search_tree = SearchTree()
search_tree.set_root_state(state)
print(monte_carlo_tree_search(search_tree, time.time()))