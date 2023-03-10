import chess
import tensorflow as tf

a_to_n = [["a",0],["b",8],["c",16],["d",24],["e",32],["f",40],["g",48],["h",56]]
def fen_to_list(fen):
    split_fen = fen.split(" ")
    ranks = split_fen[0].split("/")
    board = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]
    for i in range(8):
        file = 0
        rank = ranks[i]
        for character in rank:
            if character.isnumeric():
                file += int(character)
            else:
                n = 0
                match character:
                    case 'P':
                        n = 6
                    case 'R':
                        n = 5
                    case 'N':
                        n = 4
                    case 'B':
                        n = 3
                    case 'Q':
                        n = 2
                    case 'K':
                        n = 1
                    case 'p':
                        n = -6
                    case 'r':
                        n = -5
                    case 'n':
                        n = -4
                    case 'b':
                        n = -3
                    case 'q':
                        n = -2
                    case 'k':
                        n = -1
                board[i][file] = n
                file += 1
    n_board = []
    for i in range(8):
        n_board.extend(board[i])
    if split_fen[1] == 'w':
        n_board.append(1.0)
    elif split_fen[1] == 'b':
        n_board.append(-1.0)
    
    if split_fen[2].__contains__('K'):
        n_board.append(1.0)
    else:
        n_board.append(0.0)
    
    if split_fen[2].__contains__('Q'):
        n_board.append(1.0)
    else:
        n_board.append(0.0)
    
    if split_fen[2].__contains__('k'):
        n_board.append(1.0)
    else:
        n_board.append(0.0)
    
    if split_fen[2].__contains__('q'):
        n_board.append(1.0)
    else:
        n_board.append(0.0)
    
    if split_fen[3] == '-':
        n_board.append(-1.0)
    else:
        n = int(split_fen[3][1])-1
        for i in range(8):
            if split_fen[3][0] == a_to_n[i][0]:
                n += a_to_n[i][1]
        n_board.append(float(n-1))

    
    n_board.append(float(split_fen[4]))
    return n_board

