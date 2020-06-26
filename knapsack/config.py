from knapsack.generation import GenerationManager
from knapsack.mutation import Mutation
from knapsack.problem import KnapsackProblem
from knapsack.reproduction import Reproduction
from knapsack.selection import Selection
from knapsack.stop_criteria import StopCriteria


class Config:
    def __init__(self, configDict):
        self.configuration(configDict)

    def configuration(self, configDict):
        self.problem = KnapsackProblem(type=configDict['problem']['type'],
                                         nodes=configDict['problem']['nodes'],
                                         origdestnodes=configDict['problem']['origdestnodes'],
                                         n_nodes=configDict['problem']['n_nodes'],
                                         queuedelays=configDict['problem']['queuedelays'],
                                         procdelays=configDict['problem']['procdelays'],
                                         distances=configDict['problem']['distances'],
                                         propspeeds=configDict['problem']['propspeeds'],
                                         transmitrates=configDict['problem']['transmitrates'],
                                         packetLength=configDict['problem']['packetLength'],
                                         limit=configDict['problem']['limit'])

        selection = Selection(self.problem, configDict['selection']['strategy'])
        reproduction = Reproduction(configDict['reproduction']['strategy'], configDict['reproduction']['rate'])
        mutation = Mutation(configDict['mutation']['strategy'], configDict['mutation']['rate'])
        self.generation = GenerationManager(self.problem, configDict['generation']['strategy'],
                                              selection, reproduction, mutation)

        self.population_size = configDict['generation']['population_size']
        self.substituted_population_size = self.checkKeyAndReturn(configDict['generation'],
                                                                  'substituted_population_size')

        self.stop_criteria = StopCriteria(configDict['stop_criteria']['type'],
                                          self.checkKeyAndReturn(configDict['stop_criteria'], 'num_generations'),
                                          self.checkKeyAndReturn(configDict['stop_criteria'], 'fitness'),
                                          self.checkKeyAndReturn(configDict['stop_criteria'], 'quorum'))

    def checkKeyAndReturn(self, dict, key):
        return dict[key] if key in dict.keys() else None