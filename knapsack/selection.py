import random
from enum import IntEnum

from knapsack. problem import ProblemType

class SelectionStrategy(IntEnum):
    ROULETTE = 1,
    TOURNAMENT_BATTLE_ROYALE = 2,
    TOURNAMENT_PLAYOFF = 3

class Selection:
    def __init__(self, problem, strategy):
        self.problem = problem
        self.strategy = strategy

    def execute(self, population, population_size=-1, single=True):
        if population_size != -1:
            sample_population = random.sample(population, k=population_size)
        else:
            sample_population = population

        if self.strategy == SelectionStrategy.ROULETTE:
            return self.roulette(sample_population) if single else self.roulette_pick(sample_population)
        elif self.strategy == SelectionStrategy.TOURNAMENT_BATTLE_ROYALE:
            return self.battle_royale_tournament(sample_population) if single \
                else self.tournament_pick(sample_population, self.battle_royale_tournament)
        elif self.strategy == SelectionStrategy.TOURNAMENT_PLAYOFF:
            return self.playoff_tournament(sample_population)if single \
                else self.tournament_pick(sample_population, self.playoff_tournament)
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid selection")

    def roulette_pick(self, population):
        roulette_pop = population[:]

        first = self.roulette(roulette_pop)
        second = self.roulette(roulette_pop)

        return first, second

    def tournament_pick(self, population, tournament):
        tournament_pop = population[:]

        best = tournament(tournament_pop)

        tournament_pop.remove(best)
        second = tournament(tournament_pop)

        return best, second

    def roulette(self, population):
        fitness_sum = sum(self.problem.getFitness3(individual) for individual in population)
        draw = random.uniform(0, 1)

        accumulated = 0
        for individual in population:
            fitness = self.problem.getFitness3(individual)
            probability = fitness / fitness_sum
            accumulated += probability

            if draw <= accumulated:
                return individual

    def battle_royale_tournament(self, population):
        best = None
        for i in range(0,len(population)):
            ind = population[i]
            if (best == None) or self.compareFitness(ind, best):
                best = ind

        return best

    def playoff_tournament(self, population):
        num_contestants = len(population)
        half = (num_contestants - 1) // 2 + 1

        if num_contestants >= 3:
            finalists = (self.playoff_tournament(population[0:half]), self.playoff_tournament(population[half:num_contestants]))

            return finalists[0] if self.compareFitness(finalists[0], finalists[1]) else finalists[1]
        elif num_contestants == 2:
            return population[0] if self.compareFitness(population[0], population[1]) else population[1]
        elif num_contestants == 1:
            return population[0]

        return []
    
    def compareFitness(self, ind, best):
        if self.problem.type == ProblemType.MAXIMIZATION:
            return self.problem.getFitness(ind) > self.problem.getFitness(best)
        elif self.problem.type == ProblemType.MINIMIZATION:
            return self.problem.getFitness(ind) < self.problem.getFitness(best)
        else:
            self.invalid_problem_type()

    def compareFitness2(self, ind, best):
        if self.problem.type == ProblemType.MAXIMIZATION:
            return self.problem.getFitness2(ind) > self.problem.getFitness2(best)
        elif self.problem.type == ProblemType.MINIMIZATION:
            return self.problem.getFitness2(ind) < self.problem.getFitness2(best)
        else:
            self.invalid_problem_type()

    def compareFitness3(self, ind, best):
        if self.problem.type == ProblemType.MAXIMIZATION:
            return self.problem.getFitness3(ind) > self.problem.getFitness3(best)
        elif self.problem.type == ProblemType.MINIMIZATION:
            return self.problem.getFitness3(ind) < self.problem.getFitness3(best)
        else:
            self.invalid_problem_type()

    def invalid_problem_type(self):
        raise Exception("Invalid problem type")