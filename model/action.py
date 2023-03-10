import chess
import tensorflow as tf
from model.state import *
from model.policy import *
import numpy as np
def estimate_best_position(model : tf.keras.Model, board : chess.Board, depth, discount):
    s = []
    current_max, max_val = None, None
    moves = board.generate_legal_moves()
    for move in moves:
        c_board = chess.Board(board.fen())
        c_board.push(move)
        c_val = eval_future_states(model, c_board, depth, discount)
        s.append(c_val)
        if max_val == None or max_val < c_val:
            current_max = move
            max_val = c_val
    
    return [s, s.index(np.max(s)), current_max]

def choose_best_move(model, board, depth, discount):
    return estimate_best_position(model, board, depth, discount)[2]