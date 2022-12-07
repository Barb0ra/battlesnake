import copy
import itertools
from math import ceil, floor
import threading
import time
from run_games import run_games

GO_FILE_PATH = '../battlesnake_rules/battlesnake'

def tune_parameters():
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params':[2,10,3,0.9, 'lcb']}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params':[]}]
    games_per_param = 15
    available_ports = [8000, 8001]
    # parameter options
    tree_min_depth = [2,3,4,5]
    tree_max_depth = [5,6,8,10]
    tree_iterations_per_depth = [2,4,6,8]
    discounting_factor = [0.9]
    mean_or_lcb = ['lcb']
    # parameter combinations
    parameter_combinations = list(itertools.product(tree_min_depth, tree_max_depth, tree_iterations_per_depth, discounting_factor, mean_or_lcb))
    number_of_batches = floor(len(available_ports)/len(snakes))
    batch_size = ceil(len(parameter_combinations)/number_of_batches)
    # split into batches
    batches = [parameter_combinations[i:i + batch_size] for i in range(0, len(parameter_combinations), batch_size)]
    # put leftovers in last batch
    batches[-1] += parameter_combinations[batch_size*number_of_batches:]
    # run batches in threads
    for i, batch in enumerate(batches):
        snakes = copy.deepcopy(snakes)
        for snake in snakes:
            snake['port'] = available_ports.pop()
        thread = threading.Thread(target=run_games_for_parameters, args=(i, batch, games_per_param, snakes, 'param_game_stats/batch'+str(i)+'.txt', 'param_game_stats/logs_batch'+str(i)+'.txt')).start()
    
    

def run_games_for_parameters(batch_number, parameter_combinations, games_per_param, snakes, output_file, log_file):
    counter = 0
    while len(parameter_combinations) > 0:
        print(f'Batch {batch_number} - Running {games_per_param} games for parameter combination {counter}')
        counter += 1
        parameter_combination = parameter_combinations.pop()
        print(f'Running games for parameters: {parameter_combination}')
        for snake in snakes:
            if snake['name'] == 'Bayesian':
                snake['params'] = parameter_combination
        game_stats = run_games(games_per_param, snakes, GO_FILE_PATH, log_file)
        # write game_stats to file
        with open(output_file, 'a') as f:
            f.write(str(parameter_combination) + '\n' + str(game_stats) + '\n')
        time.sleep(5)




tune_parameters()
