import random
from bayesian_snake_logic.state_generator import next_state_for_action, transform_state
from heuristic_baseline_functions.state_reward_heuristic import state_reward


class SelfPreservingPlayer():

    def __init__(self, params, game_type, game_map, hazard_damage):
        self.rewards = {
            'death': -100,
            'opponent_death': 0,
            'distance_to_food_when_hungry': 0,
            'distance_to_food_when_small': 0,
            'board_domination': 0
        }
        self.game_type = game_type
        self.game_map = game_map
        self.hazard_damage = hazard_damage

    def info(self):
        return {
            "apiversion": "1",
            "author": "Barbora",
            "color": "#46FF33",
            "head": "default",  # TODO: Choose head
            "tail": "default",  # TODO: Choose tail
        }

    def get_move_values(self, game_state, game_type, game_map, hazard_damage):
        # value is the immedtae reward for a move
        # does not take other opponents' moves into account
        moves = ["up", "down", "left", "right"]
        move_value = {}
        for move in moves:
            move_value[move] = state_reward(
                next_state_for_action(game_state, 0, move, game_type, game_map, hazard_damage),
                self.rewards, game_type, game_map, hazard_damage)

        return move_value

    def move(self, game_state):
        # move is called on every turn and returns your next move
        # Valid moves are "up", "down", "left", or "right"
        game_state = transform_state(game_state, self.game_type, self.game_map, self.hazard_damage)

        move_values = self.get_move_values(game_state, self.game_type, self.game_map, self.hazard_damage)
        best_value = max(move_values.values())
        best_moves = []
        for move, value in move_values.items():
            if value == best_value:
                best_moves.append(move)

        # Choose a random move from the safe ones
        next_move = random.choice(best_moves)

        return {"move": next_move}
