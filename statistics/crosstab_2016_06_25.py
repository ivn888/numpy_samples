# -*- coding: UTF-8 -*-
"""
:Script:   crosstab.py
:Author:   Dan.Patterson@carleton.ca
:Modified: 2016-06-25
:Purpose:
:
:Notes:
:
:References
: http://stackoverflow.com/questions/38030054/
:      create-adjacency-matrix-in-python-for-large-dataset
: np.unique
: in the newer version, they use flags to get the sums
: 
: array([['a', 'a', 'a', 'b', 'b', 'c', 'c'],
:         ['A', 'B', 'B', 'A', 'B', 'C', 'B']]
: adjacency matrix   diagonal, sum of A,B,C's
:    A    B    C         a  b  c    A  B  C
: A  2    2    0      AB 1  1  0  A    2  0  BB is ignored?
: B  2    4    1      BA 1  1  0  B 2     1 
: C  0    1    1      BC 0  0  1  C 0  1    border links by group 
:                     CB 0  0  1            ignored?
: from scipy                       Diagonal [ 2,4,1]
: incidence = scipy.sparse.coo_matrix((np.ones_like(i), (i,j)))
: adjecency = incidence.T * incidence
"""
import sys
import numpy as np
from textwrap import dedent
np.set_printoptions(edgeitems=3, linewidth=80, precision=2,
                    suppress=True, threshold=50,
                    formatter={'float': '{: 0.3f}'.format})
from textwrap import dedent
script = sys.argv[0]


def crosstab(a, verbose=False):
    """Crosstabulate 2D data array with shape(N,2), using np.unique to do the work.
    :scipy.sparse has similar functionality and will be faster for large arrays.
    :
    :Requires:  A 2D array of data with shape(N,2) representing two variables
    :--------
    :
    :Returns:   An row*col array of the counts of the crosstabuation, where rows
    :--------   represent the 1st column and cols the 2nd column of input data.
    : data.T   transposed data array
    : array([['a', 'a', 'a', 'b', 'b', 'c', 'c'],
    :        ['A', 'B', 'B', 'A', 'B', 'C', 'B']],
    :        dtype='<U4')
    """
    if (a.ndim!=2) or (a.shape[-1] != 2):
        print("2D array with shape(n,2) is required...")
        return a
    u, u_inv = np.unique(a[:, 0], return_inverse=True)
    v, v_inv = np.unique(a[:, 1], return_inverse=True)
    rows = len(u)
    cols = len(v)
    ui_vi = [ pair for pair in zip(u_inv,v_inv)]
    z = np.zeros((rows, cols),dtype='int')
    for i in ui_vi:
        z[i] += 1
    if verbose:
        frmt = """
        :Array ... shape {} ndim {}
        {}\n
        : ---- column 0 ----
        :  unique vals  u : {}
        :  inv. idx, u_inv: {}
        : ---- column 1 ----
        :  unique vals  v : {}
        :  inv. idx, v_inv: {}\n
        :Crosstabulation...
        : u_inv vs v_inv 
        {}
        """
        args = [a.shape, a.ndim, a, u, u_inv, v, v_inv, z]
        print(dedent(frmt).format(*args))
    return z, u_inv, v_inv

#print(adjecency.todense())
if __name__=="__main__":
    """run crosstabulation with data   """
    data = np.array([['a', 'a', 'a', 'b', 'b', 'c', 'c'],
                     ['A', 'B', 'B', 'A', 'B', 'C', 'B']])
    a = data.T
    z, u_inv, v_inv = crosstab(a, verbose=True)
    d = np.eye(3,3,dtype='int') * [2,4,1]
