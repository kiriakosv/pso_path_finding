#=======================================================================
# Copyright (c) 2014 Kiriakos Velissariou
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
#=======================================================================

from random import randint
from random import random
from math import sqrt
from math import floor

class Particle:
    g_best = [0, 99, 99, 99, 99]
    CROSSOVER_PROB = 0.7
    MUTATION_PROB = 0.1
    W = 0.8
    C1 = 1.5
    C2 = 1.5
    VMAX = 1
    VMIN = -1
    XMAX = 99
    XMIN = 0
    THE_MAP = None
    T = 10
   
    def __init__(self):
        def starting_pos():
            """ Helper function for initializing the position of
            each particle
            """
            start = []
            for i in range(0, 3):
                start.append(randint(0, 99))
            start = [0] + start + [99]
            return start
            
        def starting_vel():
            """ Helper function for initializing the velocity of
            each particle
            """
            vel = []
            for i in range(0, 3):
                vel.append(randint(int(Particle.VMIN), int(Particle.VMAX)))
            vel = [0] + vel + [0]
            return vel

        self.v = starting_vel()
        self.x = starting_pos()
        self.p_best = self.x[:]
        self.fit = 0

            
    def update_velocity(self):
        """Updates the velocity of each dimension in the particle"""
        for i in range(1, len(self.v) - 1):
            vel = Particle.W * self.v[i] + Particle.C1 * random()\
             * (self.p_best[i] - self.x[i]) + Particle.C2 * random() * \
             (Particle.g_best[i] - self.x[i])
            if vel > Particle.VMAX:
                pass
            elif vel < Particle.VMIN:
                pass
            else:
                self.v[i] = vel
             
    def update_position(self):
        """Updates the position of each dimension in the particle"""
        for i in range(1, len(self.x) - 1):
            new_pos = int(floor((self.x[i] + self.v[i])))
            if new_pos > Particle.XMAX:
                pass
            elif new_pos < Particle.XMIN:
                pass
            else:
                self.x[i] = new_pos
                
 
    def mutate(self):
        """Changes some parts of x based on mutation probability"""
        for i in range(1, len(self.x) - 1):  #don't mutate start of goal
            dont_mutate = random()
            
            if Particle.MUTATION_PROB > dont_mutate:
                self.x[i] = randint(0, 99)
                    
                    
    def crossover(self, other_particle):
        """Takes two particles and exchanges part of the solution at
        a specific point
        """
        crossover_position = randint(1, len(self.x) - 1)
        new1_first_half = self.x[:crossover_position]
        new1_second_half = other_particle.x[crossover_position:]
        new = Particle()
        new.x = new1_first_half
        new.x.extend(new1_second_half)
        new.v = self.v
        new.fit = self.fit
        new.p_best = self.p_best
        return new
        
    @staticmethod   
    def squares_of_line(segment):
        """Returns the squares a line segment cuts"""
        squares = []
        x1 = segment[0] / 10
        y1 = segment[0] % 10
        x2 = segment[1] / 10
        y2 = segment[1] % 10
        y = y1
        x = x1
        dx = x2 - x1
        dy = y2 - y1
        squares.append(x * 10 + y)
        if dy < 0:
            ystep = -1
            dy = -dy
        else:
            ystep = 1
        if dx < 0:
            xstep = -1
            dx = -dx
        else:
            xstep = 1
        ddy = 2 * dy
        ddx = 2 * dx
        if ddx >= ddy:
            errorprev = dx
            error = dx
            for i in range(0, dx):
                x += xstep
                error += ddy
                if error > ddx:
                    y += ystep
                    error -= ddx
                    if error + errorprev < ddx:
                        squares.append(x * 10 + (y - ystep))
                    elif error + errorprev > ddx:
                        squares.append((x - xstep) * 10 + y)
                    else:
                        squares.append(x * 10 + (y - ystep))
                        squares.append((x - xstep) * 10 + y)
                squares.append(x * 10 + y)
                errorprev = error
        else:
            errorprev = dy
            error = dy
            for i in range(0, dy):
                y += ystep
                error += ddx
                if error > ddy:
                    x += xstep
                    error -= ddy
                    if error + errorprev < ddy:
                        squares.append((x - xstep) * 10 + y)
                    elif error + errorprev > ddy:
                        squares.append(x * 10 + (y - ystep))
                    else:
                        squares.append((x -xstep) * 10 + y)
                        squares.append(x * 10 + (y - ystep))
                squares.append(x * 10 + y)
                errorprev = error
        return squares
            
 
    @staticmethod    
    def obstacles_per_segment(list_of_segments):
        """Returns the number of obstacles a path crosses"""
        obstacles_per_segment = []
        for segment in list_of_segments:
            sqr = Particle.squares_of_line(segment)
            obstacles = 0
            for square in sqr:
                if Particle.THE_MAP[square] ==  1:
                    obstacles += 1
            #don't calculate the same obstacle twice
            if Particle.THE_MAP[segment[0]] == 1:
                obstacles -= 1
            obstacles_per_segment.append(obstacles)
        return obstacles_per_segment
            
    def calculate_fit(self, path):
        """Calculates the fit of a given path"""
        #break path into line segments
        line_segments = []
        for i in range(0, len(path) - 1):
            line_segments.append(path[i:i+2])
          
        #calculate euclidian distance of each line segment
        eucl_distances = []
        a_fit = 0
        obstacles = None
        for segment in line_segments:
            px = segment[0] / 10
            py = segment[0] % 10
            qx = segment[1] / 10
            qy = segment[1] % 10
            distance = sqrt((px - qx) ** 2 + (py - qy) ** 2)
            a_fit += distance
           
        obstacle_factor = []
        obstacles = Particle.obstacles_per_segment(line_segments)
        for nbr_of_obstacles in obstacles:
            if nbr_of_obstacles == 0:
                obstacle_factor.append(0)
            else:
                a = 0
                for i in range(1, nbr_of_obstacles + 1):
                    a += i
                obstacle_factor.append(a * Particle.T)
        for factor in obstacle_factor:
            a_fit += factor
        return a_fit
            
        
        
        
        
        
        
        
        
        
        
        
        
