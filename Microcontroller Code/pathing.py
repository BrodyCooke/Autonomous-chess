from collections import deque
import Board
import Stepper
import graphshit as g
import time


# (row,col)
def captured_piece():
    edges = [[(x, 0) for x in range(8)], [(7, y) for y in range(8)], [(x, 7) for x in range(8)], [(0, y) for y in range(8)]]
    edges.remove(start) # removed self from edge list
    end = edges

    find_path(maze,start,end)
    
def move_piece(sens,move_api):
    #already scanned
    # receive move from api 
    # server sends in format (start_loc,end_loc) (5,1)
    # scan hall effect - call get_current_board()
    # move_api is a tuple with (start_loc,end_loc) where start and end are ordered pairs (5,1)
    #hE_board = sens.get_current_board() #from Hall Effect sensor Code
    start_loc = move_api[0]
    end_loc = move_api[1]
    '''code for spec game only'''
    hE_board = sens.get_current_board()
    
    tmp = hE_board[start_loc[0]][start_loc[1]]
    hE_board[start_loc[0]][start_loc[1]] = 0
    hE_board[end_loc[0]][end_loc[1]] = tmp
    
    sens.update_board(hE_board)
    
    print(sens.get_current_board())
    
    path = g.find_path(hE_board,start_loc,[end_loc])
    for piece in path:
        emag_prev = sens.get_emag_location() # pull previous emagnet location (From board.py code)
        Stepper.deactivate_electromagnet()
        
        emag_start = piece[0]
        path_list = emag_path(emag_prev, emag_start) #previous emag location, move to location
        print('Mag Path ',path_list)
        move_motor(path_list) # move emag to underneath desired piece to move\
        sens.update_emag_location(emag_start) # update emag location
        
        Stepper.activate_electromagnet()
        piecepath = []
        for i in range(len(piece)-1):
            piecepath.append((piece[i+1][0]-piece[i][0],piece[i+1][1]-piece[i][1]))
        print('Piece Path ',piecepath)
        time.sleep(1)
        move_motor(piecepath) # Move the piece through the board
        time.sleep(1)
        #Stepper.rotate("y", -200, 2) 
        sens.update_emag_location(piece[-1])
        Stepper.deactivate_electromagnet()
        # Pass to player
        # Start Timer

def emag_path(start, end):
    x = start[0] - end[0]
    y = start[1] - end[1]
    print("emag: ", x, ' ',y)
    path_list = []
    if(y > 0):
        for i in range(abs(y)):
            path_list.append((0,-1)) #up
            
    elif(y<0):
        for i in range(abs(y)):
            path_list.append((0,1)) #down
    
    if(x > 0):
        for i in range(abs(x)):
            path_list.append((-1,0)) #left
    elif(x < 0):
        for i in range(abs(x)):
            path_list.append((1,0)) #right
            
    print('Emag Path ', path_list)
            
    return path_list
        


def move_motor(path_list):
    print('moving motor: ',path_list)
    path_count = 1
    for i in range(len(path_list)):
        if (i == len(path_list)-1):
            if(path_list[i] == (1,0)):
                #call x positive motor
                Stepper.move("y", path_count) #rotate x
            elif(path_list[i] == (-1,0)):
                #call x negative motor
                Stepper.move("y", -path_count) #rotate x
            elif(path_list[i] == (0,1)):
                #call y positive
                print('call y pos')
                Stepper.move("x", path_count) #rotate x
            elif(path_list[i] == (0,-1)):
                #call y negative
                Stepper.move("x", -path_count) #rotate x
            else:
                print("Cry\n")
        elif path_list[i] == path_list[i+1]:
            path_count += 1
        else: 
            if(path_list[i] == (1,0)):
                #call x positive motor
                Stepper.move("y", path_count) #rotate x
                path_count = 1
            elif(path_list[i] == (-1,0)):
                #call x negative motor
                Stepper.move("y", -path_count) #rotate x
                path_count = 1
            elif(path_list[i] == (0,1)):
                #call y positive
                Stepper.move("x", path_count) #rotate x
                path_count = 1
            elif(path_list[i] == (0,-1)):
                #call y negative
                Stepper.move("x", -path_count) #rotate x
                path_count = 1
            else:
                print("Cry\n")
        
            pass
            # Move to Motor Code
            #call motors
    
        
'''
def find_path(maze, start, end):
    def is_valid_move(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

    visited = set()
    queue = deque((), 64)  # Initialize deque with empty tuple and max length 20

    queue.append((start, []))  # Queue stores tuples of (position, path)

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        
        if (x, y) in visited:
            continue

        visited.add((x, y))

        # Possible moves: Up, Down, Left, Right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(new_x, new_y):
                queue.append(((new_x, new_y), path + [(dx, dy)]))

    return None
'''
# Steps needed: Change maze map to 8x8 with a 9th of all twos
# 
# Add tuple for stacking same moves
# Add an extra spot to drag captured pieces to.
# def captured_piece(piece_to_capture, captured_piece):   Shortest path to end with array
# def get_board_state():
# 
#
#
#
#
#
#
#
#
#
#
#
#
if __name__ == "__main__":

    sens = Board.board()
    sens.update_emag_location((0,0))

    move = ((7, 1), (5, 2))
    move_piece(sens,move)

