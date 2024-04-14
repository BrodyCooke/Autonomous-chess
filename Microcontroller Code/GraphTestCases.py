import graphshit as g

'''move bottom right knight'''
'''able to move to location'''
'''piece moves back!!!'''
def test1():
    maze = [[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]]
    
    # Specify start and end vertices
    start_vertex = (7, 6)
    end_vertex = [(5, 5)]

    path_to_run = g.find_path(maze,start_vertex,end_vertex)
    
    g.visulize_update(maze,path_to_run,clear=1)

'''move top left knight'''
'''able to move to location'''
'''piece moves back!!!'''
def test2():
    maze = [[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1]]
    
    # Specify start and end vertices
    start_vertex = (0, 1)
    end_vertex = [(2, 2)]
    
    path_to_run = g.find_path(maze,start_vertex,end_vertex)
    
    g.visulize_update(maze,path_to_run,clear=1)


'''scarry bishop move with way out'''
'''able to move to location'''
'''piece moves back!!!'''
def test3():
    maze = [[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,1,1,0,0,0,0],
            [1,1,1,0,0,1,1,1],
            [1,0,1,1,1,1,1,1]]
    
    # Specify start and end vertices
    start_vertex = (7, 2)
    end_vertex = [(4, 5)]

    path_to_run = g.find_path(maze,start_vertex,end_vertex)
    
    g.visulize_update(maze,path_to_run,clear=1)

'''scarry bishop move with no way out'''
'''able to move to location'''
'''moved peice gets stuck with no home'''
def test4():
    maze = [[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,1,1,0,0,1,0],
            [1,1,1,0,0,1,0,1],
            [1,0,1,1,1,1,1,1]]
    
    # Specify start and end vertices
    start_vertex = (7, 2)
    end_vertex = [(4, 5)]

    path_to_run = g.find_path(maze,start_vertex,end_vertex)
    
    g.visulize_update(maze,path_to_run,clear=1)

if __name__ == "__main__":
        test4()