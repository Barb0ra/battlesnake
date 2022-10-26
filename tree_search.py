import itertools
import copy
import numpy as np
from RL_value_function import get_value
from state_generator import next_state_for_action


def sample_best_minmax_action(game_state, rewards):
  actions = ['up', 'down', 'left', 'right']
  action_values = {}
  state_values = []
  for action in actions:
    possible_states = generate_possible_states(game_state, action)
    for state in possible_states:
          # sample from the value function
          state_values.append(get_value(state, rewards))
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


# main function for the Monte Carlo Tree Search
def monte_carlo_tree_search(root):
     
    while resources_left(time, computational power):
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        backpropagate(leaf, simulation_result)
         
    return best_child(root)
 
# function for node traversal
def traverse(node):
    while fully_expanded(node):
        node = best_uct(node)
         
    # in case no children are present / node is terminal
    return pick_unvisited(node.children) or node
 
# function for the result of the simulation
def rollout(node):
    while non_terminal(node):
        node = rollout_policy(node)
    return result(node)
 
# function for randomly selecting a child node
def rollout_policy(node):
    return pick_random(node.children)
 
# function for backpropagation
def backpropagate(node, result):
    if is_root(node) return
    node.stats = update_stats(node, result)
    backpropagate(node.parent)
 
# function for selecting the best child
# node with highest number of visits
def best_child(node):
    pick child with highest number of visits