import Hall_Effect
import LCD_timer
import Server_Conn 
from Server_Conn import server
import time
import Stepper

#Server API Works
Server_Conn.connWIFI('Chickennuggs','13221322')
server1 = server('192.168.188.30','5000')
server1.connect()
server1.waiting()


#LCD Works
x = input("Select Game Time: ")
LCD_timer.initialize(x)
while True:
    chess_move = Hall_Effect.find_change()
    index_move = chess_move.index(1)
    state_move = ['a2a4','b2b3','c2c4','d2d4','e2e4','g1h3']
    print(state_move[index_move])
    server1.send_move(str(state_move[index_move]))
    time.sleep(1)
    recv = server1.receive_move() # This returns once a message from server is recived
    print("Move from the Server is: ",recv)

    Stepper.rotate("y", -800, 6)  # rotates to show
    time.sleep(3)


