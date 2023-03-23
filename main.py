
if __name__ == "__main__":
    from server import run_server

    value_function = '15_batches_5_games_10_data_each_linear_kernel_constant_depth_linear_regression_batch_2'
    run_server(8000, 'tree_search', [7,7,50,0.9,'mean',False,value_function], 'wrapped', 'islands_and_bridges', 100)


