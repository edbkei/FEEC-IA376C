from enum import Enum

class ProblemType(Enum):
    MAXIMIZATION = 1,
    MINIMIZATION = 2,

class Problem:
    def __init__(self, type, nodes, origdestnodes, n_nodes, length):
        self.type = type
        self.nodes = nodes
        self.origdestnodes = origdestnodes
        self.n_nodes = n_nodes
        self.population_length = length
    def getFitness(self, population):
        pass

class KnapsackProblem(Problem):
    def __init__(self, type, nodes, origdestnodes, n_nodes, queuedelays, procdelays, distances, propspeeds, transmitrates, packetLength, limit):
        self.origdestnodes = origdestnodes
        self.n_nodes = n_nodes
        self.queuedelays = queuedelays
        self.procdelays = procdelays
        self.distances = distances
        self.propspeeds = propspeeds
        self.transmitrates = transmitrates
        self.packetLength = packetLength
        self.limit = limit
        super(KnapsackProblem, self).__init__(type, nodes, origdestnodes, n_nodes, len(self.queuedelays))
        self.validate()

    def validate(self):
        if (self.limit < 0):
            raise Exception("Limit should be positive")
        if (len(self.queuedelays) <= 0 or len(self.procdelays) <= 0):
            raise Exception("Queue delays and Processing delays should have an item")
        if (len(self.queuedelays) != len(self.procdelays)):
            raise Exception("Queue delays and processing delays should have the same length")

    def validateIndividual(self, individual):
        return len(self.queuedelays) == len(individual) \
               and len(self.procdelays) == len(individual) \
               and self.apply_procdelays(individual) <= self.limit

    def validateIndividual2(self, individual):
        return self.apply_distances(individual) >= self.limit

    def is_minimization_problem(self):
        return self.type ==ProblemType.MINIMIZATION

        for i in range(0, len(population)):
            total += self.getFitness3(population[i])

        return total / len(population)

    def getFitness(self, individual):
        if (self.validateIndividual(individual)):
            return self.apply_delayss(individual)
        return -1

    def getFitness2(self, individual):
        if (self.validateIndividual2(individual)):
            return self.apply_distances(individual)
        return -1

    def getFitness3(self, individual):
        if (self.validateIndividual2(individual)):
            return self.apply_propspeeds(individual)
        return -1

    def apply_queuedelayss(self, individual):
        queue = 0

        for i in range(0, len(individual)):
            queue += individual[i] * self.queuedelays[i]

        return queue

    def apply_procdelays(self, individual):
        procdelay = 0

        for i in range(0, len(individual)):
            procdelay += individual[i] * self.procdelays[i]

        return procdelay

    def apply_distances(self, individual):
        distance = 0
        for i in range(1,len(individual)):
            n=individual[i]-1
            m=individual[i-1]-1
            distance += self.distances[m][n]

        return distance

    def apply_propspeeds(self, individual):
        delay = 0
        for i in range(1,len(individual)):
            n=individual[i]-1
            m=individual[i-1]-1
            x=self.propspeeds[m][n]
            y=self.distances[m][n]
            z=self.transmitrates[m][n]
            w=self.packetLength
            if(i!=len(individual)-1):
                p=self.procdelays[i]
                q=self.queuedelays[i]
            delay += y/x+w/z+p+q

        return delay

    def meanFitness(self, population):
        total = 0

        for i in range(0, len(population)):
            total += self.getFitness(population[i])

        return total / len(population)