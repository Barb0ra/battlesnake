import random
import typing
from bayesian_snake_logic.RL_state_reward import is_dead

from bayesian_snake_logic.state_generator import next_state_for_action


def state_reward(game_state, rewards, game_type, game_map, hazard_damage):
  # a list of all snake bodies
  snakes = []
  for snake in game_state['snake_bodies']:
    snakes += snake

  state_reward = 0
  state_reward += death_reward(game_state, rewards, game_type, game_map, hazard_damage)
  state_reward += head_collision_reward(game_state, rewards)
  state_reward += food_reward(game_state, rewards, snakes, game_type, game_map, hazard_damage)
  state_reward += domination_reward(game_state, rewards, snakes, game_type, game_map, hazard_damage)
  state_reward += accessible_area_reward(game_state, snakes, game_type, game_map, hazard_damage)*3
  state_reward += next_to_hazard(game_state, game_type, game_map, hazard_damage)*3
  return state_reward


def death_reward(game_state, rewards, game_type, game_map, hazard_damage):
  dead = is_dead(game_state, 0, game_type, game_map, hazard_damage)[0]

  if dead:
    return rewards['death']
  else:
    return 0


def head_collision_reward(game_state, rewards):
  reward = 0

  for snake_index in range(1, len(game_state['snake_heads'])):
    # if my head is in an opponent's head
    if game_state['snake_heads'][0] == game_state['snake_heads'][snake_index]:
      # collision with a bigger snake head
      if game_state['snake_lengths'][0] <= game_state['snake_lengths'][
          snake_index]:
        reward += rewards['death_by_head_collision']
      # collision with a smaller snake head
      else:
        reward += rewards['opponent_death']
  return reward


def food_reward(game_state, rewards, snakes, game_type, game_map, hazard_damage):
  reward = 0
  nearest_food = bfs_nearest_food(game_state, snakes, game_type, game_map, hazard_damage)
  if nearest_food is None:
    return -10
  # if hungry
  if game_state['snake_healths'][0] < 30:
    reward += nearest_food * rewards['distance_to_food_when_hungry']
  # if not bigger than the biggest opponent
  elif game_state['snake_lengths'][0] < max(game_state['snake_lengths'][1:]):
    reward += nearest_food * rewards['distance_to_food_when_small']
  return reward


def domination_reward(game_state, rewards, snakes, game_type, game_map, hazard_damage):
  reward = 0
  board_domination = bfs_board_domination(game_state, snakes, game_type, game_map, hazard_damage)
  reward = board_domination[0] * rewards['board_domination']
  return reward


def bfs_nearest_food(game_state, snakes, game_type, game_map, hazard_damage):
  get_neighbors, deadly_fields = initialise_neighbouring_field_rules(game_state, game_type, game_map, hazard_damage)
  my_head = game_state['snake_heads'][0]
  visited = set()
  queue = []
  if my_head not in snakes and game_state['snake_healths'][0] > 0 and my_head not in game_state['snake_heads'][1:]:
    queue.append((my_head, 0))
    visited.add(my_head)
  while queue != []:
    current_node, distance = queue.pop(0)
    if current_node in game_state['food']:
      return distance
    for neighbor in get_neighbors(current_node, game_state, snakes, deadly_fields):
      if neighbor not in visited:
        queue.append((neighbor, distance + 1))
        visited.add(neighbor)
  return None


def get_neighbors_wrapped(current_node, game_state, snakes, deadly_fields):
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
    if neighbor not in deadly_fields and neighbor not in snakes and neighbor not in game_state['snake_heads']:
      neighbors.append(neighbor)
  return neighbors

def get_neighbors_standard(current_node, game_state, snakes, deadly_fields):
  potential_neighbors = []
  neighbors = []
  height = game_state['height']
  width = game_state['width']
  x, y = current_node
  if x + 1 < width:
    potential_neighbors.append((x + 1, y))
  if x - 1 >= 0:
    potential_neighbors.append((x - 1, y))
  if y + 1 < height:
    potential_neighbors.append((x, y + 1))
  if y - 1 >= 0:
    potential_neighbors.append((x, y - 1))
  for neighbor in potential_neighbors:
    if neighbor not in deadly_fields and neighbor not in snakes and neighbor not in game_state['snake_heads']:
      neighbors.append(neighbor)
  return neighbors

