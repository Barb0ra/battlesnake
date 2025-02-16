import itertools
import copy
import numpy as np
from bayesian_snake_logic.RL_value_function import compute_feature_vector, get_value
from bayesian_snake_logic.RL_state_reward import is_dead, state_reward
from bayesian_snake_logic.state_generator import get_likely_moves, cleanup_state, next_state_for_action
import time


def generate_possible_states(game_state, my_action, timeout_start, timeout, game_type, game_map, hazard_damage):
    # returns an array of possible states
    possible_states = []
    opponents_left = len(game_state['snake_heads']) - 1
    if opponents_left < 0:
        opponents_left = 0
    likely_opponent_moves = []
    for opponent in range(opponents_left):
        likely_opponent_moves.append(
            get_likely_moves(game_state, opponent + 1, game_type, game_map, hazard_damage))
    move_combinations = list(itertools.product(*likely_opponent_moves))
    # how the board changes when I move
    my_next_state = next_state_for_action(
        game_state, 0, my_action, game_type, game_map, hazard_damage)
    # how the board changes when everyone else moves
    for move_combination in move_combinations:
        next_state = my_next_state
        for snake_index, move in enumerate(move_combination):
            next_state = next_state_for_action(
                next_state, snake_index + 1, move, game_type, game_map, hazard_damage)
        possible_states.append(next_state)
        # this operation is time consuming if there are many possible move combinations
        # we need to check if we are running out of time
        if time.time() > timeout_start + timeout:
            break
    return possible_states


def equal_states(state1, state2):
    if state1['snake_heads'] != state2['snake_heads']:
        return False
    if state1['snake_bodies'] != state2['snake_bodies']:
        return False
    if state1['food'] != state2['food']:
        return False
    if state1['hazards'] != state2['hazards']:
        return False
    return True


class SearchTree:
    def __init__(self):
        self.root_state = None

    def set_root_state(self, game_state, timeout_start, timeout, mean_or_lcb, game_type, game_map, hazard_damage, value_function):
        if self.root_state == None or game_map == 'royale':
            self.root_state = StateNode(
                game_state, game_type, game_map, hazard_damage, value_function)
            self.root_state.generate_actions(
                timeout_start, timeout, game_type, game_map, hazard_damage, value_function)
        else:
            existing_state = False
            for state in self.root_state.get_max_action(timeout_start, timeout, mean_or_lcb, game_type, game_map, hazard_damage, value_function).states:
                if equal_states(state.game_state, game_state):
                    self.root_state = state
                    self.root_state.game_state = game_state
                    # increase the turn number in feature vector
                    self.root_state.feature_vector[-1] += 1
                    existing_state = True
                    break
            if not existing_state:
                self.root_state = StateNode(
                    game_state, game_type, game_map, hazard_damage, value_function)
                self.root_state.generate_actions(
                    timeout_start, timeout, game_type, game_map, hazard_damage, value_function)


class ActionNode:

    def __init__(self, parent, action, timeout_start, timeout, game_type, game_map, hazard_damage, value_function):
        self.parent_state = parent
        self.action = action
        self.states = self.generate_state_nodes(
            parent.game_state, action, timeout_start, timeout, game_type, game_map, hazard_damage, value_function)

    def sample_min_state(self):
        min = None
        min_state = None
        for state in self.states:
            sample_value = state.get_sample_value()
            # or in a non-bayesian case
            #sample_value = state.mean
            if min == None or sample_value < min:
                min = sample_value
                min_state = state
        return sample_value, min_state

    def get_state_with_min_mean(self):
        # this can be used to pick the final action
        min = None
        min_state = None
        for state in self.states:
            value = state.mean
            if min == None or value < min:
                min = value
                min_state = state
        return min, min_state

    def get_state_with_min_lcb(self):
        min_lcb = None
        min_state = None
        min_ucb = None
        all_lcbs = []
        for state in self.states:
            value = state.mean - 2*(state.variance)**0.5
            all_lcbs.append(value)
            if min_lcb == None or value < min_lcb:
                min_lcb = value
                min_state = state
                min_ucb = state.mean + 2*(state.variance)**0.5
        return min_lcb, min_ucb, min_state

    def generate_state_nodes(self, parent_state, action, timeout_start, timeout, game_type, game_map, hazard_damage, value_function):
        states = generate_possible_states(
            parent_state, action, timeout_start, timeout, game_type, game_map, hazard_damage)
        return [StateNode(state, game_type, game_map, hazard_damage, value_function, self) for state in states]


