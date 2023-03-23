import random
import numpy as np
import joblib
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, DotProduct
from learning.parameter_tuning import tune_parameters

from learning.run_games import run_games

GO_FILE_PATH = '../battlesnake_rules/battlesnake'
GAME_LOGS_FILE_PATH = 'learning/state_values.txt'
VALUE_FUNCTION_FILE_PATH = 'learning/value_functions/'

def load_game_state_data():
    # load state value and reward information from state_values.txt
    state_vectors = []
    values = []
    rewards = []
    with open(GAME_LOGS_FILE_PATH, 'r') as f:
        data = f.readlines()
    for line in data:
        split_line = line.strip().split(', ')
        # convert to float
        split_line = [float(x) for x in split_line]
        state_vectors.append(split_line[:5])
        values.append(split_line[5])
        rewards.append(split_line[6])

    # each game is separated by a terminal state: win '-111, -111, -111, -111, 1.0, 1.0\n' or lose '-111, -111, -111, -111, -1.0, -1.0\n'
    game_end_indices = []
    for i in range(len(state_vectors)):
        if state_vectors[i] == [-111, -111, -111, -111, -111]:
            game_end_indices.append(i)

    return state_vectors, values, rewards, game_end_indices

def get_td_targets_per_game(state_vectors, values, rewards):
    # calculate td_lambda_targets
    td_lambda_targets = np.zeros(len(state_vectors))
    lambda_value = 0.9
    lambda_coefficient = 1 - lambda_value
    td_depth = 0
    discounting_factor = 0.9
    # calculate td_lambda_targets
    # td_lambda_target[1] = (1-lambda) * G1(S1) + (1-lambda)*lambda*G2(S1) + (1-lambda)*lambda^2*G3(S1) + ... + (1-lambda)*lambda^(n-1)*Gn(S1)
    # where Gn(S1) = R1 + R2 + R3 + ... + Rn + V(Sn) with discounting
    while td_depth < 50:
        for i in range(len(state_vectors)):
            # calculate td_lambda_target for a given depth and state
            Gn = 0
            # n is the last index we read from
            n = min(i + td_depth + 1, len(state_vectors) - 1)
            for j in range(i+1, n):
                Gn += discounting_factor ** (j - i - 1) * rewards[j]
            # check if we reached a terminal state
            # if not, take the value, if yes, take the reward
            if i + td_depth < len(state_vectors):
                Gn += discounting_factor ** (n - i - 1) * values[n]
            else:
                Gn += discounting_factor ** (n - i - 1) * rewards[n]

            td_lambda_targets[i] += lambda_coefficient * Gn
        lambda_coefficient *= lambda_value
        td_depth += 1
    return td_lambda_targets

def train_gp(state_vectors, td_lambda_targets, alpha):
    # train a Gaussian Process to predict the td_lambda_targets
    gp_value_function = GaussianProcessRegressor(alpha=alpha, kernel=DotProduct(sigma_0 = 0, sigma_0_bounds = 'fixed')+ConstantKernel(constant_value=0.25, constant_value_bounds = (0.1,1))*RBF(length_scale = 3, length_scale_bounds = 'fixed'))
    gp_value_function.fit(state_vectors, td_lambda_targets)
    return gp_value_function

def get_td_targets(state_vectors, values, rewards, game_end_indices):
    joined_state_vectors = np.array([])
    for i in range(len(game_end_indices)):
        if i == 0:
            game_state_vectors = state_vectors[:game_end_indices[i]+1]
            game_values = values[:game_end_indices[i]+1]
            game_rewards = rewards[:game_end_indices[i]+1]
        else:
            game_state_vectors = state_vectors[game_end_indices[i-1] +
                                               1:game_end_indices[i]+1]
            game_values = values[game_end_indices[i-1]+1:game_end_indices[i]+1]
            game_rewards = rewards[game_end_indices[i-1] +
                                   1:game_end_indices[i]+1]
        game_td_lambda_targets = get_td_targets_per_game(
            game_state_vectors, game_values, game_rewards)
        # the last state vector is the terminal state and should not be used for training
        game_state_vectors = np.array(game_state_vectors[:-1])
        game_td_lambda_targets = np.array(game_td_lambda_targets[:-1])
        # subtract from the game_end_index to keep it accurate with the erased terminal state vectors
        game_end_indices[i] -= (i+1)
        # append the game state vectors and td_lambda_targets
        if joined_state_vectors.size == 0:
            joined_state_vectors = game_state_vectors
            td_lambda_targets = game_td_lambda_targets
        else:
            joined_state_vectors = np.concatenate(
                (joined_state_vectors, game_state_vectors))
            td_lambda_targets = np.concatenate(
                (td_lambda_targets, game_td_lambda_targets))
    return joined_state_vectors, td_lambda_targets, game_end_indices

