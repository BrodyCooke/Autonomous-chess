from collections import deque
'''import Board
import Stepper
import time
'''
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
    hE_board = sens.get_current_board() #from Hall Effect sensor Code
    start_loc = move_api[0]
    end_loc = move_api[1]
    emag_prev = sens.get_emag_location() # pull previous emagnet location (From board.py code)

    Stepper.deactivate_electromagnet()

    path_list = emag_path(emag_prev, start_loc) #previous emag location, move to location
    move_motor(path_list) # move emag to underneath desired piece to move\
    print('Mag Path ',path_list)
    time.sleep(1)

    #Stepper.rotate("y", 200, 2) 

    sens.update_emag_location(start_loc) # update emag location

    path_list = find_path(hE_board, start_loc,end_loc) # find the shortest path to move a piece through the board
    Stepper.activate_electromagnet()
    print('Piece Path ',path_list)
    move_motor(path_list) # Move the piece through the board
    time.sleep(1)
    #Stepper.rotate("y", -200, 2) 
    sens.update_emag_location(end_loc)
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
                Stepper.move("y", -path_count) #rotate x
            elif(path_list[i] == (-1,0)):
                #call x negative motor
                Stepper.move("y", path_count) #rotate x
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
                Stepper.move("y", -path_count) #rotate x
            elif(path_list[i] == (-1,0)):
                #call x negative motor
                Stepper.move("y", path_count) #rotate x
            elif(path_list[i] == (0,1)):
                #call y positive
                Stepper.move("x", path_count) #rotate x
            elif(path_list[i] == (0,-1)):
                #call y negative
                Stepper.move("x", -path_count) #rotate x
            else:
                print("Cry\n")
        
            pass
            # Move to Motor Code
            #call motors
        
        
def move_obs(maze,start,end,final_path):
    dir_to_travel = (0,0)
    y_change = (start[0]-end[0])
    x_change = (start[1]-end[1])
    if(abs(y_change) >= abs(x_change)):
        if(y_change > 0):
            dir_to_travel = (-1,0)
        else:
            dir_to_travel = (1,0)
    else:
        if(x_change > 0):
            dir_to_travel = (0,-1)
        else:
            dir_to_travel = (0,1)
    print('Dir: ',dir_to_travel)
    
    start2 = (start[0]+dir_to_travel[0],start[1]+dir_to_travel[1])
    end2 = (start[0]+2*dir_to_travel[0],start[1]+2*dir_to_travel[1])
    start = start2
    end = end2

    print('values: ',start,' ',end)
        
    tmp_val = maze[start[0]][start[1]]
    maze[start[0]][start[1]]=0
    maze[end[0]][end[1]]=tmp_val

    final_path.append((start2,end2,dir_to_travel))

    return maze, start, end, final_path

def find_path(maze, start, end):
    orig_start = start
    orig_end = end
    final_path = []
    path = find_path_help(maze,start,end)
    while path == None:
        maze,start,end,final_path = move_obs(maze,start,end,final_path)

        print(maze)
        path = find_path_help(maze,orig_start,orig_end)
        print('path inside: ', path)
    final_path.append((orig_start,orig_end,path))
    
    to_reverse = final_path[0:-1]
    to_reverse.reverse()
    print(to_reverse)
    for val in to_reverse:
        final_path.append((val[1],val[0],(-1*val[2][0],-1*val[2][1])))
    return final_path

    
    
def find_path_help(maze, start, end):
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

    '''looking to move peices out of the way'''
    
    maze = [[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]]
    
    print('Path: ', find_path(maze,(0,2),(2,1)))


