#!/usr/env python

# http://docs.sympy.org/latest/modules/combinatorics/polyhedron.html
from sympy.combinatorics import Polyhedron
from urllib.request import urlopen
import re
import sys

def download_polyhedron(url):
    return urlopen(url).read().decode('utf-8')

#url = 'http://dmccooey.com/polyhedra/DualGeodesicIcosahedron1.txt'
def build_polyhedron(poly_str):
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
    poly_data = download_polyhedron(sys.argv[1])
    poly = build_polyhedron(poly_data)
    print_edges(poly)