def learn_first_batch(model_name, games_per_batch, sampling_rate, starting_alpha):
    # there are no pre-generated data and we need to start from a basic value function
    # play a game
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [7, 7, 50, 0.9,
                                                                                   'mean', True, 'basic']}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]
    run_games(games_per_batch, snakes, GO_FILE_PATH, 'game_log.txt', True)
    # load the game state data
    state_vectors, values, rewards, game_end_indices = load_game_state_data()
    # calculate the td_lambda_targets
    state_vectors, td_lambda_targets, game_end_indices = get_td_targets(
        state_vectors, values, rewards, game_end_indices)
    state_vectors, td_lambda_targets = sample_from_training_data_except_game_ends(
        sampling_rate, state_vectors, td_lambda_targets, game_end_indices)
    alphas = np.full(len(state_vectors), starting_alpha)
    # train a Gaussian Process to predict the td_lambda_targets
    gp_value_function = train_gp(state_vectors, td_lambda_targets, alphas)
    # save the data
    save_training_data(state_vectors, td_lambda_targets, alphas, model_name)
    # save the Gaussian Process
    joblib.dump(gp_value_function, VALUE_FUNCTION_FILE_PATH + model_name + '.joblib')
    # save intermediate result
    joblib.dump(gp_value_function, VALUE_FUNCTION_FILE_PATH + model_name + '_batch_0.joblib')
    return gp_value_function

def learn_batch(model_name, games_per_batch, sampling_rate, alpha, batch_number):
    # load the old data
    state_vectors, td_lambda_targets, alphas = load_training_data(model_name)
    # play a game
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [7,7,50, 0.9,
                                                                                   'mean', True, model_name]}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]
    run_games(games_per_batch, snakes, GO_FILE_PATH, 'game_log.txt', True)
    # load the game state data
    new_state_vectors, values, rewards, game_end_indices = load_game_state_data()
    # calculate the td_lambda_targets
    new_state_vectors, new_td_lambda_targets, new_game_end_indices = get_td_targets(
        new_state_vectors, values, rewards, game_end_indices)
    new_state_vectors, new_td_lambda_targets = sample_from_training_data_except_game_ends(
        sampling_rate, new_state_vectors, new_td_lambda_targets, new_game_end_indices)
    # append the new data
    state_vectors = np.concatenate((state_vectors, new_state_vectors))
    td_lambda_targets = np.concatenate(
        (td_lambda_targets, new_td_lambda_targets))
    alphas = np.concatenate((alphas, np.full((len(new_state_vectors)), alpha)))
    # train a Gaussian Process to predict the td_lambda_targets
    gp_value_function = train_gp(state_vectors, td_lambda_targets, alphas)
    # save the data
    save_training_data(state_vectors, td_lambda_targets, alphas, model_name)
    # save the Gaussian Process
    joblib.dump(gp_value_function, VALUE_FUNCTION_FILE_PATH + model_name + '.joblib')
    # Also save the intermediate result
    joblib.dump(gp_value_function, VALUE_FUNCTION_FILE_PATH + model_name + '_batch_' + str(batch_number) + '.joblib')
    return gp_value_function

def save_training_data(state_vectors, td_lambda_targets, alphas, model_name):
    # save the data
    np.save(VALUE_FUNCTION_FILE_PATH + 'state_vectors_' + model_name + '.npy', state_vectors)
    np.save(VALUE_FUNCTION_FILE_PATH + 'td_lambda_targets_' + model_name + '.npy', td_lambda_targets)
    np.save(VALUE_FUNCTION_FILE_PATH + 'alphas_' + model_name + '.npy', alphas)

def load_training_data(model_name):
    # load the data
    state_vectors = np.load(VALUE_FUNCTION_FILE_PATH + 'state_vectors_' + model_name + '.npy')
    td_lambda_targets = np.load(
        VALUE_FUNCTION_FILE_PATH + 'td_lambda_targets_' + model_name + '.npy')
    alphas = np.load(VALUE_FUNCTION_FILE_PATH + 'alphas_' + model_name + '.npy')
    return state_vectors, td_lambda_targets, alphas

