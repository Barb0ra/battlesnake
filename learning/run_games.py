import subprocess
import time
import multiprocessing

from server import run_server

# example snakes dictionary
snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [2, 8, 6, 0.9, 'lcb',
                                                                               False, 'basic']}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]


def run_games(game_count, snakes, GO_FILE_PATH, log_file, log_state_values):

    command = [GO_FILE_PATH, 'play', '--width', '11', '--height', '11']
    configs = ['--output', log_file, '-g', 'wrapped', '-m',
               'hz_islands_bridges', '--hazardDamagePerTurn', '100', '-v']
    game_stats = {'Average_game_duration': 0}

    # Launch snakes
    processes = []
    for snake in snakes:
        name = snake['name']
        player_type = snake['type']
        port = snake['port']
        params = snake['params']
        print(f'Launching {name} on port {port}')
        process = multiprocessing.Process(target=run_server, args=(
            port, player_type, params), daemon=True)
        process.start()
        processes.append(process)

        snake_command = ['--name', name, '--url', f'http://localhost:{port}']
        command += snake_command
        game_stats[f'{name}_wins'] = 0
        game_stats[f'{name}_win_rate'] = 0

    time.sleep(5)

    command += configs

    print(f'Running {game_count} games')
    print(f'Command: {command}')
    for i in range(game_count):
        print(f'Game {i+1}')
        # run bash command to run game
        result = subprocess.run(command)
        # load logged game data
        try:
            with open(log_file) as f:
                game_data = f.readlines()
            # get game stats
            winner = game_data[-1].strip().split(',')[1].split(':')[1].strip('"')
            length = len(game_data) - 2
            # update game_stats
            game_stats[f'{winner}_wins'] += 1
            game_stats['Average_game_duration'] += length
            print(winner)
        except:
            print('Error reading game data')
            print(result.stdout)
            print(result.stderr)

        # this flag is for logging terminal states to learning/state_values.txt when learning a value function
        # it will always log from the perspective of the player named Bayesian
        if log_state_values:
            print('Logging state values for learning')
            with open('learning/state_values.txt', 'a') as f:
                if winner == 'Bayesian':
                    # the first 4 places are for the state features and indicate a terminal state
                    # the last two features are state value and reward
                    f.write('-111, -111, -111, -111, -111, 1.0, 1.0\n')
                else:
                    f.write(
                        '-111, -111, -111, -111, -111, -1.0, -1.0\n')

    # snake servers requests to shut down
    for process in processes:
        process.terminate()
    processes = []

    # calculate win rates
    for snake in snakes:
        name = snake['name']
        game_stats[f'{name}_win_rate'] = game_stats[f'{name}_wins']/game_count

    game_stats['Average_game_duration'] = game_stats['Average_game_duration'] / game_count
    return game_stats
