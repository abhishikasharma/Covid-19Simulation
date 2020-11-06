# -*- coding: utf-8 -*-
"""
COVID-19 Modeling - Updated basic model

@author: Abhishika, Rashmi, Ayesha

Note: Only the changes from the initial model are highlighted in this program
"""


import pycxsimulator
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from random import randint
from pylab import *
from operator import itemgetter 

    

# population of Norway    
population = 5328000 # infected + healthy
infected = 20769 # Total number of infected cases in Norway as on 30th Oct, 2020
width = 50 
height = 50
initProb = 0.01 # initial rate of infected population 
''' The actual infection rate in Norway right now is around 0.004%.
To build a realistic CA model, we made an assumption that for 
every automaton, 4 out of 8 neighbors are infected'''
infectionRate = 6/8
# Total number of COVID-19 recovered cases in Norway as on 30th Oct, 2020
recoveryRate = 11863/infected # for an infected person
# Total number of deaths due to COVID-19 in Norway as on 30th Oct, 2020
deathRate = 282/infected # for an infected person
# evolvable parameters: maskRate and hand_sanitizer
# Evolvable parameters
maskRate = 0.5
hand_sanitizer = 0.6
# The following four lists are used for plotting the graph
fitness_value1 = []
fitness_value2 = []
fitness_value3 = []
fitness_value4 = []
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
            # initializing healthy people w/ or w/o masks 
            elif random() < (population-infected)/population:
                state = 1
            # initializing empty cells
            else:
                state = 3
            config[y, x] = state

    nextConfig = zeros([height, width])
    

def observe():

    subplot(2, 1, 1)
    cla()
    im = plt.imshow(config, vmin = 0, vmax = 4, cmap = cm.jet) 
    axis('image')
    title('day = ' + str(time))
    colors = [ im.cmap(im.norm(value)) for value in values]
# create a patch (proxy artist) for every color 
    patches = [ mpatches.Patch(color=colors[i], label="{l}".format(l=k[i]) ) for i in range(len(values)) ]
# put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

    sum2 = 0
    sum3 = 0
    sum4 = 0
    sum5 = 0
    for x in range(width):
        for y in range(height):
            # fitness function calculates number of infected people
            if config[y,x]==0:
                sum2 += 1
            elif config[y,x]==1:
                sum3 += 1
            elif config[y,x]==2:
                sum4 += 1
            elif config[y,x]==3:
                sum5 += 1
    fitness_value1.append(sum2) 
    fitness_value2.append(sum3) 
    fitness_value3.append(sum4)
    fitness_value4.append(sum5)

            
 
    subplot(2, 1, 2)
    cla()
    plt.plot(fitness_value1, label='infected')
    plt.plot(fitness_value2, label='healthy w/o mask')
    plt.plot(fitness_value3, label='healthy w/ mask')
    plt.plot(fitness_value4, label='empty cell')
    #legend(fitness_value1, 'infected')
    plt.legend(framealpha=1, frameon=True, loc = 'upper center')
    plt.title('Total count of different cell states present on the grid')
    plt.xlabel('day')
    plt.ylabel('Total count')

def update():
    global time, config, nextConfig 
    time += 1
    time_count = time
    
    for x in range(width):
        for y in range(height):
            state = config[y, x]
            infectedCount = 0

            numberOfAlive = 0
            removeMask = 0
            infectionWithMask = 0
            addHealthyCell = 0
            addHealthyCell1 = 0
            countHealthyCell = 0
            allEmpty = 0            
                     '''CONDITION 1: infected person'''
            if state == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if random() < infectionRate:
                            state = 0
                        # if neighbor is also an infected person
                        elif random() > infectionRate: 
                            if config[(y+dy)%height, (x+dx)%width] == 0:
                                    if random() < recoveryRate:
                                        if random() < maskRate:
                                            state = 2
                                        else: state = 1 
                                    elif random() < deathRate:
                                        state = 3
                                    
                            elif config[(y+dy)%height, (x+dx)%width] == 2:
                                if random() < recoveryRate:
                                    if random() < maskRate:
                                        state = 2
                            elif config[(y+dy)%height, (x+dx)%width] == 3:
                                for dx in range(-1, 2):
                                        for dy in range(-1, 2):
                                            if config[(y+dy)%height, (x+dx)%width] == 3:
                                                allEmpty += 1
                                if allEmpty == 8:
                                    if random() < recoveryRate:
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
                            ''' New condition added: Check if extended neighborhood has any infected cells'''
                        infectedCount = 0
                        for i in range(-4,5):
                            for j in range(-4,5):
                                if config[(y+j)%height, (x+i)%width]==0:
                                    infectedCount += 1
                                    if infectedCount >= 1:
                                        break
                        if infectedCount == 0:
                            state = 1
                                    
                            ''' if neighbor is an infected person '''
                        elif config[(y+dy)%height, (x+dx)%width] == 0:
                            # A healthy person without wearing mask can further increase chances of getting infected if he has no access to hand sanitizer
                            if random() < infectionRate:
                                if random() > maskRate:
                                    if random() > hand_sanitizer:   
                                            state = 0
                                elif random() > infectionRate:
                                    if random() < hand_sanitizer:
                                        if random() < maskRate:
                                            state = 2
    
                                    
             '''CONDITION 3: Healthy person wearing mask'''
            elif state == 2:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        ''' New condition added: Check if extended neighborhood has any infected cells'''
                        infectedCount = 0
                        for i in range(-4,5):
                            for j in range(-4,5):
                                if config[(y+j)%height, (x+i)%width]==0:
                                    infectedCount += 1
                                    if infectedCount >= 1:
                                        break
                        if infectedCount == 0:
                            state = 1
                        
                        if config[(y+dy)%height, (x+dx)%width] == 0:
                            if random() > hand_sanitizer:
                                if random() < infectionRate: 
                                    ''' New condition added: Check if immediate neighbors have state = 0'''
                                        for dx in range(-1, 2):
                                            for dy in range(-1, 2):
                                                if config[(y+dy)%height, (x+dx)%width] == 0:
                                                    infectionWithMask += 1
                                        if infectionWithMask >= 4:
                                            state = 0
                        elif config[(y+dy)%height, (x+dx)%width] == 1:
                            if random() > maskRate:
                                if random() < hand_sanitizer:
                                    for dx in range(-1, 2):
                                        for dy in range(-1, 2):
                                            if config[(y+dy)%height, (x+dx)%width] == 1:
                                                removeMask += 1
                                    if removeMask >= 4:
                                        state = 1
                   
                '''CONDITION 4: Empty cell'''
            elif state == 3:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == 1 or config[(y+dy)%height, (x+dx)%width] == 2:
                            addHealthyCell += 1
                        elif config[(y+dy)%height, (x+dx)%width] == 3:
                            addHealthyCell1 += 1
                countHealthyCell = addHealthyCell + addHealthyCell1
                if addHealthyCell >= 2 and countHealthyCell == 9:
                    if random() < maskRate:
                        ''' New condition added: Check if extended neighborhood has any infected cells'''
                        infectedCount = 0
                        for i in range(-4,5):
                            for j in range(-4,5):
                                if config[(y+j)%height, (x+i)%width]==0:
                                    infectedCount += 1
                                    if infectedCount >= 1:
                                        break
                        if infectedCount != 0:
                            state = 2
                        else: 
                            state = 1                        
 
    
            nextConfig[y, x] = state
        
    
    config, nextConfig = nextConfig, config
    
pycxsimulator.GUI().start(func=[initialize, observe, update])
    






