import chess
import tensorflow as tf
from model.state import *
import numpy as np


def eval_future_states(model : tf.keras.Model, board : chess.Board, depth, discount):
    if depth == 0:
        return 0
    moves = board.generate_legal_moves()
    r = 0
    for move in moves:
        c_board = chess.Board(board.fen())
        c_board.push(move)
        r += (1.0/discount)*(model_eval_board(model, c_board) + eval_future_states(model, c_board, depth-1, discount))
    return r




def create_model():
    layers = [
        tf.keras.Input(shape=(71,)), 
        tf.keras.layers.Dense(64,'swish'), 
        tf.keras.layers.Dense(64,'swish'), 
        tf.keras.layers.Dense(64,'swish'), 
        tf.keras.layers.Dense(32,'swish'), 

        tf.keras.layers.Dense(1)
    ]
    test_model = tf.keras.Sequential()
    test_model.compile(optimizer='sgd',loss='mse')

    return test_model

def model_eval_board(model, board):
    return model(np.array([fen_to_list(board.fen())]))[0][0].numpy()