# importing packages

import numpy as np
import heapq
from heapq import heappush
from heapq import heappop

# initializing and checking solvability of puzzle
def initializing_and_checking_solvability():
    
    #initializing 
    initial_puzzle = np.random.choice (np.arange (9), size=(9), replace=False)
    
    # checking solvability
    count = 0 
    
    for i in range(8):
        for j in range(i+1, 9):
            if (initial_puzzle[i] > initial_puzzle[j]) and initial_puzzle[j] and initial_puzzle[i]:
                count += 1 
        
    polarity = count % 2
    
    if polarity == 0:
        return initial_puzzle
    else:
        return initializing_and_checking_solvability()
    
    
# calculating first heuristic
def calculating_first_heuristic(initial_puzzle):
    
    num_col = 3
    h1 = 0
    
    for i in range(3):
        for j in range(3):
            if initial_puzzle[i][j] != (i * num_col) + j:
                h1+=1
    
    return h1

# calculating second heuristic
def calculating_second_heuristic(initial_puzzle):
        
    num_col = 3
    h2 = 0
    
    for i in range(3):
        for j in range(3):
            if initial_puzzle[i][j] != (i * num_col) + j:
                for k in range(3):
                    for l in range(3):
                        row_idx = 0
                        col_idx = 0
                        if ((k * num_col) + l) == initial_puzzle[i][j]:
                            h2 += abs(k - i) + abs(l - j)
    return h2

# checks all legal moves that can be made 
def is_legal(i, j):
    if (i < 0 or i > 2 or j < 0 or j > 2):
        return False
    else:
        return True
    

def a_star_first_heuristic(first_board, goal_state):
    
    # adding initial board state to set of explored nodes
    explored_set = set()
    first_board = tuple(map(tuple, first_board))
    explored_set.add(first_board)
    
    first_board = np.array(first_board)
    
    # creating frontier
    priority_queue = []
    heapq.heapify(priority_queue)
    
    # adding initial board state to frontier
    h = calculating_first_heuristic(first_board)
    x = 0
    g = 0
    f = g + h
    heappush(priority_queue, (f, x, g, first_board))
    
    # while frontier is not empty 
    while priority_queue:
        
        # pop node with lowest f-value
        current_board = heapq.heappop(priority_queue)
        current_board_state = np.copy(current_board[3]) # get board state
        g = current_board[2] # get g-value
        
        # if goal state is reached, return depth (g-value)
        if np.array_equal(current_board_state, goal_state):
            branching_factor = round(x**(1/g), 2)
            return g, x, branching_factor
      
        g += 1
        
        # loop through all possible children
        for i in range(3):
            for j in range(3):
                if current_board_state[i][j] == 0:
                    if (is_legal(i-1, j)): #going up
                        child_board_up = np.copy(current_board_state)
                        child_board_up[i][j] = current_board_state[i-1][j]
                        child_board_up[i-1][j] = 0
                        h = calculating_first_heuristic(child_board_up)
                        f = g + h
                        child_board_up = tuple(map(tuple, child_board_up))
                        if child_board_up not in explored_set:
                            x += 1
                            explored_set.add(child_board_up)
                            child_board_up = np.array(child_board_up)
                            heappush(priority_queue, (f, x, g, child_board_up))
                            
                    if (is_legal(i+1, j)): #going down
                        child_board_down = np.copy(current_board_state)
                        child_board_down[i][j] = current_board_state[i+1][j]
                        child_board_down[i+1][j] = 0
                        h = calculating_first_heuristic(child_board_down)
                        f = g + h
                        child_board_down = tuple(map(tuple, child_board_down))
                        if child_board_down not in explored_set:
                            x += 1
                            explored_set.add(child_board_down)
                            child_board_down = np.array(child_board_down)
                            heappush(priority_queue, (f, x, g, child_board_down))
                            
                    if (is_legal(i, j-1)): #going left
                        child_board_left = np.copy(current_board_state)
                        child_board_left[i][j] = current_board_state[i][j-1]
                        child_board_left[i][j-1] = 0
                        h = calculating_first_heuristic(child_board_left)
                        f = g + h
                        child_board_left = tuple(map(tuple, child_board_left))
                        if child_board_left not in explored_set:
                            x += 1
                            explored_set.add(child_board_left)
                            child_board_left = np.array(child_board_left)
                            heappush(priority_queue, (f, x, g, child_board_left))
                            
                    if(is_legal(i, j+1)): #going right
                        child_board_right = np.copy(current_board_state)
                        child_board_right[i][j] = current_board_state[i][j+1]
                        child_board_right[i][j+1] = 0
                        h = calculating_first_heuristic(child_board_right)
                        f = g + h
                        child_board_right = tuple(map(tuple, child_board_right))
                        if child_board_right not in explored_set:
                            x += 1
                            explored_set.add(child_board_right)
                            child_board_right = np.array(child_board_right)
                            heappush(priority_queue, (f, x, g, child_board_right))
                            


