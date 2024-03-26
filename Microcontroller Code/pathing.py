from collections import deque

# (row,col)
def captured_piece():
    edges = [[(x, 0) for x in range(8)], [(7, y) for y in range(8)], [(x, 7) for x in range(8)], [(0, y) for y in range(8)]]
    edges.remove(start) # removed self from edge list
    end = edges
    find_path(maze,start,end)
    
def move_piece(move_api):
    #already scanned
    # receive move from api 
    # server sends in format (start_loc,end_loc) (5,1)
    # scan hall effect - call get_current_board()
    # move_api is a tuple with (start_loc,end_loc) where start and end are ordered pairs (5,1)
    hE_board = get_current_board()
    start_loc = move_api(0)
    end_loc = move_api(1)
    emag_prev = get_emag_location() # pull previous emagnet location

    deactivate_emag()
    path_list = emag_path(emag_prev, start_loc) #previous emag location, move to location
    move_motor(path_list) # move emag to underneath desired piece to move
    update_emag_location(end_loc) # update emag location

    path_list = find_path(hE_board, start_loc,end_loc) # find the shortest path to move a piece through the board
    activate_emag()
    move_motor(path_list) # Move the piece through the board
    update_emag_location(end_loc)
    deactivate_emag()

def emag_path(start, end):
    x = start(0) - end(0)
    y = start(0) - end(0)
    path_list = []
    if(x > 0):
        for i in range(abs(x)):
            path_list.append((0,1)) #right
    elif(x<0):
        for i in range(abs(x)):
            path_list.append((0,-1)) #left
    
    if(y > 0):
        for i in range(abs(y)):
            path_list.append((1,0)) #up
    elif(y < 0):
        for i in range(abs(y)):
            path_list.append((-1,0)) #down
        


def move_motor(path_list):
    path_count = 1
    for i in range(len(path) -1):
        if path[i] == path[i+1]:
            path_count += 1
        else: 
            if(path[i] == (1,0)):
                #call x positive motor
                rotate("x", path_count) #rotate x
            elif(path[i] == (-1,0)):
                #call x negative motor
                rotate("x", -path_count) #rotate x
            elif(path[i] == (0,1)):
                #call y positive
                rotate("y", path_count) #rotate x
            elif(path[i] == (0,-1)):
                #call y negative
                rotate("y", -path_count) #rotate x
            else:
                print("Cry\n")
        
            pass
            # Move to Motor Code
            #call motors
    
        

def find_path(maze, start, end):
    def is_valid_move(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

    visited = set()
    queue = deque((), 64)  # Initialize deque with empty tuple and max length 20

    queue.append((start, []))  # Queue stores tuples of (position, path)

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) in end:
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

# Example usage:
maze = [
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
end = [(2, 3)]

path = find_path(maze, start, end)
if path:
    print("Maze solved! Shortest path found:", path)
else:
    print("No path found from start to end in the maze.")

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