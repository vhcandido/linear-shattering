#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include <iomanip>
#include <ctime>

// http://en.cppreference.com/w/cpp/container/vector/vector
template<typename T>
std::ostream& operator<<(std::ostream& s, const std::vector<T>& v) {
	//s.put('[');
    char comma[2] = {'\0', '\0'};
    for (const auto& e : v) {
        s << comma << std::setw(2) << e;
		comma[0] = ' ';
    }
    return s;
}

class Graph {
	public:
		Graph(int V, int min);
		~Graph();

		int get_E();
		int get_ways_size();
		void set_debug(int debug);
		void load(const char *filename);
		void insert_edge(const int& u, const int& v);
		void remove_edge(const int& u, const int& v);
		void iterate_edges(const int cur, int depth);
		void CC();
		void DFS(int v);
		void add_if_new();
		void print_graph();
		void print_CC();
		void print_ways();

	private:
		int V;
		int E;
		int h;
		int max_CC;
		int max_depth;
		int count;
		int debug;
		std::vector<int> *adj_l;
		std::vector<std::vector<int>> edges;
		std::vector<int> id;
		std::vector<bool> marked;
		std::vector<std::vector<int>> ways;
};

Graph::Graph(int V, int h) : id(V, -1),	marked(V, false) {
	this->V = V;
	this->E = 0;
	this->h = h;
	this->max_CC = 2;
	this->max_depth = 0;
	this->count = 0;
	this->debug = false;
	this->adj_l = new std::vector<int>[V];
	ways.emplace_back(std::vector<int>(V,0));
	ways.emplace_back(std::vector<int>(V,1));
}

Graph::~Graph() {}

int Graph::get_E() { return this->E; }

void Graph::set_debug(int debug) { this->debug = debug; }

int Graph::get_ways_size() { return ways.size(); }

void Graph::insert_edge(const int& v, const int& w) {
	adj_l[v].emplace_back(w);
	adj_l[w].emplace_back(v);
}

void Graph::remove_edge(const int& v, const int& w) {
	// https://stackoverflow.com/questions/3385229/c-erase-vector-element-by-value-rather-than-by-position
	// https://en.wikipedia.org/wiki/Erase%E2%80%93remove_idiom
	adj_l[v].erase(std::remove(adj_l[v].begin(), adj_l[v].end(), w), adj_l[v].end());
	adj_l[w].erase(std::remove(adj_l[w].begin(), adj_l[w].end(), v), adj_l[w].end());
}

void Graph::load(const char *filename) {
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
		edges.emplace_back(std::vector<int>{v,w});
	}
	fclose(file);

	E = edges.size();
	if (h < 3) {
		max_depth = h;
	} else {
		max_depth = E/2;
	}
}

void Graph::iterate_edges(const int cur, int depth) {
	if (depth > max_depth) return;

	for (int i = cur; i < edges.size(); ++i) {
		remove_edge(edges[i][0], edges[i][1]);
		iterate_edges(i+1, depth+1);

		if (depth >= h) { // minimum of h cuts to disconnect the graph
			CC();
			if (count == max_CC) { // found max_CC components
				add_if_new();
			}
		}

		insert_edge(edges[i][0], edges[i][1]);
	}
}

void Graph::CC() {
	std::fill(marked.begin(), marked.end(), false);
	//std::fill(id.begin(), id.end(), -1);
	count = 0;
	for (int v = 0; v < V; ++v) {
		if (!marked[v]) {
			if(++count > max_CC) return;
			DFS(v);
		}
	}
}

void Graph::DFS(const int v) {
	marked[v] = true;
	id[v] = count-1;
	for (const int& w : adj_l[v]) {
		if(!marked[w]) DFS(w);
	}
}

void Graph::add_if_new() {
	bool new_way = true;
	for (const auto& w : ways) {
		if(w == id) {
			new_way = false;
			break;
		}
	}

	if(new_way) {
		ways.emplace_back(id);

		std::for_each(id.begin(), id.end(), [](int &x){ x = !x; });
		ways.emplace_back(id);

		if (debug > 0) {
			printf(" [NEW] \n");
			print_CC();
		}
	}
}

void Graph::print_graph() {
	printf("\n Total of %d edges:\n", this->E);
	for (int v = 0; v < V; ++v) {
		printf(" %2d ->", v);
		std::cout << adj_l[v] << '\n';
	}
	printf("\n");
}

void Graph::print_CC() {
	printf(" v  ->");
	for(int v = 0; v < V; ++v) {
		printf(" %2d", v);
	}
	std::cout << "\n CC -> " << id << '\n';
}

void Graph::print_ways() {
	std::ofstream f;
	f.open("ways.log");
	std::cout << "-> Dumping ways (patterns) in 'ways.log'\n";
	for (const auto& w : ways) {
		f << w << '\n';
	}
	f.close();
}

enum {
	PROGNAME,
	N,
	H,
	FILENAME,
	NARGS
};

int main(int argc, char **argv) {
	double elapsed_secs;
	clock_t begin, end;
	if (argc != NARGS) {
		fprintf(stderr, "usage: %s n h file\n", argv[PROGNAME]);
		exit(EXIT_FAILURE);
	}
	int n = atoi(argv[N]), h = atoi(argv[H]);

	printf("-> Initializing graph\n");
	Graph G(n, h);
	G.set_debug(0);

	printf("-> Loading edges from %s\n", argv[3]);
	G.load(argv[3]);

	printf("-> Printing generated graph\n");
	G.print_graph();

	printf("-> Iterating\n");
	begin = std::clock();
	G.iterate_edges(0, 1);
	end = std::clock();
	elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << ' ' << elapsed_secs << "s\n";

	printf("\n-> %d ways of disconnecting G into 2 CC were found\n", G.get_ways_size());
	G.print_ways();

	return 0;
}
