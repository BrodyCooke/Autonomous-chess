from machine import ADC, Pin, Timer
import time


class board:

    def __init__(self):
        self.previous_board = []
        self.current_board = []
        self.emag_location = (0,0)

        adc_pin = Pin(35)
        self.adc = ADC(adc_pin)


        self.gpio_pin1 = Pin(5, Pin.OUT)
        self.gpio_pin2 = Pin(4, Pin.OUT)
        self.gpio_pin3 = Pin(2, Pin.OUT)
        
        '''feather'''
        '''
        adc_pin = Pin(36)
        self.adc = ADC(adc_pin)


        self.gpio_pin1 = Pin(14, Pin.OUT)
        self.gpio_pin2 = Pin(32, Pin.OUT)
        self.gpio_pin3 = Pin(15, Pin.OUT)
        '''

        self.States =[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]]

    def get_current_board(self):
        return self.current_board
    
    def get_previous_board(self):
        return self.previous_board
    
    def get_emag_location(self):
        return self.emag_location
    
    def update_emag_location(self, location):
        self.emag_location = location

    def read_halleffects_once(self):
        
        board = []
        values = []
        for x in self.States:
            
            self.gpio_pin1.value(x[0])
            self.gpio_pin2.value(x[1])
            self.gpio_pin3.value(x[2])
            time.sleep(.025)
            analog_value = self.adc.read()
            #print(analog_value)
            if analog_value > 2000:
                values.append(1)
            #elif analog_value < 1500:
            #    values.append(-1)
            else:
                values.append(0)
                
            #print(self.States.index(x))
            if ((self.States.index(x) ) % 3 == 2 or self.States.index(x) == len(self.States)-1):
                #print('hello')
                #print(values)
                while len(values) <3:
                    values.append(1)
                board.append(values)
                values = []
        board.reverse()
        self.update_board(board)
        return board
    
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
        if len(changes) <= 2:
            for change in changes:
                if change[2] == 0:
                    from_pos = change[0]
                else:
                    to_pos = change[0]
        else:
            #raise('too many changes')
            print('Changes WENT WRONG')
            print(changes)
                    
        move = (from_pos,to_pos)
        print(move)
        return move
    
    
if __name__ == "__main__":


    maze1 = [
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 1]
    ]

    maze2 = [
    [0, 1, 0],
    [0, 0, 0],
    [0, 0, 1]
    ]
    
    #init
    sens = board()
    print(sens.read_halleffects_once())
    
    #call server code
    
    #server reply
    
    #move piece from server
    
    #print('test')
    #print(sens.read_halleffects_once())
    
    