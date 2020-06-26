import random
import secrets
from enum import IntEnum


class ReproductionStrategy(IntEnum):
    ASEXUAL = 1,
    SEXUAL_SINGLE_POINT = 2,
    SEXUAL_DOUBLE_POINTS = 3

class Reproduction:
    def __init__(self, strategy, rate):
        self.strategy = strategy
        self.rate = rate

    def execute(self, individual_a, individual_b=None):
        if self.strategy == ReproductionStrategy.ASEXUAL:
            return self.duplication(individual_a)
        elif self.strategy == ReproductionStrategy.SEXUAL_SINGLE_POINT:
            return self.crossover_single_point(individual_a, individual_b)
        elif self.strategy == ReproductionStrategy.SEXUAL_DOUBLE_POINTS:
            return self.crossover_double_points(individual_a, individual_b)
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid reproduction")

    def duplication(self, individual):
        return individual[:]

    def crossover_single_point(self, individual_a, individual_b):
        n = len(individual_b)
        cx=[]
        if(n==3):
            c=random.randint(0,1)
            if(c==0):
                cx=individual_a
            else:
                cx=individual_b
        else:
            c = random.randint(0, n - 1)
            cx=individual_a[0:c]
            if(len(cx)<2):
                return individual_b
            for i in range(0,n):
                ck=0
                m=len(cx)
                for j in range(0,m):
                    if(cx[j]==individual_b[i]):
                        ck=1
                if ck==0:
                    m=len(cx)
                    if(i==n-1):
                        cx.append(individual_b[i])
                        break
                    else:
                        if(m==n-1):
                            cx.append(individual_b[m])
                        else:
                            cx.append(individual_b[i])
                m=len(cx)
                if(m==n):
                    break

        return cx

    def crossover_double_points(self, individual_a, individual_b):
        n = len(individual_a)
        c1 = random.randint(0, n - 2)
        c2 = random.randint(c1, n - 1)
        return individual_a[0:c1] + individual_b[c1:c2] + individual_a[c2:n]
