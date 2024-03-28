#from machine import ADC, Pin, Timer
import time


class board:

    def __init__(self):
        self.previous_board = []
        self.current_board = []
        self.emag_location = ()

        #adc_pin = Pin(14)
        #self.adc = ADC(adc_pin)


        #self.gpio_pin1 = Pin(32, Pin.OUT)
        #self.gpio_pin2 = Pin(27, Pin.OUT)
        #self.gpio_pin3 = Pin(13, Pin.OUT)

        self.States =[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1]]

    def get_current_board(self):
        return self.current_board
    
    def get_previous_board(self):
        return self.previous_board
    
    def get_emag_location(self):
        return self.emag_location
    
    def update_emag_location(self, location):
        self.emag_location = location

    def read_halleffects_once():
    values = []
    for x in States:
        gpio_pin1.value(x[0])
        gpio_pin2.value(x[1])
        gpio_pin3.value(x[2])
        time.sleep(.025)
        analog_value = adc.read()
        if analog_value > 2000:
            values.append(1)
        elif analog_value < 1500:
            values.append(-1)
        else:
            values.append(0)
    return values

        self.update_board(values)
        return values
    
    def update_board(self,board):
        self.previous_board = self.current_board
        self.current_board = board
        
    
    def find_change(self):
        board2 = self.current_board
        board1 = self.previous_board
        
        changes = []

        # Iterate over each cell in the mazes
        for row in range(len(board1)):
            for col in range(len(board1[row])):
                # Compare corresponding cells
                if board1[row][col] != board2[row][col]:
                    changes.append(((row, col), board1[row][col], board2[row][col]))

        print("Changes:")
        for change in changes:
            print(f"Position: {change[0]}, Value before: {change[1]}, Value after: {change[2]}")
        
        from_pos = None
        to_pos = None
        if len(changes) == 2:
            for change in changes:
                if change[2] == 0:
                    from_pos = change[0]
                else:
                    to_pos = change[0]
        else:
            raise('too many changes')
                    
        move = (from_pos,to_pos)
        print(move)
        return move
    
    
if __name__ == "__main__":


    maze1 = [
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [-1, 0, -1, -1, 0],
    [0, 0, -1, 0, 0]
    ]

    maze2 = [
    [0, 1, 0, 1, 0],
    [0, 1, -1, 1, 0],
    [0, 0, 0, 0, 0],
    [-1, 0, 0, -1, 0],
    [0, 0, -1, 0, 0]
    ]
    
    #init
    sens = board()
    sens.update_board(maze1)
    
    
    #button intr
    sens.update_board(maze2)
    sens.find_change()
    
    #call server code
    
    #server reply
    
    #move piece from server
    
    
    