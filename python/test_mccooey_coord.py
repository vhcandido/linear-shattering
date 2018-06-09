import sys
import re
import numpy as np
from urllib.request import urlopen
import create_graph_dmccooey as dmc

def read_variables(text):
    print('Reading variables... ', end='')
    re_float = '-?(?:[0-9]+(?:\.[0-9]+)?)'
    regex = '^(\w+).*?(%s)' % (re_float)
    variables = {k:np.float128(v) for line in text.split('\n') for k,v in re.findall(regex, line)}
    print('Done')
    return variables

def read_vertices(text, variables=None):
    print('Reading vertices... ', end='')
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

def check_coplanarity(vertices, poly, query):
    edges = np.array([e for e in poly.edges]).astype(int)
    edges = edges[np.array(query).astype(int)]
    middle = (vertices[edges[:,0]] + vertices[edges[:,1]]) / 2
    vectors = middle - middle[0]
    v = np.cross(vectors[1], vectors[2])
    dot = np.dot(vectors, v)
    print(dot)
    return np.allclose(dot, 0)

def main(url, query=None):
    poly_data = dmc.download_polyhedron(url)
    poly = dmc.build_polyhedron(poly_data)
    blocks = poly_data.split('\n\n')
    if len(blocks) > 3:
        variables = read_variables(blocks[1])
        vertices = read_vertices(blocks[2], variables)
    else:
        vertices = read_vertices(blocks[1])

    if not query:
        print(vertices)
        print('\n'.join('%d: %s' % (i,str(e)) for i,e in enumerate(poly.edges)))
    else:
        if check_coplanarity(vertices, poly, query):
            print("Edges' middle points are coplanar")
        else:
            print("Edges' middle points are NOT coplanar")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        main(url)
    elif len(sys.argv) == 3:
        url = sys.argv[1]
        query = sys.argv[2].split(',')
        main(url, query)
    else:
        print(' usage:\n \t%s url [query]' % sys.argv[0])
        exit(1)
