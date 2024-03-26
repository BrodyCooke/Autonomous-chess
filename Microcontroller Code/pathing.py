from collections import deque

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
    
