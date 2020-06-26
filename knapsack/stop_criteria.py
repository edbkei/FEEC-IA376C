from enum import IntEnum


class StopCriteriaType(IntEnum):
    MAX_GENERATIONS = 1,
    MAX_FITNESS = 2,
    CONVERGENCE = 3,
    STEADY_PERIOD = 4

class StopCriteria:
    def __init__(self, type, num_generations=None, fitness=None, quorum=None):
        self.type = type
        self.num_generations = num_generations
        self.fitness = fitness
        self.quorum = quorum