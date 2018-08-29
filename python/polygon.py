import numpy as np
import itertools as itt
from utils import mirror_invert, combine_hyperplanes


def zip_circular(x):
    return zip(x, np.append(x[1:], x[0]))


def polygon_vertices(n, r=10):
    angle = 2 * np.pi / n
    x = [r * np.cos(np.pi / 2 - angle * i) for i in range(n)]
    y = [r * np.sin(np.pi / 2 - angle * i) for i in range(n)]
    return np.array(x), np.array(y)


def polygon_edges(x, y):
    def mid(v):
        return [(i + j) / 2 for i, j in zip_circular(v)]
    return mid(x), mid(y)


def coefficients(x, y):
    # https://math.stackexchange.com/questions/637922/how-can-i-find-coefficients-a-b-c-given-two-points
    a = y[0] - y[1]
    b = -(x[0] - x[1])
    c = x[0] * y[1] - x[1] * y[0]
    return a, b, c


# Possible combinations obtainable with 1 hyperplane in i=1 and i=0
def ways_i1p1(n):
    ways = [np.array([0] * i + [1] * (n - i)) for i in range(n)]
    np.array(ways, dtype=int)
    return ways


# Possible combinations obtainable with 1 hyperplane in i=2
def ways_i2p1(n, x, y, m_x, m_y, edge_connections):
    ways = []
    for i_p0, i_p1 in edge_connections:
        x_ = [m_x[i_p0], m_x[i_p1]]  # x0 and x1 to connect
        y_ = [m_y[i_p0], m_y[i_p1]]  # y0 and y1 to connect
        a, b, c = coefficients(x_, y_)
        classes = (a * x + b * y + c) > 0
        ways.append(classes)
    ways = np.array(ways, dtype=int)
    return ways


def ways(n, p=1, h=2, r=10):
    edges = n
    x, y = polygon_vertices(n, r)  # polygon vertices
    m_x, m_y = polygon_edges(x, y)  # edges middle points

    # Combine all possible indexes taken 2 by 2
    # '-> same as combn(1:n, 2) in R
    edge_connections = itt.combinations(range(edges), 2)

    w_i1p1 = ways_i1p1(n)  # p=1, i=1 and i=0
    w_i2p1 = ways_i2p1(n, x, y, m_x, m_y, edge_connections)  # p=1, i=1
    w_p1 = np.concatenate((w_i1p1, w_i2p1), axis=0)
    w_p1 = mirror_invert(w_p1)

    # combine voting patterns for 1 hyperplane p times
    w = combine_hyperplanes(w_p1, p)
    return w
