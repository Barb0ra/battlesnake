import random
import typing


def state_reward(game_state):
    reward = 0
    # -1 if I die
    if is_dead(game_state, 0):
        reward += -1
    # +1 if I am the last one standing
    if len(game_state['snake_heads']) == 2 and is_dead(game_state, 1) and not(is_dead(game_state, 0)):
        reward += 1
    # 0.3 if an opponent dies (not the last one)
    if len(game_state['snake_heads']) > 2:
        for snake_index in range(len(game_state['snake_heads'])):
            if snake_index != 0 and is_dead(game_state, snake_index):
                reward += 0.05
    return reward


def is_dead(game_state, snake):
    # death by hunger
    if game_state['snake_healths'][snake] <= 0:
        return True
    
    # death by collision with a wall
    if game_state['snake_heads'][snake] in game_state['hazards']:
        return True
    
    # death by collision with a snake body
    for snake_body in game_state['snake_bodies']:
        # if my head is in a snake body
        if game_state['snake_heads'][snake] in snake_body:
            return True

    # death by collision with a snake head
    for snake_index, snake_head in enumerate(game_state['snake_heads']):
        if snake_index != snake and game_state['snake_heads'][snake] == snake_head:
            if game_state['snake_lengths'][snake] <= game_state['snake_lengths'][snake_index]:
                return True
                 
    return False

