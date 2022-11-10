import numpy as np

from state_generator import next_state_for_action

feature_weights = np.array([0, 2, 3, -0.5, -0.5, 0])


def get_value(state):
    feature_vector = compute_feature_vector(state)
    value = np.dot(feature_weights, feature_vector)

    return (value)


def compute_feature_vector(state):
    feature_vector = np.zeros(6)
    snake_bodies = get_snake_bodies(state)
    # distance to food
    feature_vector[0] = distance_to_food_when_hungry(state, snake_bodies)
    # area control
    feature_vector[1] = bfs_board_area_control(state, snake_bodies)
    # accessible area
    feature_vector[2] = bfs_accessible_area(state, snake_bodies)
    # absolute difference between my length and the longest snake + 1
    # because we always want to be biggest
    feature_vector[3] = absolute_difference_in_length(state)
    # my length
    feature_vector[4] = state['snake_lengths'][0]
    feature_vector[5] = snake_hungry(state)
    print(feature_vector)
    return feature_vector


def get_snake_bodies(state):
    snake_bodies = []
    for snake in state['snake_bodies']:
        snake_bodies += snake
    return snake_bodies


def distance_to_food_when_hungry(game_state, snake_bodies):
    if game_state['snake_healths'][0] > 20:
        return 0
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
        key=lambda k: (game_state['snake_lengths'][k], 0 if k == 0 else 1),
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
    if len(state['snake_lengths']) == 1:
        return 0
    return abs(state['snake_lengths'][0] - max(state['snake_lengths'][1:]) - 1)

def snake_hungry(state):
    if state['snake_healths'][0] < 20:
        return 20 - state['snake_healths'][0]
    return 0
