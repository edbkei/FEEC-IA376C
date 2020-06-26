from knapsack. stop_criteria import StopCriteriaType

class GeneticAlgorithmFacade:
    def __init__(self, config):
        self.config = config

    def execute(self):
        fo1=open("file1.txt","w")
        fo2=open("file2.txt","w")
        fo3=open("file3.txt","a")

        population = self.config.generation.generate_population2(self.config.population_size,
                                                                self.config.problem.nodes,
                                                                self.config.problem.origdestnodes,
                                                                self.config.problem.n_nodes)
        results = []
        best_individual = None
        i = 1
        countBreak=1
        countPeriod = 1
        print("Processing ...generating file1.txt for graphics and file2.txt for detailed population generations")
        while True:
            arg="Generation {"+str(i)+"}"+"\n"
            fo2.write(arg)

            for individual in population:
                arg=str(individual)+" Fitness: "+str(self.config.problem.getFitness3(individual))+ \
                      " Queue: "+str(self.config.problem.apply_queuedelayss(individual))+ \
                      " Limit: "+str(self.config.problem.apply_procdelays(individual))+ \
                      " Distance: "+str(self.config.problem.apply_distances(individual))+"\n"
                fo2.write(arg)

            sorted_population = self.config.generation.sort_population_by_fitness(population)

            worst_fitness = self.config.problem.getFitness3(sorted_population[-1])
            best_fitness = self.config.problem.getFitness3(sorted_population[0])
            mean_fitness = self.config.problem.meanFitness(population)

            fo2.write("\n")
            arg="Best: "+str(best_fitness)+ "\n"
            fo2.write(arg)
            fo2.write("\n")
            dist = self.config.problem.apply_distances(individual)
            arg=str(i)+","+str(best_fitness)+","+str(dist)+"\n"
            fo1.write(arg)

            results.append({
                'best': best_fitness,
            })
            population = self.config.generation.next_generation(population, num_new_individuals=self.config.substituted_population_size)
            best_gen_ind = sorted_population[-1]
            dist = self.config.problem.apply_distances(individual)
            fo2.write(str(best_gen_ind)+'fitness='+str(self.config.problem.getFitness3(best_gen_ind))+' ms distance='+str(dist)+'Km')
            #print(str(best_gen_ind),' fitness=',str(self.config.problem.getFitness3(best_gen_ind)),'ms distance=',str(dist),'Km')
            if best_individual == None or self.config.generation.selection.compareFitness3(best_gen_ind, best_individual):
                best_individual = best_gen_ind[:]
                countPeriod = 1
            else:
                countPeriod += 1

            if self.stop_criteria(generation=i, period=countPeriod, fitness=best_fitness, population=sorted_population):
                countBreak=i
                break

            i += 1

        print("\nBest choice: ")
        print('Best network sequence',best_individual, "- Fitness:", self.config.problem.getFitness3(best_individual),'ms',
                      "- Distances: ", self.config.problem.apply_distances(best_individual),'Km',
                      "- Generations at stop criteria:", countBreak)
        fo3.write(str(best_individual)+'; '+str(self.config.problem.getFitness3(best_individual))+'; '+\
                  str(self.config.problem.apply_distances(best_individual))+'; '+str(countBreak)+'\n')
        #self.config.population_size,
        #self.config.problem.nodes,
        #self.config.problem.origdestnodes,
        #self.config.problem.n_nodes)

        fo1.close()
        fo2.close()
        fo3.close()

        return results

    def stop_criteria(self, generation=None, period=None, fitness=None, population=None):
        if self.config.stop_criteria.type == StopCriteriaType.MAX_GENERATIONS:
            return generation == self.config.stop_criteria.num_generations
        elif self.config.stop_criteria.type == StopCriteriaType.MAX_FITNESS:
            return fitness == self.config.stop_criteria.fitness
        elif self.config.stop_criteria.type == StopCriteriaType.CONVERGENCE:
            num_best = round(self.config.stop_criteria.quorum * len(population))
            count = sum(self.config.problem.getFitness3(pop) == fitness for pop in population)

            return count >= num_best
        elif self.config.stop_criteria.type == StopCriteriaType.STEADY_PERIOD:
            return period == self.config.stop_criteria.num_generations
        else:
            self.invalid()


    def invalid(self):
        raise Exception("Invalid criteria")