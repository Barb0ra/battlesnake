import itertools
import copy
import numpy as np
from RL_value_function import get_value
from RL_state_reward import is_dead, state_reward
from state_generator import get_likely_opponent_moves, cleanup_state, next_state_for_action
import time

def generate_possible_states(game_state, my_action):
    # returns an array of possible states
    possible_states = []
    opponents_left = len(game_state['snake_heads']) - 1
    if opponents_left < 0:
        opponents_left = 0
    likely_opponent_moves = []
    for opponent in range(opponents_left):
        likely_opponent_moves.append(get_likely_opponent_moves(game_state, opponent + 1))
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

    def set_root_state(self, game_state):
        if True:  
      #if self.root_state == None:
            self.root_state = StateNode(game_state)
            self.root_state.generate_actions()
        else:
            existing_state = False
            for state in self.root_state.get_max_action().states:
                if equal_states(state.game_state, game_state):
                    self.root_state = state
                    existing_state = True
                    break
            if not existing_state:
                self.root_state = StateNode(game_state)
                self.root_state.generate_actions()
            


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
        self.terminal = self.terminal(game_state)
        if self.terminal:
          self.value = self.reward
        else:
          self.value = get_value(game_state) + self.reward
        self.game_state = cleanup_state(game_state)
        self.actions = []
    
    def terminal(self, game_state):
        return len(game_state['snake_heads']) <= 1 or is_dead(game_state, 0)[0] or (len(game_state['snake_heads']) <= 2 and is_dead(game_state, 1)[0])

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


def min_max_tree_search(search_tree, timeout_start):
    timeout = 0.3
    # iterative deepening
    #max_depth = 6 - len(game_state['snake_heads'])
    root_state = search_tree.root_state
    depth = 1
    max_depth = 10
    iteration_counter = 0
    iterations_per_depth = 1
    # discounting factor
    alpha = 0.7
    while time.time() < timeout_start + timeout and depth <= max_depth:
        leaf_state, accumulated_reward = traverse(root_state, depth)
        simulation_result = get_simulation_result(
            leaf_state) + accumulated_reward
        backpropagate(leaf_state, simulation_result, alpha)
        iteration_counter += 1
        if iteration_counter > iterations_per_depth:
            iteration_counter = 0
            depth += 1
            print(depth)
        #for action in root_state.actions:
        #    print(action.action, action.get_min_state().value,
        #          action.get_min_state().reward)
    
    return root_state.get_max_action().action


def get_simulation_result(leaf_state):
    return leaf_state.value


# function for state traversal


def traverse(state, depth):
    accumulated_reward = 0
    while depth > 0 and not state.terminal:
        depth -= 1
        accumulated_reward += state.reward
        max_action = state.get_max_action()
        state = max_action.get_min_state()
    return state, accumulated_reward


# function for backpropagation


def backpropagate(state, result, alpha):
    state.update_value(result)
    result = result * alpha
    if state.parent_action == None:
        return
    backpropagate(state.parent_action.parent_state, result, alpha)