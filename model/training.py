import chess
import tensorflow as tf
import numpy as np
from model.state import *

def get_data_from_game(pgn_location, is_white):
    game = chess.pgn.read_game(open(pgn_location))
    n = 0.0
    outcome = game.end().board().outcome()
    if outcome == chess.WHITE:
        if is_white:
            n = 1.0
        else: 
            n = 0.0
    elif outcome == chess.BLACK:
        if is_white:
            n = 0.0
        else:
            n = 1.0

    moves = game.mainline_moves()
    board = game.board()
    n = 0
    x_f = []
    y_f = []
    for move in moves:
        board.push(move)
        if (board.fen().split(" ")[1] == 'w') == is_white:
            x_f.append(np.array([fen_to_list(board.fen())]))
            y_f.append(np.array([[n]]))
    return tf.data.Dataset.zip(tf.data.Dataset.from_tensor_slices(x_f), tf.data.Dataset.from_tensor_slices(y_f))

def self_train(model, depth, discount, games_per_generation, epochs):
    x_f_white = []
    x_f_black = []
    y_f = []
    for i in range(games_per_generation):
        game = chess.pgn.Game()
        while not game.is_end():
            
            move = action.choose_best_move(model, game.end().board(), depth, discount)
            game.end().board().push(move)
            game.end().add_main_variation(move)
            if game.turn() == chess.WHITE:
                x_f_white.append(game.end().board().fen())
            if game.turn() == chess.BLACK:
                x_f_black.append(game.end().board().fen())
        
        