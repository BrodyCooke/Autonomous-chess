import heapq
import ujson
from collections import deque
import time
import os


class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, u, v, weight):
        #print('adding vertex u, ', u)
        #print('adding vertex v, ', v)

        self.add_vertex(u)  # Ensure vertices are added to the adjacency list
        #self.add_vertex(v)
        self.adj_list[u].append((v, weight))
        #self.adj_list[v].append((u, weight))

    def bfs_to_nearest_non_shortest_path_end(self, start, occupied, shortest_path):
        # Initialize a queue with the starting position and a visited set
        queue = deque([(start, [start])])  # Each queue element is a tuple (vertex, path_to_vertex)
        visited = set([start])
        visited.update(occupied)

        while queue:
            current_vertex, path_to_vertex = queue.popleft()

            # Check if the current vertex is a valid destination:
            # Not in shortest_path (for destinations only) and not occupied
            if current_vertex not in shortest_path and current_vertex not in occupied:
                return path_to_vertex  # Return the path leading to this vertex

            # Iterate over the neighbors of the current vertex
            for neighbor, _ in self.adj_list[current_vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Add the neighbor to the queue with the updated path
                    queue.append((neighbor, path_to_vertex + [neighbor]))

        # Return an empty list if no suitable end point is found
        return []


def dijkstra(graph, start):
    # Initialize distances to all nodes as infinity
    distances = {node: float('inf') for node in graph.adj_list}
    # Distance from start to start is 0
    distances[start] = 0
    # Initialize priority queue with (distance, node)
    priority_queue = [(0, start)]
    # Initialize dictionary to store the path
    path = {}
    
    while priority_queue:
        # Pop the node with the smallest distance from priority queue
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If we have already found a shorter path to current_node, skip
        if current_distance > distances[current_node]:
            continue
        
        # Explore neighbors of current_node
        for neighbor, weight in graph.adj_list[current_node]:
            distance = current_distance + weight
            # If a shorter path to neighbor is found, update distances and path
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                path[neighbor] = current_node
                # Add neighbor to priority queue
                heapq.heappush(priority_queue, (distance, neighbor))
    return path, distances

def find_shortestpath(graph, start, end_list):
    path, distances = dijkstra(graph,start)

    shortest_distance = 1000000
    best_end = None

    for end in end_list:
        if(distances[end] < shortest_distance):
            shortest_distance = distances[end]
            best_end = end
        

    # Reconstruct the shortest path from start to end
    shortest_path = []
    current = best_end
    while current in path:
        shortest_path.append(current)
        current = path[current]
    shortest_path.append(start)
    shortest_path.reverse()
    
    return shortest_path, shortest_distance


def convert_maze_to_graph(maze):
    rows = len(maze)
    cols = len(maze[0])
    graph = Graph()
    occupied = []
    unoccupied = []
    moveable = []

    for i in range(rows):
        for j in range(cols):
            vertex = (i, j)
            zero_neighbor_flag = 0
            graph.add_vertex(vertex)
            if maze[i][j] != 0:
                occupied.append(vertex)
            else:
                unoccupied.append(vertex)

            if i > 0:
                neighbor = (i - 1, j)
                if maze[i - 1][j] == 0:
                    cost = 1
                    zero_neighbor_flag = 1
                else:
                    cost = 101
                
                graph.add_edge(vertex, neighbor, cost)
            if i < rows - 1:
                neighbor = (i + 1, j)
                if maze[i + 1][j] == 0:
                    cost = 1
                    zero_neighbor_flag = 1
                else:
                    cost = 101
                graph.add_edge(vertex, neighbor, cost)
            if j > 0:
                neighbor = (i, j - 1)
                if maze[i][j - 1] == 0:
                    cost = 1
                    zero_neighbor_flag = 1
                else:
                    cost = 101
                graph.add_edge(vertex, neighbor, cost)
            if j < cols - 1:
                neighbor = (i, j + 1)
                if maze[i][j + 1] == 0:
                    cost = 1
                    zero_neighbor_flag = 1
                else:
                    cost = 101
                graph.add_edge(vertex, neighbor, cost)
            if zero_neighbor_flag:
                moveable.append(vertex)

    return graph, unoccupied, moveable


def find_path_help(maze,graph, moveable,start_vertex,end_vertexs,final_path):
    shortest_path, shortest_distance = find_shortestpath(graph, start_vertex, end_vertexs)
    final_path.append(shortest_path)

    num_inway = shortest_distance // 100
    found_num = 0
    found_list = []
    for square in shortest_path[1:]:
        if found_num >= num_inway:
                break
        if maze[square[0]][square[1]] != 0:
            found_num = found_num + 1
            found_list.append(square)
            


    #print('Occupied: ',occupied)
    print("\nStarting: ", start_vertex)
    print("Shortest Path:", shortest_path)
    print("Shortest Distance:", shortest_distance)

    print("Found ",num_inway,' in way at: ', found_list)


    movable_spaces = list(set(moveable) - set(shortest_path))
    #flat_final = [x for xs in final_path for x in xs]
    #movable_spaces = list(set(unoccupied) - set(flat_final))
    #print('Moveable: ',movable_spaces)
    for obstacle in found_list:
        #next_short_path, next_short_distance = find_shortestpath(graph, obstacle, movable_spaces)
        moveable = movable_spaces
        final_path = find_path_help(maze,graph,moveable,obstacle,movable_spaces,final_path)

    return final_path


def find_path(maze,start_vertex,end_vertex):
    new_maze = deepcopy(maze)

    '''find path to move piece, and any pices in the way'''
    graph, unoccupied, moveable = convert_maze_to_graph(new_maze)
    #print(moveable)
    final_path = []
    path_to_run = find_path_help(new_maze,graph, moveable,start_vertex,end_vertex,final_path)
    path_to_run.reverse()
    final_path = path_to_run
    print('\nFinal_path:' ,final_path)

    '''edit maze to reflect curret board state'''
    pieces_to_return = [1]
    loopingpath = final_path
    while len(pieces_to_return) > 0:
        print('Looping path: ',loopingpath)
        for move in loopingpath:
            tmp_piece = new_maze[move[0][0]][move[0][1]]
            new_maze[move[0][0]][move[0][1]] = 0 #start = 0
            new_maze[move[-1][0]][move[-1][1]] = tmp_piece #end = old start
        
        #print_maze(new_maze)
        graph, unoccupied, moveable = convert_maze_to_graph(new_maze)

        '''find path for return of any moved pieces'''
        pieces_to_return = loopingpath[:-1]
        paths_back = []
        paths_back_change = []

        return_path = []

        for piece in pieces_to_return:
            return_path = find_path_help(new_maze,graph, moveable,piece[-1],[piece[0]],[])
            paths_back_change.append(return_path)  #here for now til i figure out recursion

        loopingpath = []
        for path_list in paths_back_change:
            for elm in path_list:
                paths_back.append(elm)
                loopingpath.append(elm)

        print(paths_back)
        
        for path_list in paths_back:
            path_list.reverse()
            for elm in path_list:
                final_path.append(elm)

        print('\nFinal_path:' ,final_path)

    return final_path



def visulize_update(maze,path,clear=0):
    if clear == 1:
        pass
        #os.system('cls')
    print_maze(maze)
    time.sleep(5)
    for moves in path:
        for i in range(len(moves)-1):
            tmp = maze[moves[i][0]][moves[i][1]]
            maze[moves[i][0]][moves[i][1]] = 0
            maze[moves[i+1][0]][moves[i+1][1]] = tmp
            if clear == 1:
                pass
                #os.system('cls')
            print('Move: ',moves[i], ' to ', moves[i+1])
            print_maze(maze)
            if clear == 1:
                time.sleep(2)


def print_maze(maze):
    for row in maze:
        print(row)
    print('\n\n')
    
def deepcopy(obj):
    return ujson.loads(ujson.dumps(obj))


if __name__ == "__main__":

    maze = [[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]]
    
    # Specify start and end vertices
    start_vertex = (7, 1)
    end_vertex = [(5, 2)]

    path_to_run = find_path(maze,start_vertex,end_vertex)

    

    #visulize_update(maze,path_to_run,clear=1)