from machine import ADC, Pin, Timer
import time

def printlist(final_list):
        for value in final_list:
            print (value)
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
        self.gpio_pin4 = Pin(13, Pin.OUT)
        self.gpio_pin5 = Pin(14, Pin.OUT)
        self.gpio_pin6 = Pin(17, Pin.OUT)
        
        '''feather'''
        '''
        adc_pin = Pin(36)
        self.adc = ADC(adc_pin)


        self.gpio_pin1 = Pin(14, Pin.OUT)
        self.gpio_pin2 = Pin(32, Pin.OUT)
        self.gpio_pin3 = Pin(15, Pin.OUT)
        '''

        self.States = [[1,1,1],[1,0,1],[0,1,1],[0,0,1],[0,1,0],[1,0,0],[0,0,0],[1,1,0]]
        self.New_States = [[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]]

    def get_current_board(self):
        return self.current_board
    
    def get_previous_board(self):
        return self.previous_board
    
    def get_emag_location(self):
        return self.emag_location
    
    def update_emag_location(self, location):
        self.emag_location = location

    def read_halleffects_once(self):
        values = []
        values2 = []

        temp_list = []
        for i in self.New_States:
            self.gpio_pin4.value(i[2])
            self.gpio_pin5.value(i[1])
            self.gpio_pin6.value(i[0])
            temp_list = []
            temp_list2 = []

            for x in self.States:
                self.gpio_pin1.value(x[2])
                self.gpio_pin2.value(x[1])
                self.gpio_pin3.value(x[0])
                #time.sleep(.025)
                time.sleep(.5)
                analog_value = self.adc.read()
                print(analog_value)
                temp_list2.append(analog_value)
                '''
                var1 = 2250
                var2 = 1900
                if analog_value > var1:
                    temp_list.append(1)
                elif analog_value < var2:
                    temp_list.append(-1)
                else:
                    temp_list.append(0)
                '''
                if i == [0,0,0]:
                    print('State 1')
                    if analog_value > 2230:
                        temp_list.append(1)
                    elif analog_value < 1980:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                elif i == [1,0,0]:
                    print('State 2')
                    if analog_value > 2500:
                        temp_list.append(1)
                    elif analog_value < 1900:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                elif i == [0,1,0]:
                    print('State 3')
                    if analog_value > 2300:
                        temp_list.append(1)
                    elif analog_value < 1900:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                elif i == [1,1,0]:
                    print('State 4')
                    if analog_value > 2220:
                        temp_list.append(1)
                    elif analog_value < 1900:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                elif i == [0,0,1]:
                    print('State 5')
                    if analog_value > 2200:
                        temp_list.append(1)
                    elif analog_value < 1900:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                elif i == [1,0,1]:
                    print('State 6')
                    if analog_value > 2200:
                        temp_list.append(1)
                    elif analog_value < 1900:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                elif i == [0,1,1]:
                    print('State 7')
                    if analog_value > 2200:
                        temp_list.append(1)
                    elif analog_value < 1900:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                else:
                    print('State 8')
                    if analog_value > 2320:
                        temp_list.append(1)
                    elif analog_value < 1900:
                        temp_list.append(-1)
                    else:
                        temp_list.append(0)
                        
            values.append(temp_list)
            values2.append(temp_list2)
                
        printlist(values)
        printlist(values2)
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
    
    