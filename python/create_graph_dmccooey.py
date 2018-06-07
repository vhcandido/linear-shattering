#!/usr/env python

from sympy.combinatorics import Polyhedron
from urllib.request import urlopen
import re
import sys

#url = 'http://dmccooey.com/polyhedra/DualGeodesicIcosahedron1.txt'
def read_polyhedron(url):
    poly_str = urlopen(url).read().decode('utf-8')
    reading_faces = False
    faces = []
    for line in poly_str.split('\n'):
        if line and reading_faces:
            faces.append([int(i) for i in re.findall('(\d+)', line)])
        else:
            cur_vertice = re.findall('V(\d+)', line)
            if cur_vertice:
                vertice_count = int(cur_vertice[0]) + 1
            reading_faces = 'Faces:' in line
    return Polyhedron(list(range(vertice_count)), faces)

def print_edges(poly):
    for e in poly.edges:
        print('%4d %4d' % (e[0], e[1]))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(' usage:\n \t%s url' % sys.argv[0])
        exit(1)
    poly = read_polyhedron(sys.argv[1])
    print_edges(poly)


