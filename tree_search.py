import itertools
import copy
import numpy as np
from RL_value_function import get_value
from RL_state_reward import is_dead, state_reward
from state_generator import cleanup_state
from state_generator import next_state_for_action


def sample_best_minmax_action(game_state):
    actions = ['up', 'down', 'left', 'right']
    action_values = {}
    state_values = []
    for action in actions:
        possible_states = generate_possible_states(game_state, action)
        for state in possible_states:
            # sample from the value function
            state_values.append(get_value(state))
        action_values[action] = min(state_values)

    return action_values


def generate_possible_states(game_state, my_action):
    # returns an array of possible states
    actions = ['up', 'down', 'left', 'right']
    possible_states = []
    move_combinations = itertools.combinations_with_replacement(
        actions,
        len(game_state['snake_heads'])-1)
    # how the board changes when I move
    my_next_state = next_state_for_action(game_state, 0, my_action)
    # how the board changes when everyone else moves
    for move_combination in move_combinations:
        next_state = my_next_state
        for snake_index, move in enumerate(
                move_combination):
            next_state = next_state_for_action(next_state, snake_index+1,
                                               move)
        possible_states.append(next_state)
    return possible_states


class ActionNode:
    def __init__(self, parent, action):
        self.parent_state = parent
        self.action = action
        self.states = self.generate_state_nodes(parent.game_state, action)

    def get_min_state(self):
        min = None
        min_state = None
        for state in self.states:
            if min == None or state.value < min:
                min = state.value
                min_state = state
        return min_state

    def generate_state_nodes(self, parent_state, action):
        states = generate_possible_states(parent_state, action)
        return [StateNode(state, self) for state in states]


class StateNode:
    def __init__(self, game_state, parent=None):
        self.n_visited = 1
        self.parent_action = parent
        self.value = get_value(game_state)
        self.reward = state_reward(game_state)*1000
        self.terminal = is_dead(game_state, 0) or len(
            game_state['snake_heads']) == 1
        self.game_state = cleanup_state(game_state)
        self.actions = []

    def generate_actions(self):
        for action in ['up', 'down', 'left', 'right']:
            self.actions.append(ActionNode(self, action))

    def update_value(self, value):
        self.n_visited += 1
        self.value = (self.value * (self.n_visited - 1) +
                      value) / self.n_visited

    def get_max_action(self):
        max_value = None
        max_action = None
        # if actions are not generated, generate them
        if len(self.actions) == 0:
            self.generate_actions()

        for action in self.actions:
            if max_action == None or action.get_min_state().value > max_value:
                max_value = action.get_min_state().value
                max_action = action
        return max_action


def monte_carlo_tree_search(game_state):
    # iterative deepening
    root_state = StateNode(game_state)
    max_depth = 5
    each_depth_iteration = 1
    for i in range(each_depth_iteration):
        for depth in range(1, max_depth):
            # print action values
            #          for action in root_state.actions:
            #              print(action.action, action.get_min_state().value, action.get_min_state().reward)
            leaf_state, accumulated_reward = traverse(root_state, depth)
            simulation_result = get_simulation_result(
                leaf_state) + accumulated_reward
            backpropagate(leaf_state, simulation_result)
    return root_state.get_max_action().action


def get_simulation_result(leaf_state):
    return 0 if leaf_state.terminal else leaf_state.value

# function for state traversal


def traverse(state, depth):
    accumulated_reward = 0
    while depth > 0 and state.terminal == False:
        depth -= 1
        state = state.get_max_action().get_min_state()
        accumulated_reward += state.reward
    accumulated_reward += state.reward
    return state, accumulated_reward

# function for backpropagation


def backpropagate(state, result):
    state.update_value(result)
    result -= state.reward

    if state.parent_action == None:
        return
    backpropagate(state.parent_action.parent_state, result)


state = {'height': 11, 'width': 11, 'food': {(1, 1), (3, 8), (4, 6), (0, 3)}, 'hazards': {(4, 0), (5, 4), (5, 1), (5, 7), (9, 5), (5, 10), (10, 0), (10, 6), (0, 5), (1, 0), (10, 9), (6, 5), (4, 5), (5, 0), (5, 6), (5, 3), (5, 9), (9, 10), (0, 1), (10, 5), (0, 4), (0, 10), (1, 5), (6, 10), (3, 5), (4, 10), (9, 0), (5, 5), (0, 0), (10, 4), (10, 1), (0, 9), (
    0, 6), (10, 10), (1, 10), (6, 0), (7, 5)}, 'snake_heads': [(10, 2), (2, 2), (5, 8)], 'snake_bodies': [[(10, 3), (9, 3), (8, 3), (8, 4), (7, 4), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2)], [(3, 2), (3, 1), (3, 0), (3, 10), (3, 9), (2, 9), (2, 8), (1, 8), (0, 8)], [(6, 8), (7, 8), (8, 8), (8, 9), (8, 10)]], 'snake_lengths': [11, 10, 6], 'snake_healths': [86, 84, 38]}
print(monte_carlo_tree_search(state))
