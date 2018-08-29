#!/usr/env python

import sys
from dmccooey import Poly
import numpy as np

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print(' usage:\n \t%s url' % sys.argv[0])
        exit(1)

    url = sys.argv[1]

    print("-> Creating object")
    P = Poly(url)
    P.build()

    print(
        "-> Printing to '../draw/vertices.dat', '../draw/edges.dat' and "
        "'../draw/faces.dat'"
    )
    np.savetxt('../draw/vertices.dat', P.vertices)
    np.savetxt('../draw/edges.dat', P.edges, fmt='%d')
    np.savetxt('../draw/faces.dat', P.faces, fmt='%d')
