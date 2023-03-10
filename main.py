import chess
import model
import tensorflow as tf
import numpy as np
from model import policy
from model import action
from model import state
from model import training

model = policy.create_model()
discount = 1.1
depth = 1
board = chess.Board()

print(action.estimate_best_position(model, board, depth, discount))