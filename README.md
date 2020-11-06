# Covid-19 Simulation

This github link contains the Python code developed for academic project for Evolutionary Artificial Intelligence and Robotics course. <br>

The <B>Update Basic Model.py</B> contains the basic implementation of the CA model with the PyCx GUI and without the Evolutionary AI.
<BR>
The <B>Evo_AI_Merge_without_simulator.py</B> contains the full code with implementation of Evolutionary AI but without the PyCx GUI.
<BR>
The <B>Experiment Output.docs</B> contains all the output screenshots of all the simulations run with different generations, individuals and timesteps.
<BR>

The code aims to simulate Covid-19 pandemic using the CA model to reduce the infection spread of coronavirus based on evolvable parameters- maskrate and hand sanitizer.<br>

Evolutionary Algorithm is also being implemented in the code. Recording the fitness scores with every individual, selecting the fittest parents, performing crossover and mutation is being done in the program.<br>

Different experiments can be run on the above code with varying generations and individuals.<br>

1. If you want to run the code for 100 individuals then change the list that says 'fitness_scores' as fitness_score = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36], [37], [38], [39],[40], [41],[42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [58], [59], [60], [61], [62], [63], 
 [64], [65], [66], [67], [68], [69], [70], [71], [72], [73], [74], [75],[76],[77], [78], [79], [80], [81], [82], [83], [84], [85], [86], [87], [88], [89], [90], [91], [92], [93], [94], [95], [96], [97], [98], [99], [100]]
 <br>
 
 2. If you want to run the code for 10 individuals then change the list that says 'fitness_scores' as fitness_score = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
 <br>
 and so on...
 <br>
 
 In order to change the generation count, just increase/decrease the range of generation in the for loop inside the main() method.
 
 <br>
 The simulation can be run with different timesteps, to do that change the time value in the observe() method and also in the main() method inside the while loop.
<br> 
<br>

<B>Contributors :</B> <br>

Abhishika Sharma (Master Student, Cloud based services and operations, ACIT, OsloMet) <br>
Rashmi Naik (Master Student, Artificial Intelligence, ACIT, OsloMet) <br>
Ayesha Shakeel (Master Student, Cloud based services and operations, ACIT, OsloMet) <br>
