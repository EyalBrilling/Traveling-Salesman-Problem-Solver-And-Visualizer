from cProfile import label
from cmath import sqrt
from copy import copy
import random
import math
from itertools import cycle
from dist_functions import randomNumbersNormalInverseDisturbition
from tsp_plot import plotTSP
import matplotlib.pyplot as plt



# file name to read Problem coordinated from
TSP_FILE_PATH="tsp.txt"

# number of generations to run
GENERATIONS_NUM = 5000
NUM_CITIES = 48
POP_SIZE = 100
# number of pairs in elitism
ELITISIM_NUM = 10
# probablity to change RSM mutation from starting at coutner=1 to higher counter
MUTATION_LONG_ROAD_PROB=0.05
# probabilty for mutation
MUTATION_PROB = 0.3
# probability to add 1 to counter,making swapped road longer
MUTATION_VAR_PROB = 0.7

# inverse normal probabilty vars
MU,SIGMA=0,1

# defining different disturbations
LINEAR_DIST,INVERSE_NORMAL_DIST=0,1
# defining a random or determinated block size for Qx4 crossover
DET_CROSSOVER_BLOCK_SIZE,RAN_CROSSOVER_BLOCK_SIZE=0,1
# defing block sizes range for RAN
QX4_MIN_BLOCK_SIZE,QX4_MAX_BLOCK_SIZE = 1,24
# defining block size for DET
QX4_DET_BLOCK_SIZE_FATHER = 3
QX4_DET_BLOCK_SIZE_MOTHER = 4

# define the power of chromosome scores. bigger the score_weight,bigger the weight difference between close scores.
SCORE_WEIGHT = 20

def chromosomeScore(chromosome,citiesCooridinates):
    travelScore=0
    for cityIndex,city in enumerate(chromosome):
        currentCityCoordinates = citiesCooridinates[city]
        # running backwords for enabling [0] and [-1] scoring without changing code more
        previousCityCoordinates = citiesCooridinates[chromosome[cityIndex-1]]
        travelScore+= math.sqrt(pow(abs(int(currentCityCoordinates[0])-int(previousCityCoordinates[0])),2)+ pow(abs(int(currentCityCoordinates[1])-int(previousCityCoordinates[1])),2))
    return travelScore

def distanceStartegyElitism(chromosomeList,chromosomeScores):
    chromosomesToKeep=[]
    elitismChoromosomeList = chromosomeList.copy()
    elitismChoromosomeScores= chromosomeScores.copy()
    for elitismNum in range(ELITISIM_NUM):
        bestChromosomeScore=min(elitismChoromosomeScores)
        worstChromosomeScore=max(elitismChoromosomeScores)
        bestChromosome=elitismChoromosomeList[elitismChoromosomeScores.index(bestChromosomeScore)]
        worstChromosome=elitismChoromosomeList[elitismChoromosomeScores.index(worstChromosomeScore)]

        elitismChoromosomeScores.remove(bestChromosomeScore)
        elitismChoromosomeScores.remove(worstChromosomeScore)
        elitismChoromosomeList.remove(bestChromosome)
        elitismChoromosomeList.remove(worstChromosome)
            # make the city 0 the first in the list
        bestChromosome0Index = bestChromosome.index(0)
        bestChromosome = bestChromosome[bestChromosome0Index:] + bestChromosome[:bestChromosome0Index]
        worstChromosome0Index = worstChromosome.index(0)
        worstChromosome = worstChromosome[worstChromosome0Index:] + worstChromosome[:worstChromosome0Index]
        chromosomesToKeep+=[bestChromosome,worstChromosome]

    return chromosomesToKeep

def mutationRSM(chromosome):
    test= chromosome.copy()
    if random.random() < MUTATION_PROB:
        startIndex = random.randrange(1,NUM_CITIES)
        endIndexCounter = 1
        if random.random() < MUTATION_LONG_ROAD_PROB:
            endIndexCounter=12
            if random.random() < 0.5:
                endIndexCounter=24
                if random.random() < 0.5:
                    endIndexCounter=36
        # run on indexes until the end index is chosen. getting to higher index is harder.
        while random.random() > (1- MUTATION_VAR_PROB):
            endIndexCounter+=1
        endIndex = startIndex+endIndexCounter
        if endIndex >= NUM_CITIES:
            chromosome[startIndex:] = chromosome[:startIndex-1:-1]
        else:
             chromosome[startIndex:endIndex+1] = chromosome[endIndex:startIndex-1:-1]
    return chromosome

    # child from father block recipe
    # 1) cut the block from father
    # 2) take the numbers from the end of the cut of MOTHER until the start of the cut
    # 3) remove from the mother numbers the father block numbers
    # 4) create child-
    # a) put in the start of the child the end of mother numbers that cant fit after the father cut
    # b) put the father block in the same place it was
    # c)from the end of the cut of FATHER,put the mother start numbers

