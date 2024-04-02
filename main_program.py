import Hall_Effect
import LCD_timer
from LCD_timer import LCD_time as LCD
import Server_Conn 
from Server_Conn import server
import time
import Stepper
import machine
from machine import Pin, Timer
import pathing as pth
import board as brd


#Server API Works
Server_Conn.connWIFI('Chickennuggs','13221322')
server1 = server('192.168.140.30','5000')
server1.connect()
server1.waiting()



# Initialize Button Interrupt
b_state = 0
pir = Pin(34,Pin.IN) #Button Interrupt

def button_pressed(self):
    brd.read_halleffects_once()
    move = brd.findchange() #if no change or too much change
    if b_state != 0: # if it is not first turn 
        LCD.paused()
    if move_valid == False:
        #power LED
        led_pow = 1
        #try another move
    #Needs to unpause bot first
    LCD.unpaused() 
    uci = server.translate_toUCI(move)
    server.send_move(uci)
    move = server.receive_move()
    server.translate_fromUCI(move)
    LCD.paused() # Pause Bot Move
    pth.move_piece(move)
    # Unpauses the player timer
    LCD.unpaused()
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