import numpy as np

from state_generator import next_state_for_action

feature_weights = np.array([-1, 2, 2, -1])

def get_value(state):
    feature_vector = compute_feature_vector(state)
    mean = np.dot(feature_weights, feature_vector) # primitive normalisation method
    return (mean)

def compute_feature_vector(state):
    feature_vector = np.zeros(4)
    snake_bodies = get_snake_bodies(state)
    # distance to food
    feature_vector[0] = distance_to_food(state, snake_bodies)
    # area control
    feature_vector[1] = bfs_board_area_control(state, snake_bodies)
    # accessible area
    feature_vector[2] = bfs_accessible_area(state, snake_bodies)
    # absolute difference between my length and the longest snake + 1
    # because we always want to be biggest
    feature_vector[3] = absolute_difference_in_length(state)
    return feature_vector

def get_snake_bodies(state):
    snake_bodies = []
    for snake in state['snake_bodies']:
        snake_bodies += snake
    return snake_bodies

def distance_to_food(game_state, snake_bodies):
    my_head = game_state['snake_heads'][0]
    visited = set()
    queue = []
    if my_head not in snake_bodies and my_head not in game_state['hazards'] and my_head not in game_state['snake_heads'][1:]:
        queue.append((my_head, 0))
        visited.add(my_head)
    while queue != []:
        current_node, distance = queue.pop(0)
        if current_node in game_state['food']:
            return distance
        for neighbor in get_neighbors(current_node, game_state, snake_bodies):
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
                visited.add(neighbor)
    # return 0 is no food is reachable
    return 0

def bfs_board_area_control(game_state, snake_bodies):
    snake_area_control = {}
    snake_queues = {}
    visited = set()
    # sort snakes by length and put me last if it's a tie
    snake_indices_by_length = sorted(
        range(len(game_state['snake_lengths'])),
        key=lambda k: (game_state['snake_lengths'][k], 0 if k==0 else 1),
        reverse=True)
    for snake_index in snake_indices_by_length:
        snake_head = game_state['snake_heads'][snake_index]
        snake_area_control[snake_index] = 0
        snake_queues[snake_index] = []
        if snake_head not in snake_bodies and snake_head not in game_state['hazards'] and snake_head not in game_state['snake_heads'][snake_index+1:] and snake_head not in game_state['snake_heads'][:snake_index]:
            snake_queues[snake_index].append((snake_head, 0))
            visited.add(snake_head)
    
    while non_empty(snake_queues):
        for snake_index in snake_indices_by_length:
            queue = snake_queues[snake_index]
            if queue != []:
                current_node, area_control = queue.pop(0)
                for neighbor in get_neighbors(current_node, game_state, snake_bodies):
                    if neighbor not in visited:
                        snake_queues[snake_index].append((neighbor, 0))
                        visited.add(neighbor)
                        snake_area_control[snake_index] += 1
    
    return snake_area_control[0]


def bfs_accessible_area(game_state, snake_bodies):
    my_head = game_state['snake_heads'][0]
    visited = set()
    area = 0
    queue = []
    if my_head not in snake_bodies and my_head not in game_state['hazards'] and my_head not in game_state['snake_heads'][1:]:
        queue.append((my_head))
        visited.add(my_head)
        area += 1
    else:
        return area
    while queue != []:
        current_node = queue.pop(0)
        for neighbor in get_neighbors(current_node, game_state, snake_bodies):
            if neighbor not in visited:
                queue.append((neighbor))
                visited.add(neighbor)
                area += 1
    return area

def non_empty(snake_queues):
    for queue in snake_queues.values():
        if queue:
            return True
    return False

def get_neighbors(current_node, game_state, snake_bodies):
    potential_neighbors = []
    neighbors = []
    height = game_state['height']
    width = game_state['width']
    x, y = current_node
    potential_neighbors.append(((x + 1) % width, y))
    potential_neighbors.append(((x - 1) % width, y))
    potential_neighbors.append((x, (y + 1) % height))
    potential_neighbors.append((x, (y - 1) % height))
    for neighbor in potential_neighbors:
        if neighbor not in game_state['hazards'] and neighbor not in snake_bodies and neighbor not in game_state['snake_heads']:
            neighbors.append(neighbor)
    return neighbors

def absolute_difference_in_length(state):
    return abs(state['snake_lengths'][0] - max(state['snake_lengths'][1:]) - 1)

state = {'height': 11, 'width': 11, 'food': {(7, 4), (4, 6), (6, 9), (7, 3)}, 'hazards': {(4, 0), (5, 4), (5, 1), (5, 7), (9, 5), (5, 10), (10, 0), (10, 6), (0, 5), (1, 0), (10, 9), (6, 5), (4, 5), (5, 0), (5, 6), (5, 3), (5, 9), (9, 10), (0, 1), (10, 5), (0, 4), (0, 10), (1, 5), (6, 10), (3, 5), (4, 10), (9, 0), (5, 5), (0, 0), (10, 4), (10, 1), (0, 9), (0, 6), (10, 10), (1, 10), (6, 0), (7, 5)}, 'snake_heads': [(8, 4), (8, 6)], 'snake_bodies': [[(9, 4), (9, 3), (9, 2), (10, 2), (10, 3), (0, 3), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 3), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (7, 1), (7, 0), (7, 10), (8, 10), (8, 0), (8, 1)], [(8, 7), (8, 8), (8, 9), (9, 9), (9, 8), (10, 8), (0, 8), (1, 8), (2, 8), (2, 9), (2, 10), (2, 0), (2, 1), (3, 1), (3, 0), (3, 10), (3, 9), (4, 9)]], 'snake_lengths': [25, 19], 'snake_healths': [86, 84]}
state = next_state_for_action(state, 0, 'right')
print(get_value(state))