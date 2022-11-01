import copy


def next_state_for_action(game_state, snake_index, action):

    game_state = copy.deepcopy(game_state)
    head = game_state['snake_heads'][snake_index]
    food = game_state['food']
    # move the head
    if action == 'up':
        next_position = (head[0], (head[1] + 1) % game_state['height'])
    if action == 'down':
        next_position = (head[0], (head[1] - 1) % game_state['height'])
    if action == 'left':
        next_position = ((head[0] - 1) % game_state['width'], head[1])
    if action == 'right':
        next_position = ((head[0] + 1) % game_state['width'], head[1])

    ate_food = False
    if next_position in food:
        ate_food = True
        game_state['snake_lengths'][snake_index] += 1
        # TODO: check rules for health
        game_state['snake_healths'][snake_index] = 100

    # add head to body
    game_state['snake_bodies'][snake_index].insert(0, head)
    # move head to the next position
    game_state['snake_heads'][snake_index] = next_position
    # remove the tail if the snake did not eat food
    if not ate_food:
        game_state['snake_bodies'][snake_index].pop(-1)


    return game_state

def cleanup_state(game_state):    
    dead_snakes = set()
    snake_bodies = []
    for body in game_state['snake_bodies']:
        snake_bodies += body
    snake_heads = game_state['snake_heads']
    for snake_index, head in enumerate(snake_heads):
        if head in game_state['hazards'] or head in snake_bodies:
            dead_snakes.add(snake_index)
        
        #collision of snakes
        for snake_index2, head2 in enumerate(snake_heads):
            if snake_index != snake_index2 and head == head2:
                if game_state['snake_lengths'][snake_index] <= game_state['snake_lengths'][snake_index2]:
                    dead_snakes.add(snake_index)
                if game_state['snake_lengths'][snake_index] >= game_state['snake_lengths'][snake_index2]:
                    dead_snakes.add(snake_index2)
        
        if game_state['snake_healths'][snake_index] <= 0:
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

def get_likely_opponent_moves(game_state, snake_index):
    # get opponent moves that are likely to happen (exclude self-destructing moves)
    # snake bodies except tails because the tails may move
    snake_bodies = []
    for body in game_state['snake_bodies']:
        snake_bodies += body[:-1]
    likely_moves = []
    possible_moves = ['up', 'down', 'left', 'right']
    good_moves_left = False
    for possible_move in possible_moves:
        next_state = next_state_for_action(game_state, snake_index, possible_move)
        # if the snake is in the wall
        if next_state['snake_heads'][snake_index] not in next_state['hazards']:
            # and not in the body of another snake except tail
            if next_state['snake_heads'][snake_index] not in snake_bodies:
                likely_moves.append(possible_move)
                good_moves_left = True
    if not good_moves_left:
        likely_moves.append(possible_moves[0])
    return likely_moves



def transform_state(game_state):
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
            for body in snake['body'][1:]:
                transformed_state['snake_bodies'][-1].append(
                    (body['x'], body['y']))
            transformed_state['snake_lengths'].append(snake['length'])
            transformed_state['snake_healths'].append(snake['health'])
    return transformed_state
