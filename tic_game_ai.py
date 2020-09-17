# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:31:04 2020

@author: Raul Ortega Ochoa
"""
import pygame
import numpy as np
from time import sleep
from tic_helper import compute_cost, available_movements, is_final_state



class Node:
    def __init__(self, state, parent, cost):
        self.state = state # the filled in grid
        self.parent = parent # previous grid state
        self.cost = cost

# define grid dimensions
num_rows = 3
num_columns = num_rows

# =======================================================
# SETTINGS FOR PYGAME

# define colors of the grid RGB
black = (0, 0, 0) # background
white = (255, 255, 255) # grid == 0, not selected
green = (50,205,50) # grid == 1, selected by player
red = (255,99,71) # grid == 2, selected by AI

# set the height/width of each location on the grid
height = 60
width = height # i want the grid square
margin = 5 # sets margin between grid locations


# initialize pygame
pygame.init()

# congiguration of the window
WINDOW_SIZE = [200, 200]
screen = pygame.display.set_mode(WINDOW_SIZE)
# screen title
pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock() # to manage how fast the screen updates

# initialize blanck grid system
grid = []
for i in range(num_rows):
    grid.append([])
    for j in range(num_columns):
        grid[i].append(0) # corresponds to white color
        
interrupt = False
valid_input = False
user_turn = True # user starts the game

# main painting loop
while not interrupt:
    user_turn = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            interrupt = True
            
        ###### USERS TURN  
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (user_turn):
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change to grid coordinates
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            # check if valid, if valid then paint it green
            if grid[row][column] != 0:
                valid_input = False
            else:
                user_turn = False # dont allow to click more than once
                grid[row][column] = 1
                
                # create the Node
                node = Node(grid, None, None)
                valid_input = True
    
    screen.fill(black) # fill background in black
    
    for row in range(num_rows):
        for column in range(num_columns):
                
            if grid[row][column] == 1:
                color = green
                pygame.draw.rect(screen, color,
                                 [(margin + width) * column + margin,
                                  (margin + height) * row + margin,
                                  width,
                                  height])
            elif grid[row][column] == 2:
                color = red
                pygame.draw.rect(screen, color,
                                 [(margin + width) * column + margin,
                                  (margin + height) * row + margin,
                                  width,
                                  height])
            else:
                color = white
                pygame.draw.rect(screen, color, 
                                 [(margin + width) * column + margin, 
                                  (margin + height) * row + margin,
                                  width,
                                  height])
    
    # set limit to 60 frames per second
    clock.tick(60)
    
    # update screen
    pygame.display.flip()
    
    if (valid_input == True):
        # check if final state
        is_final, winner = is_final_state(grid)
        if is_final:
            print(f"Winner is {winner}")
            interrupt = True
            break
        print("it is not final state yet")   
        # see what are the options
        movements = available_movements(grid)
        
        # compute the cost for each option
        cost_options = []
        for movement in movements:
            temp = grid
            x, y = movement
            temp[x][y] = 2 # AI moves (suppose)
        
            new_node = Node(temp, node, None)
            cost_options.append(compute_cost(new_node))
        print(f"Possible movements: {movements}")
        print(f"This are my cost options: {cost_options}")
        index = np.argmin(cost_options)
        next_x, next_y = movements[index]
        print(f"My next movement is {(next_x, next_y)}")
        grid[next_x][next_y] = 2
        print(grid)
        print()
        
        sleep(1)
        
        
        
    
quit_button  = False
while not quit_button:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_button = True
pygame.quit() # so that it doesnt "hang" on exit