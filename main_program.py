import Hall_Effect
import Board as brd
import LCD_timer
from LCD_timer import LCD_time
import Server_Conn 
from Server_Conn import server
import Stepper
import pathing as pth

import time
import machine
from machine import Pin, Timer


#Server API Works
Server_Conn.connWIFI('Chickennuggs','13221322')
server1 = server('192.168.198.30','5000')
server1.connect()
server1.waiting()



# Initialize Button Interrupt
b_state = 0
pir = Pin(34,Pin.IN) #Button Interrupt
sens = brd.board()
print(sens.read_halleffects_once())
sens.update_emag_location((0,0))
#LCD = LCD_time('60')

def button_pressed(self):
    global b_state
    global server1
    
    print('in button iterupt')
    print(sens.read_halleffects_once())
    
    move = sens.find_change() #if no change or too much change
    move_valid = True
    if b_state != 0: # if it is not first turn 
        #LCD.paused()
        pass
    if move_valid == False:
        #power LED
        led_pow = 1
        #try another move
    #Needs to unpause bot first
    #LCD.unpause() 
    uci = Server_Conn.translate_toUCI(move)
    print('UCI : ',uci)
    server1.send_move(uci)
    move = server1.receive_move()
    move = Server_Conn.translate_fromUCI(move)
    print('UCI : ',move)
    #LCD.paused() # Pause Bot Move
    pth.move_piece(sens,move)
    #tmp code 
    time.sleep(5)
    print(sens.read_halleffects_once())
    #tmp code
    # Unpauses the player timer
    #LCD.unpaused()
    b_state = 1 # not initial button press
    
    
    

pir.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)
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