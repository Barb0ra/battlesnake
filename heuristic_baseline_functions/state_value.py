from .state_reward_heuristic import state_reward


def state_value_deterministic(state, rewards, game_type, game_map, hazard_damage):
    # state_value is the expected reward for a state
    # just return the expected reward for the current state (no lookahead)
    return state_reward(state, rewards, game_type, game_map, hazard_damage)