# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:30:13 2020

@author: Abhishika Sharma, Rashmi Naik, Ayesha Shakeel

The below code runs for 20 generations, 6 individuals and recording the fitness scores at timestep = 1000
"""

import pycxsimulator
from random import uniform
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import random 
import math
from pylab import *
from operator import itemgetter 

# population of Norway    
population = 5328000 # infected + healthy
infected = 19563 # Total number of infected cases in Norway as on 30th Oct, 2020
width = 50 
height = 50
initProb = 0.01 # initial rate of infected population 
''' The actual infection rate in Norway right now is around 0.004%.
To build a realistic CA model, we made an assumption that for 
every automaton, 4 out of 8 neighbors are infected'''
infectionRate = 4/8
# Total number of COVID-19 recovered cases in Norway as on 30th Oct, 2020
recoveryRate = 11863/infected # for an infected person
# Total number of deaths due to COVID-19 in Norway as on 30th Oct, 2020
deathRate = 282/infected # for an infected person
# evolvable parameters: maskRate and hand_sanitizer
# Evolvable parameters
maskRate = 0
hand_sanitizer = 0
# Maximum limit for the evolvable parameters
max_maskRate = 0.6
max_handsanitizer = 0.7
'''Setting the maximum cost (limit) while considering both evolvable parameters together.
Since face masks are relatively more expensive than hand sanitizers, 
we have assigned a weight of 2 for face masks'''
total_prevention_cost = 2 * max_maskRate + 1 * max_handsanitizer 
# The following four lists are used for plotting the graph
fitness_value1 = []
fitness_value2 = []
fitness_value3 = []
fitness_value4 = []
# Stores the fitness score and evolvable parameters for every individual in a generation
fitness_score = [[1], [2], [3], [4], [5], [6]]
i=0
#Empty lists for storing the parameters values for the selected parents
parent1 = []
parent2 = []
new_parent1 = []
new_parent2 = []
generation = 1
individual_count = 1
#Below are used for creating legends in the GUI 
values = [0,1,2,3]
k = ['infected', 'healthy w/o mask', 'healthy w/ mask', 'empty']

def initialize():
    global time, config, nextConfig

    time = 0
    
    config = zeros([height, width])
    for x in range(width):
        for y in range(height):
            # initializing infected people
            if random() < initProb:
                state = 0
            # initializing healthy people w/o (without) masks 
            elif random() < (population-infected)/population:
                state = 1
            # initializing empty cells / no individual present
            else:
                state = 3
            config[y, x] = state

    nextConfig = zeros([height, width])
    
    

def observe():
    # grid creation for CA model which represents state transition of every automaton
    subplot(2, 1, 1)
    cla()
    im = plt.imshow(config, vmin = 0, vmax = 4, cmap = cm.jet) 
    axis('image')
    title('day = ' + str(time))
    colors = [ im.cmap(im.norm(value)) for value in values]
    # create a patch (proxy artist) for every color 
    patches = [ mpatches.Patch(color=colors[i], label="{l}".format(l=k[i]) ) for i in range(len(values)) ]
    # put those patches as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

    # Initializing variables to count total number of cells set to every specific state
    fitnessInfected = 0
    fitnessHealthyWithoutMask = 0
    fitnessHealthyWithMask = 0
    fitnessEmptyCell = 0
    for x in range(width):
        for y in range(height):
            # fitness function calculates total number of infected people in the grid
            if config[y,x]==0:
                fitnessInfected += 1
            elif config[y,x]==1:
                fitnessHealthyWithoutMask += 1
            elif config[y,x]==2:
                fitnessHealthyWithMask += 1
            elif config[y,x]==3:
                fitnessEmptyCell += 1
    fitness_value1.append(fitnessInfected) 
    fitness_value2.append(fitnessHealthyWithoutMask) 
    fitness_value3.append(fitnessHealthyWithMask)
    fitness_value4.append(fitnessEmptyCell)
    
    # Time step at which the fitness score and the evolvable parameters are recorded
    if time == 1000:
        if i < len(fitness_score):
            fitness_score[i].append(fitnessInfected)
            fitness_score[i].append(maskRate)
            fitness_score[i].append(hand_sanitizer)
            
            
 # Graph to reresent total count of every state
    subplot(2, 1, 2)
    cla()
    plt.plot(fitness_value1, label='infected')
    plt.plot(fitness_value2, label='healthy without mask')
    plt.plot(fitness_value3, label='healthy with mask')
    plt.plot(fitness_value4, label='empty cell')
    #legend(fitness_value1, 'infected')
    plt.legend(framealpha=1, frameon=True, loc = 'upper center')
    plt.title('Count of different states represented on the grid')
    plt.xlabel('Number of days')
    plt.ylabel('Total count of each state')


def update():
    global time, config, nextConfig 
    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            
            # Initializing local variables used in the algorithm
            numberOfAlive = 0
            removeMask = 0
            addHealthyCell = 0
            addHealthyCell1 = 0
            countHealthyCell = 0
            allEmpty = 0
            
            '''CONDITION 1: infected person'''
            if state == 0:
                # checking the surrounding eight neighbors- Moore neighborhood 
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        # If infection rate is lower than specified value, the state remains unchanged
                        if random() < infectionRate:
                            state = 0
                        # If the infection rate is higher than intended, we have to change state of infected person
                        elif random() > infectionRate: 
                            
                            '''if neighbor is also an infected person'''
                            if config[(y+dy)%height, (x+dx)%width] == 0:
                                    # We check if either recoveryRate or deathRate conditions are satisfied
                                    if random() < recoveryRate:
                                        # Recovered person can either have a mask or not
                                        if random() < maskRate:
                                            state = 2
                                        else: state = 1 
                                    # If deathRate is satisfied, infected person converts to empty cell on the grid    
                                    elif random() < deathRate:
                                        state = 3
                                        
                                        '''if neighbor is a healthy person w/ mask'''        
                            elif config[(y+dy)%height, (x+dx)%width] == 2:
                                # ASSUMPTION is that an infected person will recover quickly when surrounded by healthy people (e.g., in a hospital)
                                if random() < recoveryRate:
                                    if random() < maskRate:
                                        state = 2
                                        
                                        '''if neighbor is an empty cell'''  
                            elif config[(y+dy)%height, (x+dx)%width] == 3:
                                # Count the total number of empty cells surrounding the infected person
                                for dx in range(-1, 2):
                                        for dy in range(-1, 2):
                                            if config[(y+dy)%height, (x+dx)%width] == 3:
                                                allEmpty += 1
                                # If an infected person has no one around him/her, it may either help him recover completely or might put him into depression
                                if allEmpty == 8:
                                    if random() < recoveryRate:
                                            # Since there is no one around the infected person, he need not wear a mask
                                            state = 1
                                    elif random() < deathRate:
                                        state = 3           
            
            
                '''CONDITION 2: Healthy person w/o mask'''
            elif state == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        
                        '''if neighbor is a healthy person with mask'''
                        if config[(y+dy)%height, (x+dx)%width] == 2:
                            if random() < maskRate:
                                # Count the total number of neighbors wearing a mask
                                for dx in range(-1, 2):
                                    for dy in range(-1, 2):
                                        if config[(y+dy)%height, (x+dx)%width] == 2:
                                            numberOfAlive += 1
                                # ASSUMPTION: A person without mask will wear a mask only if four or more neighbors are wearing a mask
                                if numberOfAlive >= 4:
                                    state = 2
                                    
                                    ''' if neighbor is an infected person '''
                        elif config[(y+dy)%height, (x+dx)%width] == 0:
                            # A healthy person without wearing mask can further increase chances of getting infected if he has no access to hand sanitizer
                            if random() < infectionRate: 
                                if random() > hand_sanitizer:
                                    state = 0
    
                                    
                '''CONDITION 3: Healthy person wearing mask'''
            elif state == 2:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        
                        ''' if neighbor is an infected person'''
                        if config[(y+dy)%height, (x+dx)%width] == 0:
                            # Healthy person wearing mask can also contract the virus if he comes in contact with infected surfaces and doesn't sanitize his hands
                            if random() > hand_sanitizer:
                                if random() < infectionRate: 
                                        state = 0
                                        
                                        ''' if neighbor is a healthy person w/o mask'''               
                        elif config[(y+dy)%height, (x+dx)%width] == 1:
                            if random() > maskRate:
                                # Count the total number of neighbors not wearing a mask
                                for dx in range(-1, 2):
                                    for dy in range(-1, 2):
                                        if config[(y+dy)%height, (x+dx)%width] == 1:
                                            removeMask += 1
                                # ASSUMPTION: Pandemic fatigue and neighbors' behavior can influence a person wearing mask to remove it
                                if removeMask >= 4:
                                    state = 1
              
                
                '''CONDITION 4: Empty cell'''                        
            elif state == 3:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        # Count the total number of healthy neighbors (with or without mask)
                        if config[(y+dy)%height, (x+dx)%width] == 1 or config[(y+dy)%height, (x+dx)%width] == 2:
                            addHealthyCell += 1
                        # Count the total number of empty cells in neighborhood
                        elif config[(y+dy)%height, (x+dx)%width] == 3:
                            addHealthyCell1 += 1
                countHealthyCell = addHealthyCell + addHealthyCell1
                # To avoid extinction of population, we introduce a healthy person in place of empty cell
                # Conditions for reproduction: No infected person in neighborhood; Minimum two healthy people in neighborhood (with or without mask)
                if addHealthyCell >= 2 and countHealthyCell == 9:
                    if random() < maskRate:
                        state = 2
                    else: 
                        state = 1                        
 
    
            nextConfig[y, x] = state
        
    
    config, nextConfig = nextConfig, config
    

'''The below function performs the selection of the two fittest parent based on the fitness_score which is the count of the infected
population at timestep t and selecting the two best parents and performing crossover to produce offsprings.'''
def fitness_check():
    global maskRate
    global hand_sanitizer, parent1, parent2, new_parent1, new_parent2,fitness_score
    parent1 = []
    parent2 = []
    new_parent1 = []
    new_parent2 = []
    print('Initial fitness scores list',fitness_score)
    #sorting the list of fitness_score based on the second element in the sublist
    fitness_score.sort(key = lambda x: x[1]) 
    print('Sorted fitness scores', fitness_score)
    #selecting the 2 parents with the lowest number of infections
    parent1_fitness = fitness_score[0]
    parent2_fitness = fitness_score[1]
    print('Parent1',parent1_fitness)
    print('Parent2',parent2_fitness)
    
    #appending the values of the two parameters for parent1 and parent2
    parent1.append(parent1_fitness[2])
    parent1.append(parent1_fitness[3])
    parent2.append(parent2_fitness[2])
    parent2.append(parent2_fitness[3])
    
    ##printing the parameters values for 2 parents
    parent1_cost = parent1[0]+parent1[1]
    parent2_cost = parent2[0]+parent2[1]
    print('Parameter for Parent 1',parent1)
    print('Parameter for Parent 2',parent2)
    
    '''performing crossover if the cost of parent1 and parent2 is less than or equal to the total_prevention_cost 
    and parameters are not exceeding the maximum limit'''
    if parent1[0] <= max_maskRate and parent1[1] <= max_handsanitizer and parent1_cost <= total_prevention_cost :
        if parent2[0] <= max_maskRate and parent2[1] <= max_handsanitizer and parent2_cost <= total_prevention_cost:
            new_parent1.append(parent1[0])
            new_parent1.append(parent2[1])
            new_parent2.append(parent2[0])
            new_parent2.append(parent1[1])
            print('Offspring1', new_parent1)
            print('Offspring2',new_parent2)
    new_cost_parent1 = new_parent1[0]+new_parent1[1]
    new_cost_parent2 = new_parent2[0]+new_parent2[1]
    if new_cost_parent1 <= total_prevention_cost and new_cost_parent1 <= new_cost_parent2:
        maskRate = new_parent1[0]
        hand_sanitizer = new_parent1[1]
        print('Offspring1 maskrate' ,maskRate)
        print('Offspring1 handsanitizer ' ,hand_sanitizer)
    elif new_cost_parent2 <= total_prevention_cost and new_cost_parent2 <= new_cost_parent1:
        maskRate = new_parent2[0]
        hand_sanitizer = new_parent2[1]        
        print('Offspring2 ',maskRate)
        print('Offspring2 ',hand_sanitizer)

    
def main():
    global new_hand_sanitizer,new_maskRate,i,fitness_score,maskRate,hand_sanitizer,r1,r2
    #running the code for the below range of generations
    for generation in range (1,21):
        individual_count = 1
        print('----------------------------------------------------------------------')
        print('Running Generation', generation)
        print('MaskRate for',generation,'generation is',maskRate)
        print('Handsanitizer for', generation, 'generation is',hand_sanitizer)    
        
        '''loop for running for the below individuals in 1 generation and calling the update(), 
        initialize() and observe() function without the pycx simulator'''
        while individual_count<=6:
            time = 0
            initialize()
            observe()
            for time in range (1,1001):
                update()
                observe()
            i+=1
            #mutating the values of two eveolable parameters with each run of individual
            r1 = round(round(uniform(-0.6,0.6),1),1)    
            r2 = round(round(uniform(-0.7,0.7),1),1)
            new_maskRate = round((maskRate + r1),1)
            while(new_maskRate < 0):
                r1 = round(round(uniform(-0.6,0.6),1),1)
                new_maskRate = round((maskRate + r1),1)
            new_hand_sanitizer =round(( hand_sanitizer+ r2),1)
            while(new_hand_sanitizer < 0):
                r2 = round(round(uniform(-0.7,0.7),1),1)
                new_hand_sanitizer =round(( hand_sanitizer+ r2),1)
            '''Checking the condition that the new mutated parameters should be less than the max_maskRate and max_handsanitizer
            If the condition is True for both, then set the maskRate and hand_sanitizer to the new values for the next generation'''
            if new_maskRate <= max_maskRate and new_hand_sanitizer <= max_handsanitizer:
                maskRate = new_maskRate
                hand_sanitizer = new_hand_sanitizer
            individual_count+=1
        ''''Calling the fitness_check() for doing the selection of the fittest parent and performing crossover between the two 
        selected parents'''
        fitness_check()
        fitness_score.clear()
        fitness_score = [[1], [2], [3], [4], [5], [6]]
        i = 0
    
    
if __name__ == "__main__":
    main()
    


            





