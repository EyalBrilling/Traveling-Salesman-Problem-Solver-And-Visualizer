# Traveling-Salesman-Problem-Solver

## A run on "att48" 

<p align="center"><img src="https://github.com/EyalBrilling/Traveling-Salesman-Problem-Solver/blob/master/media/att48.gif" width="400" height="400" /></p>



## How to use
the code takes an input file in the following format:
```
x1 y1 \n
x2 y2 \n
.
.
.
```
Where x<sub>n</sub> is the x coordinate of the n'th point and y<sub>n</sub> is the y coordinate of the n'th point.
Do notice,the order of the points doesn't matter. In the travelling sales problem, the path is cyclic.

for an example,i recommend to look at the "48att.txt" file.

## If you want to try the code on other input files
The algorithm itself is modular and will work on any input file. **there are** two changes you need to do to make it work on other input files:
1) Change the variable "TSP_FILE_PATH" to your file path.
2) Change the variable "NUM_CITIES" to the number of coordinates in your input file.
The code will work even if you won't change this variable,but it will take number of points as the value of the variable.

## If you want to check yourself how different variables effect the algorithm
##### All of the CAPS-LOCKED vairables can be changed. I will explain the important ones:

GENERATIONS_NUM - The number of generations in the algorithm until stop

POP_SIZE - The number of chromosomes in a population

ELITISIM_NUM - The number of pairs to undergo the elitism stage.

MUTATION_PROB - The probabilty for a chromosome to undergo mutation

QX4_MIN_BLOCK_SIZE,QX4_MAX_BLOCK_SIZE - As part of Qx4 crossover stage, a random block size is chosen based on specific disturbtion. 

Not recommanded to play with before reading about this crossover.

##### Read about Ox4 crossover and its variants in the following paper [HERE](https://www.redalyc.org/pdf/2652/265219618002.pdf)

##### Read about distance startegy elitism in the following paper [HERE](https://ieeexplore.ieee.org/document/8426051)
