
from stockfish import Stockfish

stockfish = Stockfish(r'stockfish\stockfish-windows-x86-64.exe')
stockfish.update_engine_parameters({"Hash": 2048, "UCI_Chess960": "true"}) 
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # Sets up a board at the original spots
#print(stockfish.get_board_visual())

def call_api(player_move):
    stockfish.make_moves_from_current_position([player_move])
    api_move = stockfish.get_best_move()
    return api_move

# move_input = input("Input Chess Move in UCI Format: ")
# print(move_input)
# x = call_api(move_input)
# print(x)
# #print(stockfish.get_board_visual())
# move_input = stockfish.get_best_move()
# print(move_input)
# perform_move(move_input,1)
#print(stockfish.get_board_visual())

#print(stockfish.get_top_moves(3))


# Example usage:
""" board = chess.Board()
player = chess.WHITE  # Replace with chess.BLACK if you want black's best move

best_move = get_best_move(board, player)
print("Best Move for Player:", chess.COLOR_NAMES[player])
print(best_move.uci())  # UCI format provides a concise representation of the move

# Does not work :( """