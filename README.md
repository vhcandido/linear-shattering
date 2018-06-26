# Shatter functions of half-space intersections

## Files
* `python/utils.py`: utilities to manipulate classification patterns
* `python/polygon.py`: generates regular polygon and the number of possible cuts joining 2 edges
* `src/create_edges.c`: outputs a list of edges for an 1 or 2-dimensional graph with `n` vertices
  * to compile from `src/` subdirectory: `$ make create_edges`
* `src/disconnect_graph.cpp`: outputs the number of ways (and the patterns obtained) of disconnecting an `h`-dimensional graph with `n` vertices in 2 connected components.
  * to compile from `src/` subdirectory: `$ make disconnect_graph`

## Loading cuts/ways
Here I considered a _cut_ as a representation of a linear hyperplane that cuts a graph and _ways_ as the possible patterns obtained by classifying with a given cut (hyperplane).  
```python
import utils

w_cube = utils.mirror_invert(utils.load_cuts("../patterns/c_h3n8_cube.dat"))
# or
w_cube = utils.load_ways("../patterns/w_h3n8p1_cube.dat")

print(w_cube.shape[0])
# 104
```

## Combining ways for p hyperplanes
```python
import numpy as np
import utils

#####################
w_cube = utils.load_ways("../patterns/w_h3n8p1_cube.dat")
w_cube_p1 = utils.combine_hyperplanes(w_p1=w_cube, p=1)
w_cube_p2 = utils.combine_hyperplanes(w_p1=w_cube, p=2)
w_cube_p3 = utils.combine_hyperplanes(w_p1=w_cube, p=3)
print(w_cube_p1.shape[0], w_cube_p2.shape[0], w_cube_p3.shape[0])

#####################
import polygon
w_octa_p1 = polygon.ways(n=8, h=2, p=1)
# or with util.load_ways("../patterns/w_h2n8p1.dat), if the file exists

w_octa_p3 = polygon.ways(n=8, h=2, p=3)
# or
w_octa_p3 = utils.combine_hyperplanes(w_octa_p1, p=3)

print(w_octa_p1.shape[0], w_octa_p3.shape[0])
```

## Comparing different sets of patterns
It's possible to compare different set of patterns, for example the results obtained with a 8-point line {n=8, h=1, p=3} and a cube {n=8, h=3, p=1}:
```python
import numpy as np
import utils

# load ways for p=1 in h=1 and combine it for p=3
w_h1n8p1 = utils.load_ways("../patterns/w_h1n8p1.dat")
w_h1n8p3 = utils.combine_hyperplanes(w_h1n8p1, 3)
w_linear = w_h1n8p3 # easier name

# load ways for p=1 in h=3
w_h3n8p1 = utils.load_ways("../patterns/w_h3n8p1_cube.dat")
w_cube = w_h3n8p1 # easier name

print(w_linear.shape[0], w_cube.shape[0])
# 128 104

# get which patterns from w_h1n8p3 (linear) are NOT in w_h3n8p1 (cube)
idx = utils.which_not_match(w_linear, w_cube)
print(idx.shape[0])
# 50
print(w_linear[idx])

# get which patterns from w_h3n8p1 (cube) are NOT in w_h1n8p3 (linear)
idx = utils.which_not_match(w_cube, w_linear)
print(idx.shape[0])
# 26
print(w_cube[idx])
```


## Creating graph file
From the `src/` subdirectory: `$ ./create_edges n h`  
```bash
$ ./create_edges 9 1 > ../graphs/h1n9.dat  
$ ./create_edges 7 2 > ../graphs/h2n7.dat  
```

## Counting ways of disconnecting G in 2 CC
From the `src/` subdirectory: `$ ./disconnect_graph n h filename`  
```bash
$ ./disconnect_graph 9 1 ../graphs/h1n9.dat  
$ ./disconnect_graph 4 2 ../graphs/h2n4.dat  
$ ./disconnect_graph 8 3 ../graphs/h3n8_cube.dat  
```