def sample_from_training_data(sampling_rate, state_vectors, td_lambda_targets):
    # sample from the training data
    sampled_state_vectors = []
    sampled_td_lambda_targets = []
    for i in range(len(td_lambda_targets)):
        if random.random() < sampling_rate:
            sampled_state_vectors.append(state_vectors[i, :])
            sampled_td_lambda_targets.append(td_lambda_targets[i])
    return np.array(sampled_state_vectors), np.array(sampled_td_lambda_targets)

def sample_from_training_data_except_game_ends(sampling_rate, state_vectors, td_lambda_targets, game_end_indices):
    # get all indices representing the last 5 moves of a game
    last_5_moves_indices = []
    for i in range(len(game_end_indices)):
        last_5_moves_indices.extend(
            list(range(game_end_indices[i]-5, game_end_indices[i]+1)))
    # sample from the training data but include entire game ends
    sampled_state_vectors = []
    sampled_td_lambda_targets = []
    for i in range(len(td_lambda_targets)):
        if i in last_5_moves_indices:
            sampled_state_vectors.append(state_vectors[i, :])
            sampled_td_lambda_targets.append(td_lambda_targets[i])
        elif random.random() < sampling_rate:
            sampled_state_vectors.append(state_vectors[i, :])
            sampled_td_lambda_targets.append(td_lambda_targets[i])
    return np.array(sampled_state_vectors), np.array(sampled_td_lambda_targets)

def learn_value_function(model_name, num_batches, games_per_batch, sampling_rate, starting_alpha, alpha_step_size):
    # learn the value function
    delete_old_game_state_data()
    gp_value_function = learn_first_batch(
        model_name, games_per_batch, sampling_rate, starting_alpha)
    # evaluate the model
    tune_parameters(model_name, 7, 50, 'one_step_lookahead')
    
    for i in range(1, num_batches):
        alpha = starting_alpha - alpha_step_size * (i)
        delete_old_game_state_data()
        gp_value_function = learn_batch(
            model_name, games_per_batch, sampling_rate, alpha, i)
        # evaluate the model every other batch
        if i % 2 == 0:
            tune_parameters(model_name, 7, 50, 'one_step_lookahead')
    return gp_value_function

def delete_old_game_state_data():
    # delete old game state data
    with open(GAME_LOGS_FILE_PATH, 'w') as f:
        pass

def learn_batch_from_old(model_name, old_model_name, games_per_batch, sampling_rate, alpha):
    delete_old_game_state_data()
    # play games with the old model
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [7,7,50, 0.9,
                                                                                   'mean', True, old_model_name]}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]
    run_games(games_per_batch, snakes, GO_FILE_PATH, 'game_log.txt', True)
    # load the game state data
    state_vectors, values, rewards, game_end_indices = load_game_state_data()
    # calculate the td_lambda_targets
    state_vectors, td_lambda_targets, game_end_indices = get_td_targets(
        state_vectors, values, rewards, game_end_indices)
    state_vectors, td_lambda_targets = sample_from_training_data_except_game_ends(
        sampling_rate, state_vectors, td_lambda_targets, game_end_indices)

    alphas = np.full((len(state_vectors)), alpha)
    # train a Gaussian Process to predict the td_lambda_targets
    gp_value_function = train_gp(state_vectors, td_lambda_targets, alphas)
    # save the data
    save_training_data(state_vectors, td_lambda_targets, alphas, model_name)
    # save the Gaussian Process
    joblib.dump(gp_value_function, VALUE_FUNCTION_FILE_PATH + model_name + '.joblib')
    return gp_value_function

def learn_in_separate_batches(model_name, num_batches, games_per_batch, sampling_rate, starting_alpha, alpha_step_size):
    model_names = ['10_independent_batches_of_20_games_batch_9']
    for i in range(0, num_batches):
        model_names.append(model_name + '_batch_' + str(10 + i))
    for i in range(1, num_batches+1):
        learn_batch_from_old(model_names[i], model_names[i-1], games_per_batch, sampling_rate, starting_alpha - alpha_step_size * i)
        # evaluate the model
        tune_parameters(model_names[i], 7, 50, 'one_step_lookahead')
