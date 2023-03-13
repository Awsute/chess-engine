import chess
import tensorflow as tf
from model.state import *
import numpy as np


def eval_future_states(model : tf.keras.Model, board : chess.Board, depth, discount):
    if depth == 0:
        return 0
    moves = board.generate_legal_moves()
    r = 0
    i = 1
    for move in moves:
        i += 1
        c_board = chess.Board(board.fen())
        c_board.push(move)
        r += model_eval_board(model, c_board)+(1.0/discount)*eval_future_states(model, c_board, depth-1, discount)
    print(board.fen() + ": " + str(r/i))
    return r/i




def create_model():
    layers = [
        tf.keras.Input(shape=(71,)),
        tf.keras.layers.Dense(65,'swish'),
        tf.keras.layers.Dense(10,'swish'),
        tf.keras.layers.Dense(1, 'relu')
    ]
    test_model = tf.keras.Sequential(layers)
    test_model.compile(optimizer='sgd',loss='mse')

    return test_model

def load_model(path):
    return tf.keras.models.load_model(path)
def model_eval_board(model, board):
    return model(np.array([fen_to_list(board.fen())]))[0][0].numpy()