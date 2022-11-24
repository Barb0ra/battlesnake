import itertools
import copy
import numpy as np
from RL_value_function import get_value
from RL_state_reward import is_dead, state_reward
from state_generator import get_likely_moves, cleanup_state, next_state_for_action
import time


def generate_possible_states(game_state, my_action, timeout_start, timeout):
    # returns an array of possible states
    possible_states = []
    opponents_left = len(game_state['snake_heads']) - 1
    if opponents_left < 0:
        opponents_left = 0
    likely_opponent_moves = []
    for opponent in range(opponents_left):
        likely_opponent_moves.append(
            get_likely_moves(game_state, opponent + 1))
    move_combinations = list(itertools.product(*likely_opponent_moves))
    # how the board changes when I move
    my_next_state = next_state_for_action(game_state, 0, my_action)
    # how the board changes when everyone else moves
    for move_combination in move_combinations:
        next_state = my_next_state
        for snake_index, move in enumerate(move_combination):
            next_state = next_state_for_action(
                next_state, snake_index + 1, move)
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
    return True
      

class SearchTree:
    def __init__(self):
        self.root_state = None

    def set_root_state(self, game_state, timeout_start, timeout):
        if self.root_state == None:
            self.root_state = StateNode(game_state)
            self.root_state.generate_actions(timeout_start, timeout)
        else:
            existing_state = False
            for state in self.root_state.get_max_action(timeout_start, timeout).states:
                if equal_states(state.game_state, game_state):
                    self.root_state = state
                    self.root_state.game_state = game_state
                    existing_state = True
                    break
            if not existing_state:
                self.root_state = StateNode(game_state)
                self.root_state.generate_actions(timeout_start, timeout)


class ActionNode:

    def __init__(self, parent, action, timeout_start, timeout):
        self.parent_state = parent
        self.action = action
        self.states = self.generate_state_nodes(
            parent.game_state, action, timeout_start, timeout)

    def sample_min_state(self):
        min = None
        min_state = None
        for state in self.states:
            sample_value = state.get_sample_value()
            if min == None or sample_value < min:
                min = sample_value
                min_state = state
        return sample_value, min_state

    def get_state_with_smallest_mean(self):
        # this can be used to pick the final action
        min = None
        min_state = None
        for state in self.states:
            value = state.mean
            if min == None or value < min:
                min = value
                min_state = state
        return min, min_state

    def get_state_with_lowest_lcb(self):
        min = None
        min_state = None
        for state in self.states:
            value = state.mean - 2*(state.variance)**0.5
            if min == None or value < min:
                min = value
                min_state = state
        return min, min_state

    def generate_state_nodes(self, parent_state, action, timeout_start, timeout):
        states = generate_possible_states(
            parent_state, action, timeout_start, timeout)
        return [StateNode(state, self) for state in states]


class StateNode:

    def __init__(self, game_state, parent=None):

        self.n_visited = 1
        self.parent_action = parent
        self.reward = state_reward(game_state)
        # gamma's shape parameter
        self.alpha = 1
        self.terminal = self.terminal(game_state)

        if self.terminal:
            self.mean = self.reward
            self.variance = 0
            self.beta = 0
        else:
            mean, variance = get_value(game_state)
            self.mean = mean + self.reward
            self.variance = variance
            self.beta = variance
        self.game_state = cleanup_state(game_state)
        self.actions = []

    def terminal(self, game_state):
        return len(game_state['snake_heads']) <= 1 or is_dead(game_state, 0)[0] or (len(game_state['snake_heads']) <= 2 and is_dead(game_state, 1)[0])

    def generate_actions(self, timeout_start, timeout):
        if len(self.actions) == 0:
            for action in get_likely_moves(self.game_state, 0):
                self.actions.append(ActionNode(
                    self, action, timeout_start, timeout))

    def update_value(self, observation):
        self.mean = (observation + self.mean*self.n_visited) / (self.n_visited+1)
        self.beta += 0.5 * self.n_visited/(self.n_visited+1) * (observation - self.mean)**2
        self.n_visited += 1
        self.alpha += 0.5
        self.variance = self.beta / (self.alpha + 1)

    def get_sample_value(self):
        return np.random.normal(self.mean, np.sqrt(self.variance))

    def sample_max_action(self, timeout_start, timeout):
        max_value = None
        max_action = None
        min_state_for_max_action = None
        # if actions are not generated, generate them
        if len(self.actions) == 0:
            self.generate_actions(timeout_start, timeout)
        for action in self.actions:
            state_sample_value, min_state = action.sample_min_state()

            if max_action == None or state_sample_value > max_value:
                max_value = state_sample_value
                max_action = action
                min_state_for_max_action = min_state
        return max_action, min_state_for_max_action

    def get_max_action(self, timeout_start, timeout):
        # get action with the highest min state mean value (deterministic)
        # can be used to make a final decisionon what action to take
        max_value = None
        max_action = None
        # if actions are not generated, generate them
        if len(self.actions) == 0:
            self.generate_actions(timeout_start, timeout)
        for action in self.actions:
            state_val, min_state = action.get_state_with_smallest_mean()
            #state_val, min_state = action.get_state_with_lowest_lcb()

            if max_action == None or state_val > max_value:
                max_value = state_val
                max_action = action
        return max_action


def min_max_tree_search(search_tree, timeout_start, timeout):
    # iterative deepening
    #max_depth = 6 - len(game_state['snake_heads'])
    root_state = search_tree.root_state
    depth = 3
    max_depth = 10
    iteration_counter = 0
    iterations_per_depth = 5
    # discounting factor
    alpha = 0.8
    while time.time() < timeout_start + timeout and depth <= max_depth:
        
        #print('actions')
        #for action in root_state.actions:
        #    print(action.action)
        #    for state in action.states:
        #        print(state.mean, state.variance)

        max_action, min_state = root_state.sample_max_action(
            timeout_start, timeout)
        update_state_nodes(min_state, depth-1, alpha,
                           0, timeout_start, timeout)
        iteration_counter += 1
        if iteration_counter >= iterations_per_depth:
            iteration_counter = 0
            depth += 1

    print(depth)
    return root_state.get_max_action(timeout_start, timeout).action


def update_state_nodes(state, depth, alpha, accumulated_reward, timeout_start, timeout):
    if depth == 0 or state.terminal:
        return state.mean + accumulated_reward
    max_action, min_state = state.sample_max_action(timeout_start, timeout)
    min_state_value = update_state_nodes(
        min_state, depth - 1, alpha, accumulated_reward + state.reward, timeout_start, timeout)
    state.update_value(min_state_value)
    return min_state_value * alpha
