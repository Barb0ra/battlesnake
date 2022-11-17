from players.tree_search_player import TreeSearchPlayer
from tree_search import SearchTree, min_max_tree_search 
import time

state1 = {'game': {'id': '1e217008-ba0d-4915-b975-7850deb78aa9', 'ruleset': {'name': 'wrapped', 'version': 'v1.1.20', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 100, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'hz_islands_bridges', 'timeout': 500, 'source': 'custom'}, 'turn': 71, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_rqVKtggmctpJk3qpKgY7Qd9R', 'name': 'Bayesian snake', 'latency': '377', 'health': 82, 'body': [{'x': 4, 'y': 8}, {'x': 4, 'y': 9}, {'x': 3, 'y': 9}, {'x': 3, 'y': 10}, {'x': 2, 'y': 10}, {'x': 2, 'y': 0}, {'x': 2, 'y': 1}, {'x': 2, 'y': 2}], 'head': {'x': 4, 'y': 8}, 'length': 8, 'shout': '', 'squad': '', 'customizations': {'color': '#3352ff', 'head': 'default', 'tail': 'default'}}, {'id': 'gs_MD3hSbtS8Fqm48qSCrF9dKSc', 'name': 'Baseline Snake', 'latency': '149', 'health': 99, 'body': [{'x': 1, 'y': 8}, {'x': 1, 'y': 9}, {'x': 2, 'y': 9}, {'x': 2, 'y': 8}, {'x': 2, 'y': 7}, {'x': 2, 'y': 6}], 'head': {'x': 1, 'y': 8}, 'length': 6, 'shout': '', 'squad': '', 'customizations': {'color': '#3352ff', 'head': 'default', 'tail': 'default'}}], 'food': [{'x': 10, 'y': 3}, {'x': 7, 'y': 4}, {'x': 3, 'y': 7}, {'x': 9, 'y': 4}], 'hazards': [{'x': 5, 'y': 10}, {'x': 5, 'y': 9}, {'x': 5, 'y': 7}, {'x': 5, 'y': 6}, {'x': 5, 'y': 5}, {'x': 5, 'y': 4}, {'x': 5, 'y': 3}, {'x': 5, 'y': 0}, {'x': 5, 'y': 1}, {'x': 6, 'y': 5}, {'x': 7, 'y': 5}, {'x': 9, 'y': 5}, {'x': 10, 'y': 5}, {'x': 4, 'y': 5}, {'x': 3, 'y': 5}, {'x': 1, 'y': 5}, {'x': 0, 'y': 5}, {'x': 1, 'y': 10}, {'x': 9, 'y': 10}, {'x': 1, 'y': 0}, {'x': 9, 'y': 0}, {'x': 10, 'y': 1}, {'x': 10, 'y': 0}, {'x': 10, 'y': 10}, {'x': 10, 'y': 9}, {'x': 0, 'y': 10}, {'x': 0, 'y': 9}, {'x': 0, 'y': 1}, {'x': 0, 'y': 0}, {'x': 0, 'y': 6}, {'x': 0, 'y': 4}, {'x': 10, 'y': 6}, {'x': 10, 'y': 4}, {'x': 6, 'y': 10}, {'x': 4, 'y': 10}, {'x': 6, 'y': 0}, {'x': 4, 'y': 0}]}, 'you': {'id': 'gs_MD3hSbtS8Fqm48qSCrF9dKSc', 'name': 'Baseline Snake', 'latency': '149', 'health': 99, 'body': [{'x': 1, 'y': 8}, {'x': 1, 'y': 9}, {'x': 2, 'y': 9}, {'x': 2, 'y': 8}, {'x': 2, 'y': 7}, {'x': 2, 'y': 6}], 'head': {'x': 1, 'y': 8}, 'length': 6, 'shout': '', 'squad': '', 'customizations': {'color': '#3352ff', 'head': 'default', 'tail': 'default'}}}
state1['you'] = state1['board']['snakes'][0]


#state['snake_heads'][0], state['snake_heads'][1] = state['snake_heads'][1], state['snake_heads'][0]
#state['snake_bodies'][0], state['snake_bodies'][1] = state['snake_bodies'][1], state['snake_bodies'][0]
#state['snake_lengths'][0], state['snake_lengths'][1] = state['snake_lengths'][1], state['snake_lengths'][0]
#state['snake_healths'][0], state['snake_healths'][1] = state['snake_healths'][1], state['snake_healths'][0]

player = TreeSearchPlayer()

print(player.move(state1))
#print(player.move(state2))
#search_tree = SearchTree()
#search_tree.set_root_state(state)
#print(min_max_tree_search(search_tree, time.time()))