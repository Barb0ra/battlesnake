import random
import sys
import typing

#2.0, 8.0, 6.0, 0.9, 'lcb'
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server(8000, 'tree_search', [2.0, 8.0, 3.0, 0.9, 'lcb'], 'standard', 'royale', 15)
