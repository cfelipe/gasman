import numpy as np
import circle_fitness

def fitness(individual, target, gen=0, ngen=0):
    """
    Determine the fitness of an individual. Higher is better.

    individual: the individual to evaluate
    target: the target number individuals are aiming for
    """

    verbose = bool(circle_fitness.get_conf('verbose'))

    f = open ( 'travel.mat' , 'r')
    M = [[float(num) for num in line.split(' ')] for line in f ]
    M = np.array(M)
    f.close()

    cities = np.zeros(len(M), dtype=int)
    cost = 0
    i = 0
    value = 1

    ind = individual[:]

    for r in range(len(ind)):
        cities[ind.index(min(ind))] = value
        ind[ind.index(min(ind))] = max(ind) +1
        value += 1

    for c in cities:
        if i < len(cities) -1:
            cost += M[cities[i] -1][cities[i+1] -1]
        i += 1

    cost += M[cities[-1] -1][cities[0] -1]
    
    if verbose:
        print "Generation: " + str(gen) + "/" + str(ngen) +" \tCost: " + str(cost) + " \tFitness error: " + str(cost)

    return cost
