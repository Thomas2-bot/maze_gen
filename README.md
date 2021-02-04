# Maze Generator and Solver using Pygame
1. [the idea](#the-idea)
2. [random generation](#random-generation)
3. [solving algorithm](#solving-algorithm)
4. [efficiency](#efficiency)

## the idea
Though the idea of the random generation of mazes is quite old, this was a necessary step during my TIPE (the ~~silly~~ thing *they* make us do in french *classes préparatoires aux grandes écoles*). The original idea was the optimisation of the travel time of sail boats. Intense. So I needed some sort of optimisation algorithm, and some code to test it on basic cases. Here it goes.

## random generation
The algorithm used for the randomisation of the generation of mazes is a famous one, nothing too fancy, but effective nonetheless : the randomized depth-first search. Its name comes from a mathematical study branch called graph theory, and the basic thing it does is returning a random path (exploring all neighbors of all cells one by one and choosing one), get stuck eventually and then going back were it was last not stuck. This describes the traversing depth-first search algorithm for tree of graph data structure (tree because all cells in the graph has some parent and children), and provides us with a maze that has only one possible path through the end.

## solving algorithm
Some effective solving algorithm would be the A* algorithm. But because of the randomizeness of the maze I'm trying to solve, I have implemented the dijkstra algorithm in the case were there is only one possible path. Dijkstra also refers to some graph theory thing and thus we need some data structure to implement a sort of tree with comparisson methods. So as long as the algorithm is looking for new nodes to explore, they are store in a priority queue to speed up things (putting and getting elements), and the ones already explored are stored in a set so that we can access them in constant time.

## efficiency
This generating-solving maze was typically tested with 300 by 300 mazes. Although it can handle larger ones, it is highly likely that they won't be displayed properly. Time generation for this size of maze is around 2 minutes, exporting to text file (can be found inside the export folder) is less than a second and solving takes a couple of seconds. Time generation could be much higher if only pygame would allow us to have more than 1250 frames. To test it, simply tweak somes constants in [constants.py](constants.py) and run [main.py](main.py).