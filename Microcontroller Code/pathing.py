from collections import deque


def captured_piece():
    edges = [    # Top edge
    [(x, 0) for x in range(8)],
    # Right edge
    [(7, y) for y in range(8)],
    # Bottom edge
    [(x, 7) for x in range(8)],
    # Left edge
    [(0, y) for y in range(8)]]
    end = edges
    find_path(maze,start,end)
    move_motor(path_list)
def move_motor(path_list):
    for x in path_list:
        movement_dir = x[0]
        

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
