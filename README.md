# Traveling-Salesman-Problem-Solver And Visualizer 

### A run on "att48" 

<p align="center"><img src="https://github.com/EyalBrilling/Traveling-Salesman-Problem-Solver/blob/master/media/att48.gif" width="400" height="400" /></p>

## What this is 
This is an implemtation for a genetic algorithm to the travelling salesman problem Plus a visulizer of the algorithm run.

The decisions about the different algorithm parts were done after throught research of different papers. 

**The crossover** i used is order crossover and specificly the Ox4 variant.

The general idea is to take a block of random size from chromosome 1 and block of random size from chromosome 2. than you create 2 children by inserting the block of chromosome 1 to chromosome 2 and vice-versa. [paper](https://www.redalyc.org/pdf/2652/265219618002.pdf)

**The mutation** i used is RSM with a little variant of my own to check for bigger sections - improving the algorithm abilty to get out of local minimums. [paper](https://arxiv.org/ftp/arxiv/papers/1203/1203.3099.pdf)

**The elitism** i used is distance startegy elitism. 
You take the best scored chromosome and the worst scored chromosome and keep them to the next generation. [paper](https://ieeexplore.ieee.org/document/8426051)

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
1) Change the variable "TSP_FILE_PATH" on **line 15** to your file path.
2) Change the variable "NUM_CITIES" on **line 19** to the number of coordinates in your input file.
The code will work even if you won't change this variable,but it will take number of points as the value of the variable.

## If you want to check yourself how different variables effect the algorithm
##### All of the CAPS-LOCKED vairables can be changed. I will explain the important ones:

GENERATIONS_NUM - The number of generations in the algorithm until stop

POP_SIZE - The number of chromosomes in a population

ELITISIM_NUM - The number of pairs to undergo the elitism stage.

MUTATION_PROB - The probabilty for a chromosome to undergo mutation

QX4_MIN_BLOCK_SIZE,QX4_MAX_BLOCK_SIZE - As part of Qx4 crossover stage, a random block size is chosen based on specific disturbtion. 

Not recommanded to play with before reading about this crossover.

SCORE-WEIGHT - The bigger the value is, bigger the change differance of a chromosome to be chosen to a pairing, in comparassion to his better score counterpart. 

for example - under SCORE-WEIGHT of 5, chromosomes with score of 30,000 and 31,000 will have a very close probablity to be chosen for a pairing. Under SCORE-WEIGHT of 30, the chromosome with score of 31,000 will practically never be chosen.


## Visualization
As part of the implemtation, i made a visuliazer(using matplotlib) of the best chromosome in each generation. 
gifs like the one shown will be made for each of your runs automaticlly,no change in code needed.

showing the gif does make the algorithm MUCH slower. 

If you want to test it's speed,remove row 279 - which calls the plotting function "plotTimings".

Also,**in the end of each run - you will get a graph of how the travel score changes thoughout the algorithm** to help you understand when the algorithm gets stuck in local minimum.

An example - 

