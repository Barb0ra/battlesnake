import copy
from RL_state_reward import is_dead


def next_state_for_action(game_state, snake_index, action, game_type, game_map, hazard_damage):

    game_state = copy.deepcopy(game_state)
    head = game_state['snake_heads'][snake_index]
    food = game_state['food']
    # move the head
    next_position = move_head(
        head, action, game_state['width'], game_state['height'], game_type)

    ate_food = False
    if next_position in food:
        ate_food = True
        game_state['snake_lengths'][snake_index] += 1
        game_state['snake_healths'][snake_index] = 100

    # add head to body
    game_state['snake_bodies'][snake_index].insert(0, head)
    # move head to the next position
    game_state['snake_heads'][snake_index] = next_position
    # remove the tail if the snake did not eat food
    if not ate_food:
        game_state['snake_bodies'][snake_index].pop(-1)
        game_state['snake_healths'][snake_index] -= 1

    if next_position in game_state['hazards']:
        game_state['snake_healths'][snake_index] -= hazard_damage
        if game_map == 'royale' and ate_food:
            game_state['snake_healths'][snake_index] == 100

    return game_state


def move_head(head, action, width, height, game_type):
    if game_type == 'wrapped':
        if action == 'up':
            next_position = (head[0], (head[1] + 1) % height)
        if action == 'down':
            next_position = (head[0], (head[1] - 1) % height)
        if action == 'left':
            next_position = ((head[0] - 1) % width, head[1])
        if action == 'right':
            next_position = ((head[0] + 1) % width, head[1])
    if game_type == 'standard':
        if action == 'up':
            next_position = (head[0], head[1] + 1)
        if action == 'down':
            next_position = (head[0], head[1] - 1)
        if action == 'left':
            next_position = (head[0] - 1, head[1])
        if action == 'right':
            next_position = (head[0] + 1, head[1])
    return next_position


def cleanup_state(game_state, game_type, game_map, hazard_damage):
    dead_snakes = set()
    snake_bodies = []
    for body in game_state['snake_bodies']:
        snake_bodies += body
    snake_heads = game_state['snake_heads']
    for snake_index, head in enumerate(snake_heads):
        if is_dead(game_state, snake_index, game_type, game_map, hazard_damage)[0]:
            dead_snakes.add(snake_index)

        # remove eaten food from the game state
        if head in game_state['food']:
            game_state['food'].remove(head)

    # remove dead snakes from the game state
    for snake_index in sorted(list(dead_snakes), reverse=True):
        game_state['snake_heads'].pop(snake_index)
        game_state['snake_bodies'].pop(snake_index)
        game_state['snake_lengths'].pop(snake_index)
        game_state['snake_healths'].pop(snake_index)

    return game_state


def get_likely_moves(game_state, snake_index, game_type, game_map, hazard_damage):
    # get moves that are likely to happen (exclude self-destructing moves)
    # snake bodies except tails because the tails may move
    snake_bodies = []
    for body in game_state['snake_bodies']:
        snake_bodies += body[:-1]
    likely_moves = []
    possible_moves = ['up', 'down', 'left', 'right']
    good_moves_left = False
    for possible_move in possible_moves:
        next_state = next_state_for_action(
            game_state, snake_index, possible_move, game_type, game_map, hazard_damage)
        # if the snake is not hazard is hazard damage is deadly
        # or the snake did not run into a wall is the game is standard
        if (hazard_damage >= 100 and next_state['snake_heads'][snake_index] not in next_state['hazards']) or (game_type == 'standard' and next_state['snake_heads'][snake_index][0] >= 0 and next_state['snake_heads'][snake_index][0] < next_state['width'] and next_state['snake_heads'][snake_index][1] >= 0 and next_state['snake_heads'][snake_index][1] < next_state['height']):
            # and not in the body of another snake except tail
            if next_state['snake_heads'][snake_index] not in snake_bodies:
                likely_moves.append(possible_move)
                good_moves_left = True
    if not good_moves_left:
        likely_moves = ['up']
    return likely_moves


def transform_state(game_state, game_type, game_map, hazard_damage):
    # transform game state to a flatter format
    transformed_state = {}
    transformed_state['height'] = game_state['board']['height']
    transformed_state['width'] = game_state['board']['width']
    transformed_state['food'] = set()
    for food in game_state['board']['food']:
        transformed_state['food'].add((food['x'], food['y']))
    transformed_state['hazards'] = set()
    for hazard in game_state['board']['hazards']:
        transformed_state['hazards'].add((hazard['x'], hazard['y']))
    transformed_state['snake_heads'] = []
    transformed_state['snake_bodies'] = []
    transformed_state['snake_lengths'] = []
    transformed_state['snake_healths'] = []
    # I am always the snake at index 0
    transformed_state['snake_heads'].append(
        (game_state['you']['head']['x'], game_state['you']['head']['y']))
    transformed_state['snake_bodies'].append([])
    # do not append head to body
    if game_state['turn'] > 0:
        for body in game_state['you']['body'][1:]:
            transformed_state['snake_bodies'][0].append((body['x'], body['y']))
    transformed_state['snake_lengths'].append(game_state['you']['length'])
    transformed_state['snake_healths'].append(game_state['you']['health'])
    # Other snakes
    for snake in game_state['board']['snakes']:
        if snake['id'] != game_state['you']['id']:
            transformed_state['snake_heads'].append(
                (snake['head']['x'], snake['head']['y']))
            transformed_state['snake_bodies'].append([])
            # do not append head to body
            if game_state['turn'] > 0:
                for body in snake['body'][1:]:
                    transformed_state['snake_bodies'][-1].append(
                        (body['x'], body['y']))
            transformed_state['snake_lengths'].append(snake['length'])
            transformed_state['snake_healths'].append(snake['health'])
    return transformed_state
