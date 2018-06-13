from gasman import get_map
from operator import mod 
import numpy as np

def fitness(individual, target, gen=0, ngen=0):
    """
    Determine the fitness of an individual. Higher is better.

    individual: the individual to evaluate
    target: the target number individuals are aiming for
    """

    source = get_conf('source')
    radius = int(get_conf('radius'))
    verbose = bool(get_conf('verbose'))
    delimiter = get_conf('delimiter')
    the_map = get_map(source, delimiter)
    type(the_map)

    d = pow(10, len(str(individual[0]))/2)
    mask_matrix = np.ones(the_map.shape, dtype=int)
    
    for i in individual:
        x = int(i/d)
        y = mod(i,d)
        mask_matrix = put_points(mask_matrix, radius, x, y)

    res = the_map * mask_matrix

    # if verbose and ngen!=0:
    if verbose:
        print "Generation: " + str(gen) + "/" + str(ngen) +" \tFilled area: %.2f " % (res.sum()/float(the_map.sum() *2) * 100) + "% \tFitness error: " + str(1/float(res.sum()))

    return 1/float(res.sum())

def get_conf(param):

    """
    Get some parameter value from configuration file.

    param: parameter name
    """
    
    f = open('conf.tmp', 'r')
    for line in f:
        if param in line:
            f.close()
            line = line.split(':')[1].rstrip()
            if param == 'delimiter' and not line:
                return ' '
            else:
                return line



def put_points(mask_matrix, r, x, y):

    """
    Create a mask for a given x, y coords and return a matrix with a circle filled

    mask_matrix: numpy array with the same size of the map.
    r: radius from argparse.
    x: x coord.
    y: y coord.
    """

    nx, ny = mask_matrix.shape
    Y, X = np.ogrid[-x:nx-x, -y:ny-y]
    mask = X*X + Y*Y <= r*r
    mask_matrix[mask] = 2

    return mask_matrix

