#=======================================================================
# Copyright (c) 2014 Kiriakos Velissariou
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
#=======================================================================

from classes import *

CROSSOVER_PROB = 0.7

def instantantiate(pop):
    """Takes the number of particles and returns a swarm of particles"""
    print "Initializing swarm..."
    swarm = []
    for i in range(0, pop):
        swarm.append(Particle())
    print "Swarm initialized."
    return swarm
   
def instantantiate_map(obstacles):
    """ Takes the positions of the obstacles and returns a new map. A
    free position is denoted with a 0, an obstacle is denoted with 1
    """
    new_map = []
    for i in range(0, 100):
        if i in obstacles:
            new_map.append(1)
        else:
            new_map.append(0)
    return new_map 
    
        
def selection(swarm):
    """Performs a selection of particles for the next generation.
    Particles with higher fitness hava a higher probability of being
    selected
    """
    #The following algorithm of selection found in the following page
    #http://arxiv.org/pdf/1308.4675.pdf
    #each step is marked below
    
    #Probability of each chromosome to be selected
    fit_r = []
    for particle in swarm:
        fit_r.append(1/particle.fit)
    
    #Probability over total probability
    fit_r_sum = sum(fit_r)
    selection_probability = []
    for relative_fit in fit_r:
        selection_probability.append(relative_fit/fit_r_sum)
        
    #Cumulative probability
    cumulative_probability = []
    the_sum = 0
    for a in selection_probability:
        the_sum += a
        cumulative_probability.append(the_sum)
    
    #For the new generation, we compare a random number between 0 and 1
    #and we select the particle that has the next greater cumulative
    #probability
    probability = random()
    for i in range(0, len(cumulative_probability)):
        if probability <= cumulative_probability[i]:
            new_kid = swarm[i]
            break
    #Make new copy
    a_new_kid = Particle()
    a_new_kid.v = new_kid.v[:]
    a_new_kid.x = new_kid.x[:]
    a_new_kid.p_best = new_kid.p_best[:]
    return a_new_kid
        
def find_best_fit(swarm):
    """Returns the particle with the best fit in the swarm
    in order to perform elitism.
    """
    fitt = []
    for particle in swarm:
        fitt.append(particle.fit)
    minimum = min(fitt)
    index_of_min = fitt.index(minimum)
    return swarm[index_of_min]
    

def remove_duplicates(path):
    """Takes a path and returns it with duplicate nodes removed."""
    final_path = []
    final_path.append(0)
    for i in range(1, len(path) - 1):
        if path[i] != path[i - 1]:
            final_path.append(path[i])
    if final_path[len(final_path) - 1] != 99:
        final_path.append(99)
    return final_path 
        
def algorithm(pop, generations, OBSTACLES):
    """Runs the main pso - ga algorithm as described on the paper"""
    swarm = instantantiate(pop)
    print "Swarm population: ", pop
    print "Max generations: ", generations
    print "-----------------------------------"
    my_map = instantantiate_map(OBSTACLES)
    Particle.THE_MAP = my_map
    best_history = [] #keeps track of best history to terminate program
    
    print "Searching..."
    for i in range(0, generations):
        #---------------Step 3-------------------
        #print "--------Start----------"
        for particle in swarm:
            particle.fit = particle.calculate_fit(particle.x)
            #print particle.fit
        #print"------------------------"
            
        #----------------Step 4------------------   
        new_gen = []
        the_best = find_best_fit(swarm)
        elite = Particle()
        elite.v = the_best.v[:]
        elite.x = the_best.x[:] 
        elite.p_best = the_best.p_best[:]
        new_gen.append(elite)
        for j in range(1, len(swarm)):
            #Decide for crossover
            dont_crossover = random()
            if dont_crossover < CROSSOVER_PROB:
                parent1 = selection(swarm)
                parent2 = selection(swarm)
                a_new_kid = parent1.crossover(parent2)
            else:
               a_new_kid = selection(swarm)
            a_new_kid.mutate()
            new_gen.append(a_new_kid)
        swarm = new_gen
        #print "------After mutation-------"
        for particle in swarm:
            particle.fit = particle.calculate_fit(particle.x)
            #print particle.fit
        #print "---------------------------"
        
            
        #----------------Step 5------------------
        #Find p_best of each particle
        for particle in swarm:
            if particle.fit < particle.calculate_fit(particle.p_best):
                particle.p_best = particle.x[:]
                
        #Find g_best
        fitt = []
        for particle in swarm:
            fitt.append(particle.calculate_fit(particle.p_best))
        minimum = min(fitt)
        if minimum < particle.calculate_fit(Particle.g_best):
            position = fitt.index(minimum)
            Particle.g_best = swarm[position].x[:]
            
        fitt = []
        for particle in swarm:
            fitt.append(particle.fit)
        #print fitt
        minimum = min(fitt)
        position = fitt.index(minimum)
        best_x = swarm[position].x[:]
        best_history.append(minimum)
        print "Generation number: %d, best fit: %f" % (i, minimum)
        #---------Uncoment the following six lines for faster results----------
        if abs(best_history[i] - best_history[i - 1]) < 0.00000000001 and i > 0:
           same += 1
        else:
            same = 0
        if same >= 20:
            break
        #print "-----After step 5-------"
        for particle in swarm:
            particle.fit = particle.calculate_fit(particle.x)
            #print particle.fit
        #print "------------------------"
        #----------------Step 6------------------
        #print "--------Update position-------"
        #print "position: ", position
        for i in range(len(swarm)):
            if i != position:
                swarm[i].update_velocity()
            else:
                pass
        for i in range(len(swarm)):
            if i != position:
                swarm[i].update_position()
            else:
                pass

        for particle in swarm:
            particle.fit = particle.calculate_fit(particle.x)
            #print particle.fit
        #print "------------------------------"
        #raw_input()
 

    #Check if the solution is valid
    line_segments = []
    for i in range(0, len(best_x) - 1):
        line_segments.append(best_x[i:i+2])
    obstacle_factor = []
    obstacles = Particle.obstacles_per_segment(line_segments)
    valid = True
    for nmbr_of_obstacles in obstacles:
        if nmbr_of_obstacles != 0:
            valid = False
            break
    if valid:
        print "Path found, press Enter to view."
        sol = remove_duplicates(best_x)
        raw_input()
        return sol
    else:
        print "A valid path could not be found. Press Enter."
        raw_input()
        return False
        
        
        

    
        
        
    
    
    
    