def initialise_neighbouring_field_rules(game_state, game_type, game_map, hazard_damage):
  if game_type == 'wrapped':
    get_neighbors = get_neighbors_wrapped
    deadly_fields = set()
  elif game_type == 'standard':
    get_neighbors = get_neighbors_standard
    # out of bounds fields
    deadly_fields = set()
    for x in range(game_state['width']):
      deadly_fields.add((x, -1))
      deadly_fields.add((x, game_state['height']))
    for y in range(game_state['height']):
      deadly_fields.add((-1, y))
      deadly_fields.add((game_state['width'], y))
  if hazard_damage >= 100:
    deadly_fields = deadly_fields.union(game_state['hazards'])
  return get_neighbors, deadly_fields

def bfs_board_domination(game_state, snakes, game_type, game_map, hazard_damage):
  get_neighbors, deadly_fields = initialise_neighbouring_field_rules(game_state, game_type, game_map, hazard_damage)
  snake_domination = {}
  snake_queues = {}
  visited = set()
  # sort snakes by length and put me last if it's a tie
  snake_indices_by_length = sorted(
    range(len(game_state['snake_lengths'])),
    key=lambda k: (game_state['snake_lengths'][k], 0 if k==0 else 1),
    reverse=True)
  for snake_index in snake_indices_by_length:
    snake_head = game_state['snake_heads'][snake_index]
    snake_domination[snake_index] = 0
    snake_queues[snake_index] = []
    if snake_head not in snakes and snake_head not in deadly_fields and snake_head not in game_state['snake_heads'][snake_index+1:] and snake_head not in game_state['snake_heads'][:snake_index]:
      snake_queues[snake_index].append((snake_head, 0))
      visited.add(snake_head)

  while non_empty(snake_queues):
    for snake_index in snake_indices_by_length:
      queue = snake_queues[snake_index]
      if queue != []:
        current_node, domination = queue.pop(0)
        for neighbor in get_neighbors(current_node, game_state, snakes, deadly_fields):
          if neighbor not in visited:
            snake_queues[snake_index].append((neighbor, 0))
            visited.add(neighbor)
            snake_domination[snake_index] += 1
  return snake_domination


def non_empty(snake_queues):
  for queue in snake_queues.values():
    if queue:
      return True
  return False

def bfs_accessible_area(game_state, snake_bodies, snake_index, game_type, game_map, hazard_damage):
  get_neighbors, deadly_fields = initialise_neighbouring_field_rules(game_state, game_type, game_map, hazard_damage)
  head = game_state['snake_heads'][snake_index]
  visited = set()
  area = 0
  queue = []
  if head not in snake_bodies and head not in deadly_fields and head not in game_state['snake_heads'][:snake_index] and head not in game_state['snake_heads'][snake_index+1:]:
      queue.append((head))
      visited.add(head)
      area += 1
  else:
      return area
  while queue != []:
      current_node = queue.pop(0)
      for neighbor in get_neighbors(current_node, game_state, snake_bodies, deadly_fields):
          if neighbor not in visited:
              queue.append((neighbor))
              visited.add(neighbor)
              area += 1
  return area

def accessible_area_reward(state, snakes, game_type, game_map, hazard_damage):
  reward = 0
  reward += bfs_accessible_area(state, snakes, 0, game_type, game_map, hazard_damage)
  return reward

def next_to_hazard(state, game_type, game_map, hazard_damage):
  head = state['snake_heads'][0]
  for hazard in state['hazards']:
    distance = abs(hazard[0] - head[0]) + abs(hazard[1] - head[1])
    if  distance == 1:
      return 1
  return 0

def in_hazard(state, game_type, game_map, hazard_damage):
  head = state['snake_heads'][0]
  if head in state['hazards']:
    return 1
  return 0
