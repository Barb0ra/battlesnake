import copy
import itertools
from math import ceil, floor
import threading
import time
from learning.run_games import run_games

GO_FILE_PATH = '../battlesnake_rules/battlesnake'


def tune_parameters():
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [2.0, 8.0, 6.0, 0.9,
                                                                                   'lcb', True, 'basic']}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]
    games_per_param = 1
    available_ports = [8000, 8001]
    # parameter options
    tree_min_depth = [2]
    tree_max_depth = [8]
    tree_iterations_per_depth = [6]
    discounting_factor = [0.9]
    mean_or_lcb = ['mean']
    log_state_values = [True]
    value_function = ['gp_value_function_10_batches_5_games.joblib']
    # parameter combinations
    parameter_combinations = list(itertools.product(tree_min_depth, tree_max_depth,
                                  tree_iterations_per_depth, discounting_factor, mean_or_lcb, log_state_values, value_function))
    for snake in snakes:
        snake['port'] = available_ports.pop()
    run_games_for_parameters(parameter_combinations, games_per_param, snakes,
                             'param_game_stats/parameter_tuning.txt', 'param_game_stats/logs.txt')


def run_games_for_parameters(parameter_combinations, games_per_param, snakes, output_file, log_file):
    counter = 0
    while len(parameter_combinations) > 0:
        print(
            f'Running {games_per_param} games for parameter combination {counter}')
        counter += 1
        parameter_combination = parameter_combinations.pop()
        print(f'Running games for parameters: {parameter_combination}')
        for snake in snakes:
            if snake['name'] == 'Bayesian':
                snake['params'] = parameter_combination
        # run games
        game_stats = run_games(games_per_param, snakes, GO_FILE_PATH, log_file)
        # write game_stats to file
        with open(output_file, 'a') as f:
            f.write(str(parameter_combination) + '\n' + str(game_stats) + '\n')
        time.sleep(5)
