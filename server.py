import logging
import os
import typing

from flask import Flask
from flask import request

from players.heuristic_player import HeuristicPlayer
from players.random_player import RandomPlayer
from players.self_preserving_player import SelfPreservingPlayer
from players.tree_search_player import TreeSearchPlayer
from players.one_step_lookahead_player import OneStepLookaheadPlayer



def start(game_state: typing.Dict, player, player_name):
    print("GAME START")
    if player_name == 'tree_search':
        player.search_tree.root_state = None


def end(game_state: typing.Dict):
    print("GAME OVER\n")


def run_server(port, player_name, params, game_type='wrapped', game_map='islands_and_bridges', hazard_damage=100):
    players = {
        'tree_search': TreeSearchPlayer,
        'random': RandomPlayer,
        'self_preserving': SelfPreservingPlayer,
        'heuristic': HeuristicPlayer,
        'one_step_lookahead': OneStepLookaheadPlayer
    }
    player = players[player_name](params, game_type, game_map, hazard_damage)
    handlers = {
        "info": player.info,
        "start": start,
        "move": player.move,
        "end": end
    }

    app = Flask("Battlesnake")

    @app.get("/")
    def on_info():
        return handlers["info"]()

    @app.post("/start")
    def on_start():
        game_state = request.get_json()
        handlers["start"](game_state, player, player_name)
        return "ok"

    @app.post("/move")
    def on_move():
        game_state = request.get_json()
        return handlers["move"](game_state)

    @app.post("/end")
    def on_end():
        game_state = request.get_json()
        handlers["end"](game_state)
        return "ok"

    @app.after_request
    def identify_server(response):
        response.headers.set(
            "server", "battlesnake/github/starter-snake-python"
        )
        return response

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", port))

    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print(f"\nRunning Battlesnake at http://{host}:{port}")
    app.run(host=host, port=port)
