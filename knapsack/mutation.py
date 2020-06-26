import random
import secrets
from enum import IntEnum

class MutationStrategy(IntEnum):
    FLIP = 1,
    SWAP = 2,
    SEQUENCE_SWAP = 3

class Mutation:
    def __init__(self, strategy, rate):
        self.strategy = strategy
        self.rate = rate

    def execute(self, individual):
        if self.strategy == MutationStrategy.FLIP:
            return self.flip(individual)
        elif self.strategy == MutationStrategy.SWAP:
            if(len(individual)==3):
                return self.flip(individual)
            return self.swap(individual)
        elif self.strategy == MutationStrategy.SEQUENCE_SWAP:
            return self.sequence_swap(individual)
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid mutation")

    def flip(self, individual):
        if(len(individual)==3):
            ini=individual[0]
            end=individual[2]
            i=0
            mid=0
            while(True):
                n=random.randint(ini,end)
                if(ini!=n and end!=n):
                    mid=n
                    break
                elif(ini<end):
                    if(end-ini==1):
                        if(ini>1):
                            mid=random.randint(1,ini-1)
                            break
                        else:
                            mid=individual[1]
                            break
                    elif(end-ini==2):
                        x=random.randint(0,1)
                        if(x==0):
                            mid=individual[1]
                            break
                        else:
                            mid=ini+1
                            break
                    else:
                        mid=random.randint(ini+1,end-1)
                        break

                elif(end<ini):
                    if(ini-end==1):
                        if(end>1):
                            mid=random.randint(1,end-1)
                            break
                        else:
                            mid=individual[1]
                            break
                    elif(end-ini==2):
                        x=random.randint(0,1)
                        if(x==0):
                            mid=individual[1]
                            break
                        else:
                            mid=end+1
                            break
                    else:
                        mid=random.randint(end+1,ini-1)
                        break
            individual[1]=mid
            return individual
        n = len(individual)
        c = random.randint(0, n - 1)
        m = random.randint(0, 1)
        individual[c] = m
        return individual

    def swap(self, individual):
        n = len(individual)
        pop=individual
        swapped=0
        swapWith=0
        while(swapped==swapWith):
            swapped = random.randint(1, n - 2)
            swapWith = random.randint(1, n - 2)

        aux = individual[swapped]
        individual[swapped] = individual[swapWith]
        individual[swapWith] = aux
        return individual

    def sequence_swap(self, individual):
        n = len(individual)
        while True:
            sequence_swap_init = random.randint(0, n - 2)
            sequence_swap_final = random.randint(sequence_swap_init, n - 1)
            if sequence_swap_init != 0 and sequence_swap_final != n - 1:
                break

        remaining = list(range(0, sequence_swap_init)) + list(range(sequence_swap_final+1, n))
        swapWith = random.choice(remaining)

        if swapWith < sequence_swap_init:
            individual = [] + individual[0:swapWith]\
                + individual[sequence_swap_init:sequence_swap_final + 1]\
                + individual[swapWith:sequence_swap_init]\
                + individual[(sequence_swap_final + 1):len(individual)]
        else:
            individual = [] + individual[0:sequence_swap_init]\
                + individual[(sequence_swap_final + 1):swapWith + 1]\
                + individual[sequence_swap_init:sequence_swap_final + 1]\
                + individual[(swapWith + 1):len(individual)]

        return individual
