#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


class Struct:
    """ Create a Python object from a dictionary of key-values """ 
    def __init__(self, **entries): 
        self.__dict__.update(entries)


def custom_cast(x, cast_types=[int, float, str]):
    """ Attempt to cast x using the specified types in the order
        in which they appear.  """ 
    for cast_func in cast_types:
        try:
            return cast_func(x)
        except ValueError:
            pass
    raise BaseException('All casts failed!')


def add_weighted_edge(G, vertex_pair, weight=1.0):
    """ Wrapper to facilitate making weighted, directed
        networks.  If an edge exists between the vertex_pair,   
        the weight is incremented by the supplied value. 
        If the edge does not already exist, it is created 
        and initialized with the supplied weight value.
    """ 
    s, d = vertex_pair  # unpack
    if G.has_edge(s, d):
        G[s][d]['weight'] += weight
    else:
        G.add_edge(s,d, weight=weight)
