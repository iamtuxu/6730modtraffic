# 6730modtraffic
Final project implementation for project 1 - Team 51: Tu Xu, Hongyu Lu, Zixiu Fu

## Markov Chain
This folder includes the codes for the car-following model based on Discrete Time Markov Chain, and the output csv files.

### Subfolder of output:
A subfolder contains all the output. The csv files are named after the launching time of the simulation and the car ID. An overall output file is also generated for each simulation, ending with ‘_Total’ in the file name.
    
### basicFunction.py:
A code file that includes the random number generation function.

### car.py:
A code file that includes the classes of trajectory and car. The calculation of the update (displacement due to desired acceleration and constrain of the leader) is all included in this file, as well as a I/O function of the class of car.

### globalVariable.py:
A variable declaration file lists the setting objects.

### main.py:
A code file to call the simulation.

### markovSetting.py:
A code file of the class of simulation settings, including the calculation of the standard deviation of the stochastic disturbance.

### sim.py:
A code file that includes the function to launch the simulation, including all the I/O.


## Cellular Automata
This folder includes necessary codes for the cellular simulation for simple one-layer intersections. For specific usage, please refer to the tutorial.

### acc.py
This is the main code include the definition of three main objects.

### var.py
pre-defined direction variable

### test.py
A simple usage of the program to simulate a 1D road。

## Jupyter
This folder includes tutorial and sample analysis for both model.