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
    opponents_left = len(game_state['snake_heads']) - 1
    if opponents_left < 0:
        opponents_left = 0
    move_combinations = itertools.combinations_with_replacement(
        actions, opponents_left)
    # how the board changes when I move
    my_next_state = next_state_for_action(game_state, 0, my_action)
    # how the board changes when everyone else moves
    for move_combination in move_combinations:
        next_state = my_next_state
        for snake_index, move in enumerate(move_combination):
            next_state = next_state_for_action(
                next_state, snake_index + 1, move)
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
            if min == None or state.value + state.reward < min:
                min = state.value + state.reward
                min_state = state
        return min_state

    def generate_state_nodes(self, parent_state, action):
        states = generate_possible_states(parent_state, action)
        return [StateNode(state, self) for state in states]


class StateNode:

    def __init__(self, game_state, parent=None):
        self.n_visited = 1
        self.parent_action = parent
        self.reward = state_reward(game_state) * 1000
        self.value = get_value(game_state)
        self.terminal = is_dead(game_state,
                                0)[0] or (len(game_state['snake_heads']) <= 2 and is_dead(game_state, 1)[0])
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
            min_state = action.get_min_state()
            if max_action == None or min_state.value + min_state.reward > max_value:
                max_value = min_state.value + min_state.reward
                max_action = action
        return max_action


def monte_carlo_tree_search(game_state):
    # iterative deepening
    root_state = StateNode(game_state)
    root_state.generate_actions()
    max_depth = 6 - len(game_state['snake_heads'])
    # discounting factor
    alpha = 0.6
    each_depth_iteration = 1
    for i in range(each_depth_iteration):
        for depth in range(1, max_depth + 1):
            leaf_state, accumulated_reward = traverse(root_state, max_depth)
            simulation_result = get_simulation_result(
                leaf_state) + accumulated_reward
            backpropagate(leaf_state, simulation_result, alpha)
            #for action in root_state.actions:
            #    print(action.action, action.get_min_state().value,
            #          action.get_min_state().reward)
    # print action values

    return root_state.get_max_action().action


def get_simulation_result(leaf_state):
    return leaf_state.value


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


def backpropagate(state, result, alpha):
    state.update_value(result)
    result = result * alpha
    if state.parent_action == None:
        return
    backpropagate(state.parent_action.parent_state, result, alpha)


#state = {'height': 11, 'width': 11, 'food': {(1, 6), (10, 8)}, 'hazards': {(4, 0), (5, 4), (5, 1), (5, 7), (9, 5), (5, 10), (10, 0), (10, 6), (0, 5), (1, 0), (10, 9), (6, 5), (4, 5), (5, 0), (5, 6), (5, 3), (5, 9), (9, 10), (0, 1), (10, 5), (0, 4), (0, 10), (1, 5), (6, 10), (3, 5), (4, 10), (9, 0), (5, 5), (0, 0), (10, 4), (10, 1), (0, 9), (0, 6), (10, 10), (1, 10), (6, 0), (7, 5)}, 'snake_heads': [(2, 9), (9, 7)], 'snake_bodies': [[(3, 9), (4, 9), (4, 8), (4, 7), (4, 6), (3, 6), (3, 7), (2, 7)], [(9, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (8, 2)]], 'snake_lengths': [9, 9], 'snake_healths': [95, 85]}
#state['snake_heads'][0], state['snake_heads'][1] = state['snake_heads'][1], state['snake_heads'][0]
#state['snake_bodies'][0], state['snake_bodies'][1] = state['snake_bodies'][1], state['snake_bodies'][0]
#state['snake_lengths'][0], state['snake_lengths'][1] = state['snake_lengths'][1], state['snake_lengths'][0]
#state['snake_healths'][0], state['snake_healths'][1] = state['snake_healths'][1], state['snake_healths'][0]
##
#print(monte_carlo_tree_search(state))
