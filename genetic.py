import circle_fitness
import travel_fitness
from random import randint, random
from operator import add

def individual(length, min, max):
    'Create a member of the population.'
    return [ randint(min,max) for x in xrange(length) ]

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values

    """
    return [ individual(length, min, max) for x in xrange(count) ]

def grade(pop, target, situation, gen=0, ngen=0):
    'Find average fitness for a population.'
    
    l = []
    if situation == 'travel':
        for x in pop:
            l.append(travel_fitness.fitness(x, target, gen, ngen))
    
    elif situation == 'circle':
        for x in pop:
            l.append(circle_fitness.fitness(x, target, gen, ngen))
    
    return min(l)

def evolve(pop, target, situation, gen, ngen, retain=0.2, random_select=0.05, mutate=0.01):
    
    if situation == 'travel':
        graded = [ (travel_fitness.fitness(x, target, gen, ngen), x) for x in pop]
    elif situation == 'circle':
        graded = [ (circle_fitness.fitness(x, target, gen, ngen), x) for x in pop]

    graded = [ x[1] for x in sorted(graded)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]
    # randomly add other individuals to
    # promote genetic diversity

    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []

    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)

        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:half] + female[half:]
            children.append(child)        
    parents.extend(children)

    return parents
