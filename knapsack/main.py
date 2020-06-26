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
    mean = list(map(lambda result: result["mean"], generationsResult))
    worst = list(map(lambda result: result["worst"], generationsResult))
    plt.plot(best, label="best")
    plt.plot(mean, label="mean")
    plt.plot(worst, label="worst")

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Knapsack Problem")
    plt.legend(loc='lower left', frameon=True)

    plt.show()

if __name__ == "__main__":
    config = Config({
        'problem': {
            'type': ProblemType.MAXIMIZATION,
            'values': [0, 1],
            'costs': [100, 350, 200, 90, 500, 250, 220, 360, 150, 700, 400, 230, 550],
            'weights': [50, 90, 30, 40, 100, 70, 20, 80, 80, 90, 50, 30, 70],
            'cargo': 600
        },
        'selection': {
            'strategy': SelectionStrategy.TOURNAMENT_BATTLE_ROYALE
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
            'population_size': 25,
        },
        'stop_criteria': {
            #'fitness': 0, #Used only on MAX_FITNESS
            #'num_generations': 100, #Used only on MAX_GENERATIONS and STEADY_PERIOD
            'quorum': 0.95,  #Used only on CONVERGENCE
            'type': StopCriteriaType.MAX_GENERATIONS
        }
    })



    generationsResult = GeneticAlgorithmFacade(config).execute()

    plot_fitness(generationsResult)