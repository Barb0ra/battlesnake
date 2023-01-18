import numpy as np
import joblib
from bayesian_snake_logic.state_generator import next_state_for_action
from heuristic_baseline_functions.state_reward_heuristic import bfs_nearest_food, bfs_board_domination, bfs_accessible_area, is_dead, next_to_hazard, in_hazard


def get_value(state, value_function):
    feature_vector = state.feature_vector
    if value_function == 'basic':
        return basic_value_function(feature_vector)
    else:
        # the value function is a Gaussian Process
        state_value = value_function.predict([feature_vector], return_std=True)
        return state_value[0][0], state_value[1][0]**2


def basic_value_function(feature_vector):
    feature_weights = np.array([2, 2, -3, -1, -3, 0])
    mean = np.dot(feature_weights, feature_vector)
    # uncertainty of our estimate
    variance = 0.6**2
    return mean/1000, variance


def compute_feature_vector(state, game_type, game_map, hazard_damage):
    feature_vector = np.zeros(6)
    snake_bodies = get_snake_bodies(state)
    # area control
    feature_vector[0] = bfs_board_domination(
        state, snake_bodies, game_type, game_map, hazard_damage)[0]
    # accessible area
    feature_vector[1] = bfs_accessible_area(
        state, snake_bodies, 0, game_type, game_map, hazard_damage)
    # absolute difference between my length and the longest snake + 1
    # because we always want to be bigger
    feature_vector[2] = absolute_difference_in_length(state)
    # average opponent accessible area
    feature_vector[3] = np.mean(list(bfs_accessible_area(
        state, snake_bodies, i, game_type, game_map, hazard_damage) for i in range(1, len(state['snake_heads']))))
    #feature_vector[6] = next_to_hazard(state, game_type, game_map, hazard_damage)
    # hungry (health < 40)
    feature_vector[4] = snake_hungry(state)
    # my length
    feature_vector[5] = state['snake_lengths'][0]

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
    distance = bfs_nearest_food(
        game_state, snake_bodies, game_type, game_map, hazard_damage)
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
