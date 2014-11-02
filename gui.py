#=======================================================================
# Copyright (c) 2014 Kiriakos Velissariou
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
#=======================================================================

import pygame
from classes import *
from pso_ga import *

def start():
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
 
    pygame.init()
 
    #Set the width and height of the screen [width, height]
    size = (401, 401)

    #Set the width, height and margin of the squares.
    width = 39
    height = 39
    margin = 1

    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("PSO-GA Algorithm")
 
    #Loop until the user clicks the close button.
    done = False
 
    #Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #Create a 10*10 arrray of numbers
    grid = []
    for row in range(10):
        grid.append([])
        for column in range(10):
            grid[row].append(0)

    grid[0][0] = 2
    grid[9][9] = 3

    # A list that holds the obstacles the user chose
    OBSTACLES = []

    # Population of the swarm
    population = 0

    # Max number of generations
    generations = 0

    # This variable checks if the pso-ga algorithm finished
    algorithm_finished = False
    print "Enter the obstacles by clicking the corresponding square. \
When finished press SPACE."
    print ""
 
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # )lag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                a = int(x /(width + margin))
                b = int(y / (height + margin))
                if (a == 0 and b == 0) or (a == 9 and b == 9):
                    pass
                else:
                    if grid[b][a] == 0:
                        grid[b][a] = 1
                    else:
                        grid[b][a] = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for i in range(0, 10):
                    for j in range(0, 10):
                        if (grid[j][i] == 1) and ((10 * j + i)\
                        not in OBSTACLES):
                            OBSTACLES.append(10 * j + i)
                try :
                    population = int(raw_input("Enter swarm population (recommended value: 100): "))
                    generations = int(raw_input("Enter max \
number of generations (recommended value: 150): "))
                except ValueError:
                    print "Invalid Input! The population is set to 100. \
Max number of generations is set to 150."
                    population = 100
                    generations = 150
         
                sol = algorithm(population, generations, OBSTACLES)
                algorithm_finished = True

                # Find the coordinates of the line segments
                segs = []
                if sol != False:
                    for point in sol:
                        x = point % 10
                        y = point / 10
                        x = ((x + 1) * (width)) - 20 + x * margin
                        y = ((y + 1) * (height)) - 20 + y * margin
                        segs.append([x, y])

 
        screen.fill(BLACK)
        for row in range(10):
            for column in range(10):
                if grid[row][column] == 1:
                    color = BLACK
                elif grid[row][column] == 2:
                    color = GREEN
                elif grid[row][column] == 3:
                    color = RED
                else:
                    color = WHITE
                pygame.draw.rect(screen, color, (margin + (column * \
                (margin + width)), (margin + height) * row + margin,\
                width, height))
                if algorithm_finished:
                    if sol != False:
                        pygame.draw.aalines(screen, BLUE, False, segs)
                    else:
                        segs = [[20, 20], [40, 40]]
                        pygame.draw.aalines(screen, RED, False, segs)
                        

 
        pygame.display.flip()
 
        #Limit to 60 frames per second
        clock.tick(60)
 
    # Close the window and quit.
    pygame.quit()
