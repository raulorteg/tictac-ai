# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 11:41:13 2020

@author: Raul Ortega Ochoa
"""

# class Node:
#     def __init__(self, state, parent, cost):
#         self.state = state # the filled in grid
#         self.parent = parent # previous grid state
#         self.cost = cost


# =================================================
def is_available(pos, grid):
    """
    Parameters
    ----------
    pos : tuple of two ints
        position to check if available.
    grid : list of list of ints
        grid system.
    Returns
    -------
     True if available
     False if not
    """
    x, y = pos
    cond = grid[x][y] == 0
    return bool(cond)

# =================================================
def is_final_state(grid):
    """
    Parameters
    ----------
    grid : list of lists of ints
        grid system. The state of the game 
        when its the ai's turn

    Returns
    -------
    is_final_state : boolean
        True if final state
        False if not final state
    winner : string
        None if game not finished
        "Tie" if tie
        "AI" if ai wins
        "User" if user wins
    """
    #### TODO: this is really inefficient, maybe better check for every point
    #### in the grid if has cells of the same color at both sides (3 in row)
    
    # check if everything is filled in 
    counter = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                counter += 1
    
    if counter == 0:
        any_pos_left = False
    else:
        any_pos_left = True
    
    # check winner patern in rows
    green_in_row, red_in_row = 0, 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                green_in_row += 1
                red_in_row = 0
            elif grid[i][j] == 2:
                red_in_row += 1
                green_in_row = 0
            else:
                red_in_row = 0
                green_in_row = 0
        if (green_in_row == 3):
            return True, "Human"
        elif (red_in_row == 3):
            return True, "AI"
        else:
                red_in_row = 0
                green_in_row = 0
    
    # check for winner pattern in columns
    green_in_row, red_in_row = 0, 0
    for j in range(len(grid[0])):
        for i in range(len(grid)):
            if grid[i][j] == 1:
                green_in_row += 1
                red_in_row = 0
            elif grid[i][j] == 2:
                red_in_row += 1
                green_in_row = 0
            else:
                red_in_row = 0
                green_in_row = 0
                break
        if (green_in_row == 3):
            return True, "Human"
        elif (red_in_row == 3):
            return True, "AI"
        else:
                red_in_row = 0
                green_in_row = 0
    
    # check for winner pattern in diagonals
    green_in_row, red_in_row = 0, 0
    for i in range(len(grid)): # principal diagonal
        if grid[i][i] == 1:
            green_in_row += 1
            red_in_row = 0
        elif grid[i][i] == 2:
            red_in_row += 1
            green_in_row = 0
        else:
            red_in_row = 0
            green_in_row = 0
            break
    if (green_in_row == 3):
            return True, "Human"
    elif (red_in_row == 3):
            return True, "AI"
        
    green_in_row, red_in_row = 0, 0
    for i in range(len(grid)): # the other diagonal
        if grid[-i-1][i] == 1:
            green_in_row += 1
            red_in_row = 0
        elif grid[-i-1][i] == 2:
            red_in_row += 1
            green_in_row = 0
        else:
            red_in_row = 0
            green_in_row = 0
            break
    if (green_in_row == 3):
            return True, "Human"
    elif (red_in_row == 3):
            return True, "AI"
    
    # if at this point there is no winner and no positions left then its a tie
    # otherwise the game is still not finished
    if any_pos_left:
        return False, None
    else:
        return True, "Tie"
    
#=============================================
def available_movements(grid):
    """
    Parameters
    ----------
    grid : list of list of ints
        grid system.
    Returns
    -------
    movements : list of tuples of two ints.
        list of all empty positions in the grid
    """
    movements = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                movements.append((i,j))
    return movements

# ===========================================
def compute_cost(node, user):
    """
    Description:
    ----------
        Returns the cost of the Node given. Returns the max
        cost from within the costs of his children (successors)
    Parameters
    ----------
    grid : grid
    user : boolean
        True if users turn
        False if computers turn
    Returns
    -------
    cost: int
        2 if human wins
        1 if tie
        0 if ai wins 
    """
    if user:
        color = 1 # green
    else:
        color = 2 # red
        
    winner_dict = {"Human": 2, "Tie": 1, "AI": 0}
    
    # check if the node is a final one
    grid = node
    is_final, winner = is_final_state(grid)
    if is_final:
        cost = winner_dict[winner]
        return cost
    # if node its not a final one
    cost_options = []
    movements = available_movements(grid)
    for movement in movements:
        temp = grid.copy()
        x, y = movement
        temp[x][y] = color
        
        new_node = temp
        
        # check if final
        is_final, winner = is_final_state(temp)
        if is_final:
            cost = winner_dict[winner]
            cost_options.append(cost)
        
        # if node not a final one
        cost_options.append(compute_cost(new_node, not user))
        
    if user:
        color = 1 # green
        return max(cost_options)
    else:
        color = 2 # red
        return min(cost_options)

# ============================================
def is_in_map(pos, grid_dim):
    """
    Parameters
    ----------
    pos : tuple of 2 ints 
        x, y coordinates in the grid system of current
        position
    grid_dim : tuple of ints
        x, y dimension of the grid system
    Returns
        true if pos in map
        false if not in map
    """
    (max_x, max_y) = grid_dim # unroll the dimensions
    (x, y) = pos # unroll the position coordinates
    
    x_in = (x <= max_x) & (x >= 0) # logical x in map
    y_in = (y <= max_y) & (y >= 0) # logical y in map
    return bool(x_in*y_in) # only true if both true

# =============================================