class StateNode:

    def __init__(self, game_state, game_type, game_map, hazard_damage, value_function, parent=None):
        self.n_visited = 1
        self.parent_action = parent
        self.reward = state_reward(
            game_state, game_type, game_map, hazard_damage)
        # gamma's shape parameter
        self.alpha = 1
        self.terminal = self.terminal(
            game_state, game_type, game_map, hazard_damage)
        self.feature_vector = compute_feature_vector(
            game_state, game_type, game_map, hazard_damage)

        if self.terminal:
            self.mean = self.reward
            self.variance = 0
            self.beta = 0
        else:
            mean, variance = get_value(self, value_function)
            self.mean = mean + self.reward
            self.variance = variance
            self.beta = variance
        self.game_state = cleanup_state(
            game_state, game_type, game_map, hazard_damage)
        self.actions = []

    def terminal(self, game_state, game_type, game_map, hazard_damage):
        return len(game_state['snake_heads']) <= 1 or is_dead(game_state, 0, game_type, game_map, hazard_damage)[0] or (len(game_state['snake_heads']) <= 2 and is_dead(game_state, 1, game_type, game_map, hazard_damage)[0])

    def generate_actions(self, timeout_start, timeout, game_type, game_map, hazard_damage, value_function):
        if len(self.actions) == 0:
            for action in get_likely_moves(self.game_state, 0, game_type, game_map, hazard_damage):
                self.actions.append(ActionNode(
                    self, action, timeout_start, timeout, game_type, game_map, hazard_damage, value_function))

    def update_value(self, observation):
        self.mean = (observation + self.mean*self.n_visited) / \
            (self.n_visited+1)
        self.beta += 0.5 * self.n_visited / \
            (self.n_visited+1) * (observation - self.mean)**2
        self.n_visited += 1
        self.alpha += 0.5
        self.variance = self.beta / (self.alpha + 1)

    def get_sample_value(self):
        return np.random.normal(self.mean, np.sqrt(self.variance))

    def sample_max_action(self, timeout_start, timeout, game_type, game_map, hazard_damage, value_function):
        max_value = None
        max_action = None
        min_state_for_max_action = None
        # if actions are not generated, generate them
        if len(self.actions) == 0:
            self.generate_actions(
                timeout_start, timeout, game_type, game_map, hazard_damage, value_function)
        for action in self.actions:
            state_sample_value, min_state = action.sample_min_state()

            if max_action == None or state_sample_value > max_value:
                max_value = state_sample_value
                max_action = action
                min_state_for_max_action = min_state
        return max_action, min_state_for_max_action

    def get_max_action(self, timeout_start, timeout, mean_or_lcb, game_type, game_map, hazard_damage, value_function):
        # get action with the highest min state mean value (deterministic)
        # can be used to make a final decisionon about what action to take
        max_value = None
        max_action = None
        # if actions are not generated, generate them
        if len(self.actions) == 0:
            self.generate_actions(
                timeout_start, timeout, game_type, game_map, hazard_damage, value_function)
        for action in self.actions:
            if mean_or_lcb == 'mean':
                state_val, min_state = action.get_state_with_min_mean()
            elif mean_or_lcb == 'lcb' or mean_or_lcb == 'lcb-ucb':
                state_min_lcb, state_min_ucb, min_state = action.get_state_with_min_lcb()
                if mean_or_lcb == 'lcb':
                    state_val = state_min_lcb
                elif mean_or_lcb == 'lcb-ucb':
                    state_val = state_min_ucb

            if max_action == None or state_val > max_value:
                max_value = state_val
                max_action = action
        return max_action


def min_max_tree_search(search_tree, timeout_start, timeout, tree_min_depth, tree_max_depth, tree_iterations_per_depth, discounting_factor, mean_or_lcb, game_type, game_map, hazard_damage, log_state_values, value_function):
    root_state = search_tree.root_state
    depth = tree_min_depth
    iteration_counter = 0

    while time.time() < timeout_start + timeout and depth <= tree_max_depth:
        max_action, min_state = root_state.sample_max_action(
            timeout_start, timeout, game_type, game_map, hazard_damage, value_function)
        update_state_nodes(min_state, depth-1, discounting_factor,
                           0, timeout_start, timeout, game_type, game_map, hazard_damage, value_function)
        iteration_counter += 1
        if iteration_counter >= tree_iterations_per_depth:
            iteration_counter = 0
            depth += 1

    if log_state_values:
        log_state_value(root_state)
    action = root_state.get_max_action(
        timeout_start, timeout, mean_or_lcb, game_type, game_map, hazard_damage, value_function).action
    return action


def update_state_nodes(state, depth, alpha, accumulated_reward, timeout_start, timeout, game_type, game_map, hazard_damage, value_function):
    if depth == 0 or state.terminal or time.time() > timeout_start + timeout:
        return state.get_sample_value() + accumulated_reward
    max_action, min_state = state.sample_max_action(
        timeout_start, timeout, game_type, game_map, hazard_damage, value_function)
    min_state_value = update_state_nodes(
        min_state, depth - 1, alpha, accumulated_reward + state.reward, timeout_start, timeout, game_type, game_map, hazard_damage, value_function)
    state.update_value(min_state_value)
    return min_state_value * alpha


def log_state_value(state):
    # log state values to file that will later be used for value function learning
    # format: state_features, state_mean, state_reward
    with open('learning/state_values.txt', 'a') as f:
        f.write(str(list(state.feature_vector))[
                1:-1] + ', ' + str(state.mean) + ', ' + str(state.reward) + '\n')
