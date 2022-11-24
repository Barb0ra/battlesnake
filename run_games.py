import json
import subprocess
import sys
import threading
import time

from server import run_server

GO_FILE_PATH = '../battlesnake_rules/battlesnake'

snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080}]

def run_games(game_count, snakes):

    command = [GO_FILE_PATH, 'play', '--width', '11', '--height', '11']
    configs = ['--output', 'out.log', '-g', 'wrapped', '-m', 'hz_islands_bridges', '--hazardDamagePerTurn', '100', '-v']
    game_stats = {'Average_game_duration':0}
    
    # Launch snakes
    for snake in snakes:
        name = snake['name']
        player_type = snake['type']
        port = snake['port']
        print(f'Launching {name} on port {port}')
        thread = threading.Thread(target=run_server, args=(port, player_type), daemon=True).start()
        snake_command = ['--name', name, '--url', f'http://localhost:{port}']
        command += snake_command
        game_stats[f'{name}_wins'] = 0
        game_stats[f'{name}_win_rate'] = 0

    time.sleep(0.5)
  
    command += configs

    print(f'Running {game_count} games')
    print(f'Command: {command}')
    for i in range(game_count):
        print(f'Game {i+1}')
        #run bash command to run game
        result = subprocess.run(command)
        #load logged game data
        with open('out.log') as f:
            game_data = f.readlines()
        #get game stats
        winner = game_data[-1].strip().split(',')[1].split(':')[1].strip('"')
        length = len(game_data) - 2
        #update game_stats
        game_stats[f'{winner}_wins'] += 1
        game_stats['Average_game_duration'] += length
        print(winner)
    #calculate win rates
    for snake in snakes:
        name = snake['name']
        game_stats[f'{name}_win_rate'] = game_stats[f'{name}_wins']/game_count

    game_stats['Average_game_duration'] = game_stats['Average_game_duration'] / game_count
    #write game_stats to file
    with open('game_stats.json', 'w') as f:
        json.dump(game_stats, f)




run_games(1, snakes)
    