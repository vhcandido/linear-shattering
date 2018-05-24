#include <iostream>
#include <vector>
#include <algorithm>
#include <array>
#include <stdio.h>

class Graph {
	public:
		Graph(int V, int min);
		~Graph();

		int get_E();
		int get_count_ways();
		void set_debug(int debug);
		void load(char *filename);
		void insert_edge(int u, int v);
		void remove_edge(int u, int v);
		void print_graph();
		void iterate_edges(int cur, int depth);
		void CC();
		void DFS(int v);
		void print_CC();
		void add_if_new();
		void print_ways();
		void print_edges_cut();

	private:
		int V;
		int E;
		int h;
		int max_CC;
		int max_depth;
		int count;
		int count_ways;
		int debug;
		std::vector<std::vector<int>> edges_cut;
		std::vector<int> *adj;
		std::vector<std::array<int,2>> edges;
		std::vector<int> id;
		std::vector<bool> marked;
		std::vector<std::vector<int>> ways;
};

Graph::Graph(int V, int h) : id(V, -1), marked(V, false) {
	this->V = V;
	this->E = 0;
	this->h = h;
	this->max_CC = 2;
	this->max_depth = 0;
	this->count = 0;
	this->count_ways = 0;
	this->debug = false;
	this->adj = new std::vector<int>[V];
}

Graph::~Graph() {}

int Graph::get_E() { return this->E; }

void Graph::set_debug(int debug) { this->debug = debug; }

int Graph::get_count_ways() { return count_ways; }

void Graph::insert_edge(int v, int w) {
	adj[v].push_back(w);
	adj[w].push_back(v);
	E++;
}


void Graph::remove_edge(int v, int w) {
	adj[v].erase(remove(adj[v].begin(), adj[v].end(), w), adj[v].end());
	adj[w].erase(remove(adj[w].begin(), adj[w].end(), v), adj[w].end());
	E--;
}

void Graph::load(char *filename) {
	int v, w;
	FILE *file;

	// open file for reading
	file = fopen(filename, "r");
	if (!file) {
		fprintf(stderr, "error: while trying to open '%s' for reading\n", filename);
		exit(EXIT_FAILURE);
	}

	// read each vertice pair and add edge
	while(fscanf(file, "%d %d", &v, &w) == 2) {
		insert_edge(v, w);

		std::array<int,2> e = {v,w};
		edges.push_back(e);
	}
	fclose(file);

	max_depth = E/2;
}

void Graph::print_graph() {
	printf("\n Total of %d edges:\n", this->E);
	for (int v = 0; v < this->V; ++v) {
		printf(" %d ->", v);
		for (int w : this->adj[v]) {
			printf(" %d", w);
		}
		printf("\n");
	}
	printf("\n");
}

void Graph::print_edges_cut() {
	for (std::vector<int> e : edges_cut) {
		printf(" (%d,%d)", e[0], e[1]);
	}
	printf("\n");
}

void Graph::iterate_edges(int cur, int depth) {
	edges_cut.reserve(edges.size());
	if (depth >= max_depth) return;

	depth++;
	for (int i = cur; i < edges.size(); ++i) {
		remove_edge(edges[i][0], edges[i][1]);
		std::vector<int> e = {edges[i][0], edges[i][1]};
		edges_cut.push_back(e);

		iterate_edges(i+1, depth);

		if (depth >= h) { // minimum of h cuts to disconnect the graph
			if (debug > 1) print_edges_cut();
			CC();

			if (debug > 2) print_graph();
			if (count == max_CC) { // found max_CC components
				add_if_new();
			}
		}

		insert_edge(edges[i][0], edges[i][1]);
		edges_cut.pop_back();
	}
	depth--;
}

void Graph::add_if_new() {
	bool new_way = true;
	for (std::vector<int> w : ways) {
		if(w == id) {
			new_way = false;
			break;
		}
	}

	if(new_way) {
		ways.push_back(id);

		std::for_each(id.begin(), id.end(), [](int &x){ x = !x; });
		ways.push_back(id);

		count_ways += 2;

		if (debug > 0) {
			printf(" [NEW] ");
			print_CC();
		}
	}
}

void Graph::CC() {
	std::fill(marked.begin(), marked.end(), false);
	std::fill(id.begin(), id.end(), -1);
	count = 0;
	for (int v = 0; v < V; ++v) {
		if (!marked[v]) {
			if(++count > max_CC) return;
			DFS(v);
		}
	}
}

void Graph::DFS(int v) {
	marked[v] = true;
	id[v] = count-1;
	for (int w : adj[v]) {
		if(!marked[w]) DFS(w);
	}
}

void Graph::print_CC() {
	printf(" v  ->");
	for(int v = 0; v < V; ++v) {
		printf("%2d ", v);
	}
	printf("\n CC ->");
	for(int i : id) {
		printf("%2d ", i);
	}
	printf("\n");
}

void Graph::print_ways() {
	for (std::vector<int> w : ways) {
		for (int c : w) {
			printf(" %d", c);
		}
		printf("\n");
	}
}

enum {
	PROGNAME,
	N,
	H,
	FILENAME,
	NARGS
};

int main(int argc, char **argv) {
	if (argc != NARGS) {
		fprintf(stderr, "usage: %s n h file\n", argv[PROGNAME]);
		exit(EXIT_FAILURE);
	}

	printf("-> Initializing graph\n");
	Graph G((int) atoi(argv[N]), atoi(argv[H]));
	G.set_debug(0);

	printf("-> Loading edges from %s\n", argv[3]);
	G.load(argv[3]);

	printf("-> Printing generated graph\n");
	G.print_graph();

	printf("-> Iterating\n");
	G.iterate_edges(0, 0);

	// +2 because of all positive/negative
	printf("\n-> %d ways of disconnecting G into 2 CC were found\n", G.get_count_ways()+2);
	G.print_ways();

	return 0;
}
