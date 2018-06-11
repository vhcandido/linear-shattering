import sys
import re
import numpy as np
from urllib.request import urlopen
import create_graph_dmccooey as dmc

def read_variables(text):
    print(' Reading variables... ', end='')
    re_float = '-?(?:[0-9]+(?:\.[0-9]+)?)'
    regex = '^(\w+).*?(%s)' % (re_float)
    variables = {k:np.float128(v) for line in text.split('\n') for k,v in re.findall(regex, line)}
    print('Done')
    return variables

def read_vertices(text, variables=None):
    print(' Reading vertices... ', end='')
    re_float = '-?(?:[0-9]+(?:\.[0-9]+)?)'
    re_variable = '-?(?:\w+)'
    re_float_variable = '(?:(?:%s)|(?:%s))' % (re_float, re_variable)
    regex = '\s*?(%s)\s*?' % (re_float_variable)
    #regex = '^(\w+).*?\(%s,%s,%s\)' % (regex, regex, regex)
    is_neg = np.vectorize(lambda x: (True,x[1:]) if x.startswith('-') else (False,x))
    vertices = []
    for line in text.split('\n'):
        match = np.array(re.findall(regex, line)[1:])
        if variables:
            coord = np.full(match.shape, np.nan, dtype=np.float128)
            match_isneg, match = is_neg(match)
            for k,v in variables.items():
                if k in match:
                    coord[np.where(match == k)] = v
            i = np.where(np.isnan(coord))
            coord[i] = match[i].astype(np.float128)
            coord[np.where(match_isneg)] *= -1
            vertices.append(coord)
        else:
            vertices.append(match)

    print('Done')
    return np.array(vertices).astype(np.float128)

def adj_list(P):
    adj_l = [[]] * len(P.vertices)
    for i,j in P.edges:
        adj_l[i].append(j)
        adj_l[j].append(i)
    return adj_l

class Poly(object):
    def __init__(self, url):
        self.vertices = []
        self.adj_l = []
        self.edges = []
        self.mid = []
        self.url = url

        # Download text from url
        self.poly_txt = dmc.download_polyhedron(url)

        # Build SymPy Polyhedron using the given faces
        self.P = dmc.build_polyhedron(self.poly_txt)

    def prepare_to_check(self):
        # Divide downloaded text and read the variables/vertices block
        blocks = self.poly_txt.split('\n\n')
        variables = read_variables(blocks[1]) if len(blocks) > 3 else None
        self.vertices = read_vertices(blocks[-2], variables)

        # Build adjacency list of edges (from SymPy's Polyhedron)
        self.adj_l = adj_list(self.P)

        # Build array of edges and compute midpoints for each one of them
        self.edges = np.array([e for e in self.P.edges]).astype(int)
        self.mid = (self.vertices[self.edges[:,0]] + self.vertices[self.edges[:,1]]) / 2

    def check_coplanarity(self, query):
        # Compute the difference vectors between the queried edges and the 1st midpoint
        query_mid = self.mid[np.array(query)]
        vectors = query_mid - query_mid[0]

        # Cross product between the 1st and 2nd difference vectors (pos. 0 is (0,0))
        # '-> results in the orthogonal vector in relation to the plane
        v = np.cross(vectors[1], vectors[2])

        # Dot product between the ortog. vector and every vector
        # '-> results in 0 if vector is in the plane
        dot = np.dot(vectors, v)
        return np.allclose(dot, 0)

    def query_from_file(self, filename):
        count = 0
        ways = np.loadtxt(filename).astype(int)
        for way in ways:
            removed_edges = [way[v] != way[w] for v,w in self.edges]
            query = np.where(removed_edges)[0]
            if query.size == 0: continue
            if not self.check_coplanarity(query):
                print(' ', way, ' -> not linear')
                count += 1
            else:
                print(' ', way, ' -> linear')
        print('\n %d linear, %d not linear' % (len(ways) - count, count))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        url = sys.argv[1]
        filename = sys.argv[2]

        print("-> Creating object")
        P = Poly(url)

        print("-> Preparing to check")
        P.prepare_to_check()

        print("-> Querying from file")
        P.query_from_file(filename)
    else:
        print(' usage:\n \t%s url file' % sys.argv[0])
        exit(1)
