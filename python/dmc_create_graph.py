#!/usr/env python

import sys
from dmccooey import Poly

def print_edges(poly):
    for e in poly.edges:
        print('%4d %4d' % (e[0], e[1]))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(' usage:\n \t%s url' % sys.argv[0])
        exit(1)

    url = sys.argv[1]

    P = Poly(url)
    P.build()
    print_edges(P)