def pairingStage(chromosomeList,populationScore,crossoverType,dist_type):
    pairs=[]
    children=[]
    scoreList=[]
    # each pair gives 2 children. each elitisim_num saves 2 pop from previous popultion so need 1 less pair for each elitism.
    sort_score = [(x,i) for i,x in enumerate(populationScore)]
    sort_score = sorted(sort_score,reverse=True)
    result = [0]*len(sort_score)
    for i,(_,idx) in enumerate(sort_score):
        result[idx] = (POP_SIZE - i)
    populationScore= [ (1/(score/1000))**SCORE_WEIGHT for score in populationScore]
    for pairNum in range(int(POP_SIZE/2 - ELITISIM_NUM)):
        pairs.append(random.choices(chromosomeList,weights=populationScore,k=2))
    for pair in pairs:
        children += orderCrossoverQx4(*pair,crossoverType,dist_type)
    return children

def orderCrossoverQx4(father,mother,crossoverType,dist_type):
    testfather= father.copy()
    testmother=mother.copy()
    if crossoverType== RAN_CROSSOVER_BLOCK_SIZE:
        if dist_type == LINEAR_DIST:
            fatherBlockSize = random.randint(QX4_MIN_BLOCK_SIZE,QX4_MAX_BLOCK_SIZE)
            motherBlockSize = random.randint(QX4_MIN_BLOCK_SIZE,QX4_MAX_BLOCK_SIZE)
        if dist_type == INVERSE_NORMAL_DIST:
            fatherBlockSize,motherBlockSize = randomNumbersNormalInverseDisturbition(QX4_MIN_BLOCK_SIZE,QX4_MAX_BLOCK_SIZE,MU,SIGMA)
        
    else:
        fatherBlockSize = QX4_DET_BLOCK_SIZE_FATHER
        motherBlockSize = QX4_DET_BLOCK_SIZE_MOTHER

    fatherCutPointStartIndex = random.randint(1,NUM_CITIES-fatherBlockSize-1)
    motherCutPointStartIndex = random.randint(1,NUM_CITIES-motherBlockSize-1)

    fatherCutPointEndIndex = fatherCutPointStartIndex+fatherBlockSize
    motherCutPointEndIndex = motherCutPointStartIndex+motherBlockSize
    # 1)
    fatherBlock = father[fatherCutPointStartIndex:fatherCutPointEndIndex]
    motherBlock = mother[motherCutPointStartIndex:motherCutPointEndIndex]
    # 2)
    fatherSequenceAfterCutPoint= father[fatherCutPointEndIndex:] + father[:fatherCutPointEndIndex]
    motherSequenceAfterCutPoint= mother[motherCutPointEndIndex:] + mother[:motherCutPointEndIndex]
    # 3)
    fatherSequenceRemovedBlock = [number for number in fatherSequenceAfterCutPoint if number not in motherBlock]
    motherSequenceRemovedBlock = [number for number in motherSequenceAfterCutPoint if number not in fatherBlock]
    # 4) num of numbers that fit from the end cut: (len) - (endcutIndex+1)
    childFromFatherBlockAfterCutFit = (NUM_CITIES) - fatherCutPointEndIndex 
    childFromMotherBlockAfterCutFit = (NUM_CITIES) - motherCutPointEndIndex 
    # put the child together: 
    childFromFatherBlock = motherSequenceRemovedBlock[:childFromFatherBlockAfterCutFit] + fatherBlock + motherSequenceRemovedBlock[childFromFatherBlockAfterCutFit:]
    childFromMotherBlock = fatherSequenceRemovedBlock[:childFromMotherBlockAfterCutFit] + motherBlock + fatherSequenceRemovedBlock[childFromMotherBlockAfterCutFit:]

    # make the city 0 the first in the list
    firstChild0Index = childFromFatherBlock.index(0)
    childFromFatherBlock = childFromFatherBlock[firstChild0Index:] + childFromFatherBlock[:firstChild0Index]
    secondChild0Index = childFromMotherBlock.index(0)
    childFromMotherBlock = childFromMotherBlock[secondChild0Index:] + childFromMotherBlock[:secondChild0Index]
    return [childFromFatherBlock,childFromMotherBlock]

def initiateChromosome():
    chromosome = [0] + [city for city in range(1,NUM_CITIES)]
    random.shuffle(chromosome)
    return chromosome

def initiatePopulation():
    population=[]
    for popNum in range(POP_SIZE):
        population.append(initiateChromosome())
    return population
def printInfo(population,popultionScore,loopNum,citiesCooridinates):
    bestChromosomeScore=min(popultionScore)
    worstChromosomeScore=max(popultionScore)
    bestChromosome=population[popultionScore.index(bestChromosomeScore)]
    worstChromosome=population[popultionScore.index(worstChromosomeScore)]
    print("GEN: " + str(loopNum) + " BEST SCORE: " + str(bestChromosomeScore) + " BEST CHROMOSOME: " + str(bestChromosome))
    print("WORST SCORE: " + str(worstChromosomeScore) + " WORST CHROMOSOME: " + str(worstChromosome))

def TSPcitiesCoordinates(filePath):
    citiesCoordinates=[]
    with open(filePath,"r") as fl:
        for line in fl:
            splittedLine= line.strip().split()
            citiesCoordinates.append(splittedLine)
    return citiesCoordinates

