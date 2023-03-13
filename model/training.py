import chess
import chess.pgn
import tensorflow as tf
import numpy as np
import model as m
import os

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
    x_f = []
    y_f = []
    for move in moves:
        board.push(move)
        if (board.fen().split(" ")[1] == 'w') == is_white:
            x_f.append(np.array([m.state.fen_to_list(board.fen())]))
            y_f.append(np.array([[n]]))
    return tf.data.Dataset.zip((tf.data.Dataset.from_tensor_slices(x_f), tf.data.Dataset.from_tensor_slices(y_f)))

def self_train(model, depth, discount, games_per_generation, epochs):
    data_set = None
    length = 0
    for i in range(games_per_generation):
        x_f = []
        x_f_white = []
        x_f_black = []
        y_f = []
        board = chess.Board()
        while not board.is_game_over():            
            move = m.action.choose_best_move(model, board, depth, discount)
            print(move)
            board.push(move)
            fen = np.array([m.state.fen_to_list(board.fen())])
            if board.turn == chess.WHITE:
                x_f_white.append(fen)
            if board.turn == chess.BLACK:
                x_f_black.append(fen)
        
        w = np.array([[0.5]])
        b = np.array([[0.5]])
        if board.outcome() == chess.BLACK:
            w = np.array([[0.0]])
            b = np.array([[1.0]])
        elif board.outcome() == chess.WHITE:
            w = np.array([[1.0]])
            b = np.array([[0.0]])
        for o in range(len(x_f_white)):
            y_f.append(w)
        for o in range(len(x_f_black)):
            y_f.append(b)
        x_f.extend(x_f_white)
        x_f.extend(x_f_black)
        length += len(x_f)
        x_f = tf.data.Dataset.from_tensor_slices(x_f)
        y_f = tf.data.Dataset.from_tensor_slices(y_f)
        zipped_data = tf.data.Dataset.zip((x_f,y_f))
        if data_set == None:
            data_set = zipped_data
        else: 
            data_set = data_set.concatenate(zipped_data)
        #model.fit(data_set, batch_size=length, epochs=epochs)
        print("game# " + str(i))
    model.fit(data_set, batch_size=length, epochs=epochs)
    
    print(data_set)

def train_pgn(model, location, epochs):
    data = get_data_from_game(location, True)
    model.fit(data, batch_size=data.__len__(), epochs=epochs)
    
    data = get_data_from_game(location, False)
    model.fit(data, batch_size=data.__len__(), epochs=epochs)


def train_folder(folder_path, model, epochs):
    data = None
    for filepath in os.listdir(folder_path):
        data1 = get_data_from_game(folder_path+"/"+filepath, True)
        data2 = get_data_from_game(folder_path+"/"+filepath, False)
        if data == None:
            data = data1.concatenate(data2)
        else:
            data = data.concatenate(data1.concatenate(data2))
    model.fit(data, batch_size=data.__len__(), epochs=epochs)