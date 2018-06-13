import matplotlib.pyplot as plt
from matplotlib import cm
from operator import mod 
import circle_fitness
import travel_fitness
import numpy as np
import argparse
import genetic
import math
import time

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="the matrix.dat file", required=True)
    parser.add_argument("-r", "--radius", help="radius size in pixels", type=int, required=True)
    parser.add_argument("-d", "--delimiter", help="dat file elements delimiter", default=' ')
    parser.add_argument("-cp", "--circle-population", help="initial population for circle optimization (default=100)", type=int, default=100)
    parser.add_argument("-cg", "--circle-generation", help="generation number for circle optimization (default=100)", type=int, default=100)
    parser.add_argument("-tp", "--traveller-population", help="initial population for traveller optimization (default=100)", type=int, default=100)
    parser.add_argument("-tg", "--traveller-generation", help="generation number for traveller optimization (default=100)", type=int, default=100)
    parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")
    parser.add_argument("-nl", "--no-line", help="hide route line between cities", action="store_true")
    parser.add_argument("-sc", "--simple-colors", help="use just one color to draw circles", action="store_true")
    parser.add_argument("-t", "--execution-time", help="show script execution time", action="store_true")

    args = parser.parse_args()
    create_conf_file(args)

    start = time.time()
    the_map = get_map(args.source, args.delimiter)
    npoints = get_number_of_points(args.radius, the_map.shape)
    deltap  = get_delta_population(the_map.shape)
    bestc   = optimize(npoints, deltap, args.circle_population, args.circle_generation, situation='circle')
    bestc, filled = fit_circle_pop(bestc, the_map, args.radius)
    build_matrix(bestc)

    bestr = optimize(len(bestc), len(bestc)+100, args.traveller_population, args.traveller_generation, situation='travel')
    route, cost = fit_traveller_pop(bestr, args)
    end = time.time()
    exec_time = (end - start)

    print "Done!"
    plot(bestc, filled, route, the_map, args.radius, cost, args, exec_time)

    # destroy_conf_file

def get_map(source, delimiter):

    """
    Create a numpy array from the matrix.dat file.

    source: name of the .dat file

    """

    if source == 'mapa_source.dat':
        delimiter = '  '

    f = open(source, 'r')
    the_map = [[int(num) for num in line.split(delimiter)] for line in f ]
    f.close()

    return np.array(the_map)
    

def get_number_of_points(r, shape):

    """
    Return the number of circles to fill the entire area of the map.

    r: radius from argparse
    shape: shape from numpy array

    """

    h, l = shape
    return int(h*l / (math.pi * math.pow(r, 2)))


def get_delta_population(shape):

    """
    Return the maximum possible value for a given .dat file

    shape: shape from numpy array

    """

    h, l = shape
    return int(str(h) + str(l))


def optimize(npoints, deltap, ipop, ngen, situation):

    """
    Call genetic functions and return the best population.

    npoints: number of values per individual 
    deltap: maximum possible value in an individual's list of values
    ipop: number of initial population
    ngen: number of generations
    situation: circle or travel
    """

    target = 0
    p = genetic.population(ipop, npoints, 0, deltap)
    fitness_history = [genetic.grade(p, target, situation, ngen=ngen),]

    for i in xrange(ngen):
        p = genetic.evolve(p, target, situation, i, ngen)
        fitness_history.append(genetic.grade(p, target, situation, gen=i, ngen=ngen))

    return p.pop()


def create_conf_file(args):

    """
    Create a configuration file with all the important parameters. This is
    usefull because script can access all these parameters from everywhere in code.

    args: argparse object

    """

    f = open('conf.tmp', 'w')

    for arg in vars(args):
        if isinstance(getattr(args, arg), bool) and not(getattr(args, arg)):
            line = arg + ':' + '' + '\n'
        else:
            line = arg + ':' + str(getattr(args, arg)) + '\n'
        
        f.write(line)

    f.close()


def plot(bestc, filled, bestr, the_map, radius, cost, args, exec_time):

    """
    Plot results. 

    bestc: best circle population
    filled: percentage of filled area
    bestr: best route population
    the_map: numpy array with matrix.dat data
    radius: radius from argparse
    cost: cost of travel returned by genetic traveller fitness
    args: argparse object
    
    """

    i = 2
    cost = "%.2f" % cost
    tmp = np.ones(the_map.shape, dtype=int)
    nx, ny = the_map.shape

    for c in bestc:
        a, b = c
        y, x = np.ogrid[-a:nx-a, -b:ny-b]
        mask = x*x + y*y <= radius*radius
        tmp[mask] = i
        if not args.simple_colors:
            i += 1

    res = tmp * the_map
    x1 = []
    y1 = []

    for r in bestr:
        v1, v2 = bestc[r -1]
        x1.append(v2)
        y1.append(v1)

    cmap_custom = cm.Blues
    cmap_custom.set_under('0.75')
    plt.matshow( res, interpolation='nearest' ,cmap=cmap_custom, vmin=0.01)
   
    if not args.no_line:
        i = 1
        plt.plot(x1, y1, color='green', marker='o')
        for p, q in zip(x1, y1):
            plt.text(p, q, str(i), color='black', fontsize=12)
            i += 1

    if args.execution_time:
        plt.title(str(len(bestr)) + ' points | %.2f' % filled + '% filled | ' + str(cost) + ' km costed  | ' + 'execution time: %.2f' % exec_time + 's')
    else:
        plt.title(str(len(bestr)) + ' points | %.2f' % filled + '% filled | ' + str(cost) + ' km costed')

    plt.show()



def fit_circle_pop(best, the_map, radius):

    """
    Make sure that best circle population only contains coords inside the map.

    best: best circle population
    the_map: numpy two dimensional array
    radius: radius from argparse

    """

    d = pow(10, len(str(best[0]))/2)
    mask_matrix = np.ones(the_map.shape, dtype=int)
    
    for i in best:
        x = int(i/d)
        y = mod(i,d)
        mask_matrix = circle_fitness.put_points(mask_matrix, radius, x, y)

    res = the_map * mask_matrix
    valids = []

    for i in best:
        x = int(i/d)
        y = mod(i,d)

        try:
            if res[x][y] == 2:
                valids.append((x,y))
        except IndexError:
            pass

    return valids, (res.sum()/float(the_map.sum() *2) * 100) 


def fit_traveller_pop(ind, args):

    """
    Fit best travel population and return the order of cities and cost of travel.

    ind: best travel population
    args: argparse object

    """

    args.verbose = False
    create_conf_file(args)
    individuals = ind[:]

    cities = np.zeros(len(ind), dtype=int)
    value = 1

    for r in range(len(ind)):
        cities[ind.index(min(ind))] = value
        ind[ind.index(min(ind))] = max(ind) +1
        value += 1

    return  np.append(cities, cities[0]), travel_fitness.fitness(individuals, 0)



def build_matrix(best):

    """
    Build a cost matrix where each element represent a cost between different cities.

    best: circle coords from best circle population

    """

    matrix = np.zeros((len(best), len(best)))

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            xa, ya = best[i]
            xb, yb = best[j]
            matrix[i][j] = math.sqrt(math.pow((xb - xa), 2) + math.pow((yb - ya), 2))

    np.savetxt('travel.mat', matrix, fmt='%.2f', delimiter=' ')



if __name__ == "__main__":
    main()
