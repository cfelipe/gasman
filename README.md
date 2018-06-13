# Gasman
Genetic algorithm solution to a different version of the [travelling salesman](https://en.wikipedia.org/wiki/Travelling_salesman_problem) problem.

# The Problem

The goal is to fill a given map with gas stations, where each gas station covers an area with 30m of radius. We want to optize it and get the maxium filled area with the minimum of gas station points possible. Also, we want to run throught all the gas station points in the shortest distance route. 

# Solution Approach 

This problem was solved by multiplying a matrix with a lot of circle areas with the given matrix map. This way, the result is a map with circles inside. All the circles outside the map become zeros. The fitness error here is the sum of resultant matrix map area. After that, a cost matrix was build and genetic algorithm was applyed again to finded the lowerst cost and hence the shortest route.

# Requirements

* *matplotlib* - wich can be installed with pip
* *tk* - this package is probably in your package manager distro
* A somewhat capable hardware. Genetic algorithm is a slow solution.

# Usage Example

```
python gasman.py --source=map.dat --radius=60 --circle-population=100 --traveller-population=100 --verbose
```

![Image of the Map](https://i.imgur.com/RROIZzT.png)

```
python gasman.py --source=map.dat --radius=30 --circle-generation=100 --traveller-population=50 --verbose

Generation: 1/100 	Filled area: 82.83 % 	Fitness error: 0.000276778300581
Generation: 1/100 	Filled area: 84.53 % 	Fitness error: 0.000271223216707
Generation: 1/100 	Filled area: 82.90 % 	Fitness error: 0.000276548672566
Generation: 1/100 	Filled area: 81.18 % 	Fitness error: 0.000282406099972
Generation: 1/100 	Filled area: 80.97 % 	Fitness error: 0.000283125707814
Generation: 1/100 	Filled area: 74.92 % 	Fitness error: 0.00030599755202
Generation: 1/100 	Filled area: 83.72 % 	Fitness error: 0.000273822562979
Generation: 1/100 	Filled area: 81.36 % 	Fitness error: 0.000281769512539

```

![Image of the Map](https://i.imgur.com/xOSJrva.png)

## Other options

```
python gasman.py --help

usage: gasman.py [-h] -s SOURCE -r RADIUS [-d DELIMITER]
                 [-cp CIRCLE_POPULATION] [-cg CIRCLE_GENERATION]
                 [-tp TRAVELLER_POPULATION] [-tg TRAVELLER_GENERATION] [-v]
                 [-nl] [-sc] [-t]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        the matrix.dat file
  -r RADIUS, --radius RADIUS
                        radius size in pixels
  -d DELIMITER, --delimiter DELIMITER
                        dat file elements delimiter
  -cp CIRCLE_POPULATION, --circle-population CIRCLE_POPULATION
                        initial population for circle optimization
                        (default=100)
  -cg CIRCLE_GENERATION, --circle-generation CIRCLE_GENERATION
                        generation number for circle optimization
                        (default=100)
  -tp TRAVELLER_POPULATION, --traveller-population TRAVELLER_POPULATION
                        initial population for traveller optimization
                        (default=100)
  -tg TRAVELLER_GENERATION, --traveller-generation TRAVELLER_GENERATION
                        generation number for traveller optimization
                        (default=100)
  -v, --verbose         verbose mode
  -nl, --no-line        hide route line between cities
  -sc, --simple-colors  use just one color to draw circles
  -t, --execution-time  show script execution time
  
```