def populationScorer(population,citiesCoordinates):
    popScore=[]
    for chromosome in population:
        popScore.append(chromosomeScore(chromosome,citiesCoordinates))
    return popScore

def mutateTheChildren(children):
    mutatedChildren=[]
    for child in children:
        mutatedChildren.append(mutationRSM(child))
        if len(child)!=NUM_CITIES:
            print("ERROR")
    return mutatedChildren

def visuliazeRunWithGreedyAlgo(BestScoreList,avergeScoreList,greedyScore):
    plt.plot([x for x in range(1,GENERATIONS_NUM+1)],BestScoreList,label="Best Route Score")
    plt.plot([x for x in range(1,GENERATIONS_NUM+1)],avergeScoreList,label="Average Route Score")
    plt.plot([x for x in range(1,GENERATIONS_NUM+1)],[greedyScore for x in range(len(BestScoreList))],label="Greedy Score")
    plt.xlabel("Generation")
    plt.ylabel("Score")
    plt.legend()
    plt.ylim(33607,60000)
    ax=plt.gca()
    for scoreIndex,score in enumerate(BestScoreList):
        if score == min(BestScoreList):
            ax.annotate(str(int(score)),xy=(scoreIndex+500,score+100),color= 'red',size='large')
            break
        elif scoreIndex %2000==0:
            ax.annotate(str(int(score)),xy=(scoreIndex+1,score))
    plt.show()

def visuliazeRun(BestScoreList,avergeScoreList):
    plt.plot([x for x in range(1,GENERATIONS_NUM+1)],BestScoreList,label="Best Route Score")
    plt.plot([x for x in range(1,GENERATIONS_NUM+1)],avergeScoreList,label="Average Route Score")
    plt.xlabel("Generation")
    plt.ylabel("Score")
    plt.legend()
    plt.ylim(33607,60000)
    ax=plt.gca()
    for scoreIndex,score in enumerate(BestScoreList):
        if score == min(BestScoreList):
            ax.annotate(str(int(score)),xy=(scoreIndex+500,score+100),color= 'red',size='large')
            break
        if scoreIndex %2000==0:
            ax.annotate(str(int(score)),xy=(scoreIndex+1,score))
    plt.show()
def greedyAlgo(citiesCooridinates):
    travelScore=0
    currentTravel=[0]
    for num in range(NUM_CITIES-1):
        bestDistance=10000000
        bestCity=None
        for cityIndex,cityInfo in enumerate(citiesCooridinates):
            distance = math.sqrt(pow(abs(int(citiesCooridinates[currentTravel[num]][0])-int(cityInfo[0])),2)+ pow(abs(int(citiesCooridinates[currentTravel[num]][1])-int(cityInfo[1])),2))
            if distance<bestDistance and cityIndex not in currentTravel:
                bestDistance=distance
                bestCity=cityIndex
        currentTravel.append(bestCity)
        travelScore+=bestDistance
    return currentTravel,travelScore

def plotTimings(generationNum,populationScore,population,citiesCooridinates):
    if generationNum <500:
        if generationNum%50:
            bestChromosomeScore=min(populationScore)
            bestChromosome=population[populationScore.index(bestChromosomeScore)]
            plotTSP([bestChromosome],citiesCooridinates,1)
    elif generationNum % 100==0:
        bestChromosomeScore=min(populationScore)
        bestChromosome=population[populationScore.index(bestChromosomeScore)]
        plotTSP([bestChromosome],citiesCooridinates,1)
def main():
    bestScoreList=[]
    averageScoreList=[]
    citiesCooridinates=TSPcitiesCoordinates(TSP_FILE_PATH)
    citiesCooridinates = [[int(x) for x in coord] for coord in citiesCooridinates]
    population=initiatePopulation()
    for generationNum in range(GENERATIONS_NUM):
        populationScore = populationScorer(population,citiesCooridinates)
        elitisimWinners = distanceStartegyElitism(population,populationScore)
        children = pairingStage(population,populationScore,RAN_CROSSOVER_BLOCK_SIZE,INVERSE_NORMAL_DIST)
        mutantChildren= mutateTheChildren(children)
        population=mutantChildren + elitisimWinners
        bestScoreList.append(min(populationScore))
        averageScoreList.append(sum(populationScore)/POP_SIZE)
        plotTimings(generationNum,populationScore,population,citiesCooridinates)
        if generationNum %100 == 0 :
          bestChromosomeScore=min(populationScore)
          bestChromosome=population[populationScore.index(bestChromosomeScore)]
          plotTSP([bestChromosome],citiesCooridinates,1)
   # bestChromosomeScore=min(populationScore)
   # bestChromosome=population[populationScore.index(bestChromosomeScore)]
    printInfo(population,populationScore,generationNum,citiesCooridinates)
   # plotTSP([bestChromosome],citiesCooridinates,1)
    greedyTravel,greedyScore=greedyAlgo(citiesCooridinates)
    visuliazeRunWithGreedyAlgo(bestScoreList,averageScoreList,greedyScore)

if __name__=="__main__":
    main()