def a_star_second_heuristic(first_board, goal_state):
    
    # adding initial board state to set of explored nodes
    explored_set = set()
    first_board = tuple(map(tuple, first_board))
    explored_set.add(first_board)
    
    first_board = np.array(first_board)
    
    # creating frontier
    priority_queue = []
    heapq.heapify(priority_queue)
    
    # adding initial board state to frontier
    h = calculating_second_heuristic(first_board)
    x = 0
    g = 0
    f = g + h
    heappush(priority_queue, (f, x, g, first_board))
    
    
    # while frontier is not empty 
    while priority_queue:
        
        # pop node with lowest f-value
        current_board = heapq.heappop(priority_queue)
        current_board_state = np.copy(current_board[3]) # get board state
        g = current_board[2] # get g-value
        
        # if goal state is reached, return depth (g-value)
        if np.array_equal(current_board_state, goal_state):
            branching_factor = round(x**(1/g), 2)
            return g, x, branching_factor
      
        g += 1
        
        # loop through all possible children
        for i in range(3):
            for j in range(3):
                if current_board_state[i][j] == 0:
                    if (is_legal(i-1, j)): # going up
                        child_board_up = np.copy(current_board_state)
                        child_board_up[i][j] = current_board_state[i-1][j]
                        child_board_up[i-1][j] = 0
                        h = calculating_second_heuristic(child_board_up)
                        f = g + h
                        child_board_up = tuple(map(tuple, child_board_up))
                        if child_board_up not in explored_set:
                            x += 1
                            explored_set.add(child_board_up)
                            child_board_up = np.array(child_board_up)
                            heappush(priority_queue, (f, x, g, child_board_up))
                            
                    if (is_legal(i+1, j)): # going down
                        child_board_down = np.copy(current_board_state)
                        child_board_down[i][j] = current_board_state[i+1][j]
                        child_board_down[i+1][j] = 0
                        h = calculating_second_heuristic(child_board_down)
                        f = g + h
                        child_board_down = tuple(map(tuple, child_board_down))
                        if child_board_down not in explored_set:
                            x += 1
                            explored_set.add(child_board_down)
                            child_board_down = np.array(child_board_down)
                            heappush(priority_queue, (f, x, g, child_board_down))
                            
                    if (is_legal(i, j-1)): # going left
                        child_board_left = np.copy(current_board_state)
                        child_board_left[i][j] = current_board_state[i][j-1]
                        child_board_left[i][j-1] = 0
                        h = calculating_second_heuristic(child_board_left)
                        f = g + h
                        child_board_left = tuple(map(tuple, child_board_left))
                        if child_board_left not in explored_set:
                            x += 1
                            explored_set.add(child_board_left)
                            child_board_left = np.array(child_board_left)
                            heappush(priority_queue, (f, x, g, child_board_left))
                            
                    if(is_legal(i, j+1)): # going right
                        child_board_right = np.copy(current_board_state)
                        child_board_right[i][j] = current_board_state[i][j+1]
                        child_board_right[i][j+1] = 0
                        h = calculating_second_heuristic(child_board_right)
                        f = g + h
                        child_board_right = tuple(map(tuple, child_board_right))
                        if child_board_right not in explored_set:
                            x += 1
                            explored_set.add(child_board_right)
                            child_board_right = np.array(child_board_right)
                            heappush(priority_queue, (f, x, g, child_board_right))
                            
                        
def main():
    h1_dict = {}
    h2_dict = {}
    
    for i in range(5000):
        # initializing a random solvable board
        first_board = initializing_and_checking_solvability()
        first_board = first_board.reshape(3,3)

        # goal state
        goal_state = np.array([0,1,2,3,4,5,6,7,8])
        goal_state = goal_state.reshape(3,3)

        # running A* with h1
        h1_results = a_star_first_heuristic(first_board, goal_state)
        h1_depth = h1_results[0]
        h1_nodes = h1_results[1]
        h1_bf = h1_results[2]
        
        if h1_depth not in h1_dict.keys():
            h1_dict[h1_depth] = [h1_nodes, h1_bf, 1]
        else:
            h1_values = h1_dict.get(h1_depth)
            h1_values[0] += h1_nodes
            h1_values[1] += h1_bf
            h1_values[2] += 1
            h1_dict[h1_depth] = [h1_values[0], h1_values[1], h1_values[2]]

        

        # running A* with h2
        h2_results = a_star_second_heuristic(first_board, goal_state)
        h2_depth = h2_results[0]
        h2_nodes = h2_results[1]
        h2_bf = h2_results[2]

        if h2_depth not in h2_dict.keys():
            h2_dict[h2_depth] = [h2_nodes, h2_bf, 1]
        else:
            h2_values = h2_dict.get(h2_depth)
            h2_values[0] += h2_nodes
            h2_values[1] += h2_bf
            h2_values[2] += 1
            h2_dict[h2_depth] = [h2_values[0], h2_values[1], h2_values[2]]
    
    for key in h1_dict.keys():
        h1_values = h1_dict.get(key)
        h1_values[0] = round(h1_values[0]/h1_values[2])
        h1_values[1] = round(h1_values[1]/h1_values[2], 2)
        
    for key in h2_dict.keys():
        h2_values = h2_dict.get(key)
        h2_values[0] = round(h2_values[0]/h2_values[2])
        h2_values[1] = round(h2_values[1]/h2_values[2], 2)
            
    print("h1: ", h1_dict)
    print("h2: ", h2_dict)
    
    
if __name__ == "__main__":
    main()
    
    