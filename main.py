from knapsack.config import Config
from knapsack.genetic_algorithm import GeneticAlgorithmFacade
from knapsack.generation import GenerationStrategy
from knapsack.mutation import MutationStrategy
from knapsack.problem import ProblemType
from knapsack.reproduction import ReproductionStrategy
from knapsack.selection import SelectionStrategy
from knapsack.stop_criteria import StopCriteriaType

import matplotlib.pyplot as plt


def plot_fitness(generationsResult):
    best = list(map(lambda result: result["best"], generationsResult))
    #mean = list(map(lambda result: result["mean"], generationsResult))
    #worst = list(map(lambda result: result["worst"], generationsResult))
    plt.plot(best, label="best")
    #plt.plot(mean, label="mean")
    #plt.plot(worst, label="worst")

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Knapsack Problem")
    plt.legend(loc='lower left', frameon=True)

    plt.show()

def run_genetic_algorithm(arg0, arg1, arg2, arg3):
    config = Config({
        'problem': {
            'type': ProblemType.MINIMIZATION,
            'nodes': arg0,
            'origdestnodes': arg1,                   # origin and destination nodes
            'n_nodes': arg2,                         # number of intermediate nodes in between origin
            'queuedelays': [0, 0, 0, 0, 0],          # queue delay of nodes, it depends on traffic intensity
            'procdelays': [3, 3, 3, 3, 3],           # default processing delay in ms, acc Kurose/Ross
            'distances': [[0,2,9,3,6], \
                          [2,0,4,3,8], \
                          [9,4,0,7,3], \
                          [3,3,7,0,3], \
                          [6,8,3,3,0]],              # matrix of distances amongst nodes in the network
            'propspeeds': [[  0, 200, 300, 200, 300], \
                           [200,   0, 200, 200, 300], \
                           [300, 200,   0, 230, 200], \
                           [200, 200, 230,   0, 290], \
                           [300, 300, 200, 290,   0]], # in M m/s depend on physical link
                                                     # propagation speed amongst nodes matrix
            'transmitrates': [[0,    10,  100, 100,  10], \
                              [10,    0,   10, 100,  10], \
                              [100,  10,    0,  10, 100], \
                              [100,  100, 100,   0, 100], \
                              [10,    10, 100, 100,   0]],  # in Mbps depend on switches/routers
                                                         # nodes transmission rates matrix
            'packetLength': arg3,   # packet length in bytes to be transmitted from Node A to Node B
            'limit': 0
        },
        'selection': {
            'strategy': SelectionStrategy.ROULETTE
        },
        'reproduction': {
            'strategy': ReproductionStrategy.SEXUAL_SINGLE_POINT,
            'rate': 0.4
        },
        'mutation': {
            'strategy': MutationStrategy.SWAP,
            'rate': 0.1
        },
        'generation': {
            'strategy': GenerationStrategy.EXCHANGE,
            #'substituted_population_size': 10, #Used only on STEADY_STATE
            'population_size': 10,
        },
        'stop_criteria': {
            #'fitness': 0, #Used only on MAX_FITNESS
            'num_generations': 10, #Used only on MAX_GENERATIONS and STEADY_PERIOD
            'quorum': 0.95,  #Used only on CONVERGENCE
            'type': StopCriteriaType.CONVERGENCE
        }
    })



    generationsResult = GeneticAlgorithmFacade(config).execute()

    #plot_fitness(generationsResult)
if __name__ == "__main__":
    nodes = [1, 2, 3, 4, 5] # nodes in the network
    hops = 3 # número de nós intermediário entre 2 pontos da rede (hops)
    nbytes_to_send = 1000 # send 1000 bytes
    n=len(nodes)
    for i in range(1,n):             # n
        for j in range(i+1,n+1):     # n + 1
            print('i=',i,'j=',j)
            orig_dest = [i, j]
            run_genetic_algorithm(nodes, orig_dest, hops, nbytes_to_send)