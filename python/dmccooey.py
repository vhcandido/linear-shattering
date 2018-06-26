from sympy.combinatorics import Polyhedron
from urllib.request import urlopen
import numpy as np
import re

class Poly(object):
    def __init__(self, url):
        self.url = url.replace('.html', '.txt') # I tend to forget this
        self.poly_txt = ''
        self.edges = None
        self.vertices = None
        self.mid = None
        self.P = None

    def download_file(self):
        # Download text from url
        self.poly_txt = urlopen(self.url).read().decode('utf-8')

    def parse_file(self):
        # Build a Polyhedron (sympy) object via faces
        self.P = self.build_Polyhedron()

        # Divide downloaded text and read the variables/vertices block
        blocks = self.poly_txt.split('\n\n')
        variables = self.read_variables(blocks[1]) if len(blocks) > 3 else None
        self.vertices = self.read_vertices(blocks[-2], variables)

        # Build array of edges and compute midpoints for each one of them
        self.edges = np.array([e for e in self.P.edges]).astype(int)
        self.mid = (self.vertices[self.edges[:,0]] + self.vertices[self.edges[:,1]]) / 2

    def build(self):
        self.download_file()
        self.parse_file()

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

    def build_Polyhedron(self):
        """Build a SymPy Polyhedron from McCooey's website

        Returns
        sympy.combinatorics.polyhedron.Polyhedron
            Polyhedron object built using the faces in self.poly_txt
        """
        # Create list of faces that will be passed to Polyhedron's constructor
        faces = []
        for line in re.split('Faces:.*?\n', self.poly_txt)[1].split('\n'):
            if line:
                face = [int(i) for i in re.findall('(\d+)', line)]
                faces.append(face)

        # Count how many vertices are defined
        v = len(re.findall('V', self.poly_txt))

        return Polyhedron([*range(v)], faces)

    def read_variables(self, text):
        """Read variables' values (following McCooey's website format)

        Parameters
        ----------
        text: string
            Text containing variable definitions

        Returns
        -------
        dict
            Dictionary mapping each variable to its value
        """
        re_float = '-?(?:[0-9]+(?:\.[0-9]+)?)'
        regex = '^(\w+).*?(%s)' % (re_float)
        variables = {k:np.float128(v) for line in text.split('\n') for k,v in re.findall(regex, line)}

        return variables

    def read_vertices(self, text, variables=None):
        """Read vertices' coordinates (following McCooey's website format)

        Parameters
        ----------
        text: string
            Text containing vertices coordinates
        variables: dict
            Dictionary mapping variables' names to their respective values

        Returns
        -------
        numpy.ndarray
            Matrix of coordinates
        """
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

        return np.array(vertices).astype(np.float128)

    #def adjacency_list(self):
    #    """Build adjacency list

    #    Returns
    #    -------
    #    list
    #        List with lists of adjacent vertices
    #    """
    #    adj_l = [[]] * len(self.vertices)
    #    for i,j in P.edges:
    #        adj_l[i].append(j)
    #        adj_l[j].append(i)
    #   self.adj_l = adj_l
