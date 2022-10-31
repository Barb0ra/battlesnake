import random
import typing


def state_reward(game_state):
    reward = 0
    # reward for dying (negative)
    dead, death_reward = is_dead(game_state, 0)
    if dead:
        reward += death_reward
    # +1 if I am the last one standing
    if len(game_state['snake_heads']) <= 2 and is_dead(game_state, 1)[0] and not(dead):
        reward += 1
    # 0.3 if an opponent dies (not the last one)
    if len(game_state['snake_heads']) > 2:
        for snake_index in range(1, len(game_state['snake_heads'])):
            if is_dead(game_state, snake_index)[0]:
                reward += 0.1
    return reward


def is_dead(game_state, snake):
    # death by hunger
    if game_state['snake_healths'][snake] <= 0:
        return True, -1
    
    # death by collision with a wall
    if game_state['snake_heads'][snake] in game_state['hazards']:
        return True, -1
    
    # death by collision with a snake body
    for snake_body in game_state['snake_bodies']:
        # if my head is in a snake body
        if game_state['snake_heads'][snake] in snake_body:
            return True, -1

    # death by collision with a snake head
    for snake_index, snake_head in enumerate(game_state['snake_heads']):
        if snake_index != snake and game_state['snake_heads'][snake] == snake_head:
            if game_state['snake_lengths'][snake] <= game_state['snake_lengths'][snake_index]:
                return True, -0.8
                 
    return False, 0

