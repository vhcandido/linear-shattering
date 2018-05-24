# Disconnecting a graph in 2 connected components

## Files
* `src/create_edges.c`: outputs a list of edges for an 1 or 2-dimensional graph with `n` vertices
  * to compile from `src/` subdirectory: `make create_edges`
* `src/disconnect_graph.cpp`: outputs the number of ways (and the patterns obtained) of disconnecting an `h`-dimensional graph with `n` vertices in 2 connected components.
  * to compile from `src/` subdirectory: `make disconnect_graph`

## Creating graph file
From the `src/` subdirectory:  
`./create_edges n h`  
`./create_edges 9 1 > ../graphs/h1n9.dat`  
`./create_edges 7 2 > ../graphs/h2n7.dat`  

## Counting ways of disconnecting G in 2 CC
From the `src/` subdirectory:  
`./disconnect_graph n h filename`  
`./disconnect_graph 9 1 ../graphs/h1n9.dat`  
`./disconnect_graph 4 2 ../graphs/h2n4.dat`  
`./disconnect_graph 8 3 ../graphs/h3n8_cube.dat`  
