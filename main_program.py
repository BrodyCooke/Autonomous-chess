import Board as brd
import LCD_timer
from LCD_timer import LCD_time
import Server_Conn 
from Server_Conn import server
import Stepper
import pathing as pth
import graphshit as g

import time
import machine
from machine import Pin, Timer, SoftI2C
import pcf8575 

#Server API Works
Server_Conn.connWIFI('Chickennuggs','13221322')
server1 = server('192.168.91.30','5000')
server1.connect()
playtype,gametime = server1.waiting()

# Initialize Button Interrupt
b_state = 0
pir = Pin(34,Pin.IN) #Button Interrupt
sens = brd.board()
print(sens.read_halleffects_once())
sens.update_emag_location((0,0))
maze = [[-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]]
sens.update_board(maze)
i2c_set = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
gpio_i2c_addr = 0x20
pcf = pcf8575.PCF8575(i2c_set, 0x20)
Stepper.pcf = pcf
#LCD = LCD_time(gametime,i2c_set)

if playtype == 'spectator_player':
    print('starting spectator code')
    spec_move_list = []
    while True:
        recv = server1.spectator()
        for i in range(len(spec_move_list), len(recv)):
            move = recv[i]
            move = Server_Conn.translate_fromUCI(move)
            print('UCI : ',move)
            pth.move_piece(sens,move)


def button_pressed(self,pcf):
    global server1
    global b_state
    print('in button iterupt')
    print(sens.read_halleffects_once())
    
    #move = sens.find_change() #if no change or too much change
    move_valid = True
    pcf.pin(2,0)
    if b_state != 0: # if it is not first turn
        
        LCD.pause()
    try:
        move = sens.find_change()
        if len(move) != 2:
            move_valid = False
            pcf.pin(2,1)
            sens.update_board(sens.get_previous_board())
    except Exception as e:
        print(e)
        move_valid = False
        pcf.pin(2,1)
        sens.update_board(sens.get_previous_board())
        return # would we break to get out of function as a whole?
        #try another move
    if move_valid == False:
        return
    #Needs to unpause bot first
    LCD.unpause() 
    uci = Server_Conn.translate_toUCI(move)
    print('UCI : ',uci)
    serv_move = server1.send_move(uci)
    if serv_move == 'invalid':
        move_valid = False
        print(move_valid)
        pcf.pin(2,1)
        sens.update_board(sens.get_previous_board())
        return
    # Check valid
    move = server1.receive_move()
    move = Server_Conn.translate_fromUCI(move)
    print('UCI : ',move)
    LCD.pause() # Pause Bot Move
    pth.move_piece(sens,move)
    #tmp code 
    time.sleep(5)
    print(sens.read_halleffects_once())
    #tmp code
    # Unpauses the player timer
    LCD.unpause()
    b_state = 1 # not initial button press

if playtype == 'white_player' or 'black_player':
    while True:
        new_bstate = pir.value()
        if (new_bstate == 1) and (b_state == 0):
            button_pressed(pcf)
    
    

#pir.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)
#Button Pressed 
#     Scan (Done) 
#     On Button:
#         Scan
#         check valid move
#             turn on red light
#             wait for button hit
#         translate move (start Timer for API)
#         send move 
#         receive move (api)
#         translate move(stop Timer for API)
#         move piece (this updates all variables)
#         Start Player timer (Wait for player button press)

#LCD Works
'''
x = input("Select Game Time: ")
LCD_timer.initialize(x)

while True:
    chess_move = Hall_Effect.find_change() # Hall Effect detect move
    index_move = chess_move.index(1) 
    state_move = ['a2a4','b2b3','c2c4','d2d4','e2e4','g1h3'] #Simple board positions
    print(state_move[index_move])

    start = time.time_ns() # Timer to detect the API/server response time
    server1.send_move(str(state_move[index_move]))
    time.sleep(1)
    recv = server1.receive_move() # This returns once a message from server is recived
    print("Move from the Server is: ",recv)
    end = time.time_ns()
    print("Time to receive API: ",(end - start)/1000000000.0, " seconds")
    Stepper.activate_electromagnet()
    Stepper.rotate("y", -900, 6)  # rotates a distance (will rotate the specific distance required to move piece to correct location)
    Stepper.deactivate_electromagnet()
    time.sleep(3)
    '''

'''testing pathing'''
'''
sens = brd.board()
print(sens.read_halleffects_once())

move = ((0, 0), (0, 1))

pth.move_piece(sens,move)
'''

if __name__ == "__main__":
    pass
'''
    maze = [[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]]
    
    start_vertex = (7, 1)
    end_vertex = [(5, 2)]
    
    
    path_to_run = g.find_path(maze,start_vertex,end_vertex)
    
    final_path = []
    for elm in path_to_run:
        for i in range(len(elm)-1):
            final_path.append((elm[i+1][0]-elm[i][0],elm[i+1][1]-elm[i][1]))
    
        
    pth.move_motor(final_path)
'''
    