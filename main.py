import chess
import model
import tensorflow as tf
import numpy as np
from model import policy
from model import action
from model import state
from model import training

model = policy.load_model('saved_models/model_second')
discount = 1.1
depth = 1
board = chess.Board()
#training.train_folder("./model/training_games/me_vs_ai_games", model, 100)

#training.train_folder("./model/training_games/awsute_online_games", model, 100)
training.self_train(model, depth, discount, 1, 100)
model.save('saved_models/model_second')

def playgame_vs_ai(model):
    board = chess.Board()
    while not board.is_game_over():
        playermove = input("Move: ")
        board.push_san(playermove)

        ai_move = action.choose_best_move(model, board, depth, discount)
        print("AI played: " + ai_move.__str__())
        board.push(ai_move)







playgame_vs_ai(model)
        