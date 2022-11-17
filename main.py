import random
import sys
import typing


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server(8000, 'one_step_lookahead')
