
from stockfish import Stockfish
import json

class API:
    def __init__(self):
        self.stockfish = Stockfish(r'stockfish\stockfish-windows-x86-64.exe')
        self.stockfish.update_engine_parameters({"Hash": 2048, "UCI_Chess960": "true", "UCI_LimitStrength": 'true'}) 
        self.stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # Sets up a board at the original spots
        #self.stockfish.set_elo_rating(600)
        #self.stockfish.set_depth(10)
        #self.stockfish.set_skill_level(0)
        print(json.dumps(self.stockfish.get_parameters(), indent = 4))


    def get_api_move(self):
        api_move = self.stockfish.get_best_move(10)
        #print(api_move)
        self.stockfish.make_moves_from_current_position([api_move])
        return api_move
    
    def make_playermove(self,player_move):
        self.stockfish.make_moves_from_current_position([player_move])
    
    def board_state(self):
        print(self.stockfish.get_fen_position())

if __name__ == "__main__":
    API = API()
    move_input = input("Input Chess Move in UCI Format: ")
    print(move_input)
    x = API.call_api(move_input)
    print(x)
    move_input = input("Input Chess Move in UCI Format: ")
    x = API.call_api(move_input)
    print(x)
    move_input = input("Input Chess Move in UCI Format: ")
    x = API.call_api(move_input)
    print(x)
    print(API.stockfish.get_board_visual())