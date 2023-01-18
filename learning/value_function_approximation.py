import random
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
import joblib

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
        state_vectors.append(split_line[:6])
        values.append(split_line[6])
        rewards.append(split_line[7])

    # each game is separated by a terminal state: win '-111, -111, -111, -111, 1.0, 1.0\n' or lose '-111, -111, -111, -111, -1.0, -1.0\n'
    game_end_indices = []
    for i in range(len(state_vectors)):
        if state_vectors[i] == [-111, -111, -111, -111, -111, -111]:
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
    gp_value_fucntion = GaussianProcessRegressor()
    gp_value_fucntion.fit(state_vectors, td_lambda_targets)
    return gp_value_fucntion


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
        # append the game state vectors and td_lambda_targets
        if joined_state_vectors.size == 0:
            joined_state_vectors = game_state_vectors
            td_lambda_targets = game_td_lambda_targets
        else:
            joined_state_vectors = np.concatenate(
                (joined_state_vectors, game_state_vectors))
            td_lambda_targets = np.concatenate(
                (td_lambda_targets, game_td_lambda_targets))
    return joined_state_vectors, td_lambda_targets


def learn_first_batch(model_name, games_per_batch, sampling_rate, starting_alpha):
    # there are no pre-generated data and we need to start from a basic value function
    # play a game
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [2.0, 8.0, 6.0, 0.9,
                                                                                   'lcb', True, 'basic']}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]
    run_games(games_per_batch, snakes, GO_FILE_PATH, 'game_log.txt', True)
    # load the game state data
    state_vectors, values, rewards, game_end_indices = load_game_state_data()
    # calculate the td_lambda_targets
    state_vectors, td_lambda_targets = get_td_targets(
        state_vectors, values, rewards, game_end_indices)
    state_vectors, td_lambda_targets = sample_from_training_data(
        sampling_rate, state_vectors, td_lambda_targets)
    alphas = np.full(len(state_vectors), starting_alpha)
    # train a Gaussian Process to predict the td_lambda_targets
    gp_value_fucntion = train_gp(state_vectors, td_lambda_targets, alphas)
    # save the data
    np.save(VALUE_FUNCTION_FILE_PATH + 'state_vectors_' + model_name + '.npy', state_vectors)
    np.save(VALUE_FUNCTION_FILE_PATH + 'td_lambda_targets_' + model_name + '.npy', td_lambda_targets)
    np.save(VALUE_FUNCTION_FILE_PATH + 'alphas_' + model_name + '.npy', alphas)
    # save the Gaussian Process
    joblib.dump(gp_value_fucntion, model_name)
    return gp_value_fucntion


def learn_batch(model_name, games_per_batch, sampling_rate, alpha):
    # load the old data
    state_vectors = np.load(VALUE_FUNCTION_FILE_PATH + 'state_vectors_' + model_name + '.npy')
    td_lambda_targets = np.load(
        VALUE_FUNCTION_FILE_PATH + 'td_lambda_targets_' + model_name + '.npy')
    alphas = np.load(VALUE_FUNCTION_FILE_PATH + 'alphas_' + model_name + '.npy')
    # play a game
    snakes = [{'name': 'Bayesian', 'type': 'tree_search', 'port': 8000, 'params': [2.0, 8.0, 6.0, 0.9,
                                                                                   'lcb', True, 'basic']}, {'name': 'Baseline', 'type': 'one_step_lookahead', 'port': 8080, 'params': []}]
    run_games(games_per_batch, snakes, GO_FILE_PATH, 'game_log.txt', True)
    # load the game state data
    new_state_vectors, values, rewards, game_end_indices = load_game_state_data()
    # calculate the td_lambda_targets
    new_state_vectors, new_td_lambda_targets = get_td_targets(
        new_state_vectors, values, rewards, game_end_indices)
    new_state_vectors, new_td_lambda_targets = sample_from_training_data(
        sampling_rate, new_state_vectors, new_td_lambda_targets)
    # append the new data
    state_vectors = np.concatenate((state_vectors, new_state_vectors))
    td_lambda_targets = np.concatenate(
        (td_lambda_targets, new_td_lambda_targets))
    alphas = np.concatenate((alphas, np.full((len(new_state_vectors)), alpha)))
    # train a Gaussian Process to predict the td_lambda_targets
    gp_value_fucntion = train_gp(state_vectors, td_lambda_targets, alphas)
    # save the data
    np.save(VALUE_FUNCTION_FILE_PATH + 'state_vectors.npy', state_vectors)
    np.save(VALUE_FUNCTION_FILE_PATH + 'td_lambda_targets.npy', td_lambda_targets)
    np.save(VALUE_FUNCTION_FILE_PATH +'alphas.npy', alphas)
    # save the Gaussian Process
    joblib.dump(gp_value_fucntion, model_name)
    return gp_value_fucntion


def sample_from_training_data(sampling_rate, state_vectors, td_lambda_targets):
    # sample from the training data
    sampled_state_vectors = []
    sampled_td_lambda_targets = []
    for i in range(len(td_lambda_targets)):
        if random.random() < sampling_rate:
            sampled_state_vectors.append(state_vectors[i, :])
            sampled_td_lambda_targets.append(td_lambda_targets[i])
    return np.array(sampled_state_vectors), np.array(sampled_td_lambda_targets)


def learn_value_function(model_name, num_batches, games_per_batch, sampling_rate, starting_alpha, alpha_step_size):
    # learn the value function
    delete_old_game_state_data()
    gp_value_fucntion = learn_first_batch(
        model_name, games_per_batch, sampling_rate, starting_alpha)
    for i in range(num_batches-1):
        alpha = starting_alpha - alpha_step_size * (i+1)
        delete_old_game_state_data()
        gp_value_fucntion = learn_batch(
            model_name, games_per_batch, sampling_rate, alpha)
    return gp_value_fucntion


def delete_old_game_state_data():
    # delete old game state data
    with open(GAME_LOGS_FILE_PATH, 'w') as f:
        pass
