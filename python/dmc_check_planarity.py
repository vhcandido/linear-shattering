#!/usr/env python

import sys
from dmccooey import Poly

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print(' usage:\n \t%s url file' % sys.argv[0])
        exit(1)

    url = sys.argv[1]
    filename = sys.argv[2]

    print("-> Creating object")
    P = Poly(url)

    print("-> Preparing to check")
    P.build()

    print("-> Querying from file")
    P.query_from_file(filename)
