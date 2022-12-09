import numpy as np

from state_generator import next_state_for_action
from heuristic_baseline_functions.state_reward_heuristic import bfs_nearest_food, bfs_board_domination, bfs_accessible_area, is_dead, next_to_hazard, in_hazard

feature_weights = np.array([-1, 2, 2, 0, 0, -1, -15, -10, -20, -30])


def get_value(state, game_type, game_map, hazard_damage):
    feature_vector = compute_feature_vector(state, game_type, game_map, hazard_damage)
    mean = np.dot(feature_weights, feature_vector)
    # uncertainty of our estimate
    variance = 0.6**2
    return mean/1000, variance


def compute_feature_vector(state, game_type, game_map, hazard_damage):
    feature_vector = np.zeros(10)
    snake_bodies = get_snake_bodies(state)
    # distance to food
    feature_vector[0] = distance_to_food_when_hungry(state, snake_bodies, game_type, game_map, hazard_damage)
    # area control
    feature_vector[1] = bfs_board_domination(state, snake_bodies, game_type, game_map, hazard_damage)[0]
    # accessible area
    feature_vector[2] = bfs_accessible_area(state, snake_bodies, 0, game_type, game_map, hazard_damage)
    # absolute difference between my length and the longest snake + 1
    # because we always want to be biggest
    feature_vector[3] = absolute_difference_in_length(state)
    # my length
    feature_vector[4] = state['snake_lengths'][0]
    # average opponent accessible area
    feature_vector[5] = np.mean(list(bfs_accessible_area(state, snake_bodies, i, game_type, game_map, hazard_damage) for i in range(1, len(state['snake_heads']))))
    feature_vector[6] = next_to_hazard(state, game_type, game_map, hazard_damage)
    # hungry (health < 40)
    feature_vector[7] = snake_hungry(state)
    # very hungry (health < 20)
    feature_vector[8] = snake_very_hungry(state)
    # in hazard
    feature_vector[9] = in_hazard(state, game_type, game_map, hazard_damage)

    return feature_vector


def get_snake_bodies(state):
    snake_bodies = []
    for snake in state['snake_bodies']:
        snake_bodies += snake
    return snake_bodies


def distance_to_food_when_hungry(game_state, snake_bodies, game_type, game_map, hazard_damage):
    if game_state['snake_healths'][0] > 30:
        return 0
    my_head = game_state['snake_heads'][0]
    visited = set()
    distance = bfs_nearest_food(game_state, snake_bodies, game_type, game_map, hazard_damage)
    # return 0 is no food is reachable
    if distance:
        return distance
    else:
        return 0


def absolute_difference_in_length(state):
    if len(state['snake_lengths']) == 1:
        return 0
    return abs(state['snake_lengths'][0] - max(state['snake_lengths'][1:]) - 1)

def snake_hungry(state):
    if state['snake_healths'][0] < 40:
        return 1
    return 0

def snake_very_hungry(state):
    if state['snake_healths'][0] < 20:
        return 1
    return 0
