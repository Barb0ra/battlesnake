import copy
import itertools
from math import ceil, floor
import time
from learning.run_games import run_games

GO_FILE_PATH = '../battlesnake_rules/battlesnake'


def tune_parameters(value_function, depth, iterations, baseline):
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [2.0, 6.0, 4.0, 0.9,
                                                                                   'lcb', False, value_function]},
              {'name': 'Baseline', 'type': baseline, 'port': 8080, 'params': []}]
    games_per_param = 100
    available_ports = [8080, 8000]
    # parameter options
    tree_min_depth = [depth]
    tree_max_depth = [depth]
    tree_iterations_per_depth = [iterations]
    discounting_factor = [0.9]
    mean_or_lcb = ['mean']
    log_state_values = [False]
    value_function = [value_function]
    # parameter combinations
    parameter_combinations = list(itertools.product(tree_min_depth, tree_max_depth,
                                  tree_iterations_per_depth, discounting_factor, mean_or_lcb, log_state_values, value_function))
    for snake in snakes:
        snake['port'] = available_ports.pop()
    run_games_for_parameters(parameter_combinations, games_per_param, snakes,
                             'param_game_stats/parameter_tuning.txt', 'param_game_stats/logs.txt', log_state_values[0])


def run_games_for_parameters(parameter_combinations, games_per_param, snakes, output_file, log_file, log_state_values):
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
        print(snakes)
        game_stats = run_games(games_per_param, snakes,
                               GO_FILE_PATH, log_file, log_state_values)
        # write game_stats to file
        with open(output_file, 'a') as f:
            f.write(str(parameter_combination) + '\n' + str(game_stats) + '\n')
        time.sleep(5)
