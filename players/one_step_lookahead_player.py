import random
from heuristic_baseline_functions.one_step_lookahead import sample_best_minmax_action
from bayesian_snake_logic.state_generator import next_state_for_action, transform_state
from heuristic_baseline_functions.state_reward_heuristic import state_reward


class OneStepLookaheadPlayer():

    def __init__(self, params, game_type, game_map, hazard_damage):
        self.rewards = {
            'death': -1000,
            'death_by_head_collision': -700,
            'opponent_death': 100,
            'distance_to_food_when_hungry': -5,
            'distance_to_food_when_small': -1,
            'board_domination': 2
        }
        self.game_type = game_type
        self.game_map = game_map
        self.hazard_damage = hazard_damage

    def info(self):
        return {
            "apiversion": "1",
            "author": "Barbora",
            "color": "#3352FF",
            "head": "default",  # TODO: Choose head
            "tail": "default",  # TODO: Choose tail
        }

    def move(self, game_state):
        # move is called on every turn and returns your next move
        # Valid moves are "up", "down", "left", or "right"

        #print('turn ', game_state['turn'])
        #print(game_state)
        game_state = transform_state(game_state, self.game_type, self.game_map, self.hazard_damage)
        #print(game_state)
        action_values = sample_best_minmax_action(game_state, self.rewards, self.game_type, self.game_map, self.hazard_damage)

        next_move = sorted(
            action_values, key=action_values.get, reverse=True)[0]
        #print(action_values, next_move)

        return {"move": next_move}
