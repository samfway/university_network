#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


from numpy import zeros, ones
from numpy.random import shuffle, seed
from scipy.sparse import csc_matrix


class ConfigurationModel:
    """ Class for generating networks using the configuration model.

        This implementation allows for both in and out degrees to be specfied.
        If you don't wish to make this distinction, simply pass the same degree
        sequence for both in-degree and out-degree. 

        The heart of the algorithm relies on numpy's shuffle command to permute
        expanded degree sequence arrays and scipy's csc_matrix format to efficiently
        create the adjacency matrix from these permuted lists.  Duplicate edges *are*
        countd appropriately by csc_matrix, so the resulting adjacency matrix will
        be weighted.  Convert to binary as needed.   

        FUNCTIONS 
        - generate_adjacency_matrix() : Returns a (sparse) adjacency matrix.

        - yield_edges() : Calls generate_adjacency_matrix(), then iterates over the
                        edges, returning 
    """


    def __init__(self, in_degree_seq, out_degree_seq, n=None, rnd_seed=None): 
        """ Prepare model for generating networks """ 
        if len(in_degree_seq) != len(out_degree_seq):
            raise ValueError("In-degree and out-degree sequences must "
                             "be of equal length!")
        if n is None:
            self.n = len(in_degree_seq)
        else:
            self.n = n

        seed(rnd_seed)
        self.in_degrees = in_degree_seq
        self.out_degrees = out_degree_seq

        # Prep in-stubs
        p = 0
        self.total_in = sum(in_degree_seq)
        self.in_stubs = zeros(self.total_in)
        for i, d in enumerate(in_degree_seq):
            self.in_stubs[p:p+d] = i
            p += d

        # Prep out-stubs
        p = 0
        self.total_out = sum(out_degree_seq)
        self.out_stubs = zeros(self.total_out)
        for i, d in enumerate(out_degree_seq):
            self.out_stubs[p:p+d] = i
            p +=d 

        self.total_edges = min(self.total_in, self.total_out)


    def generate_adjacency_matrix(self):
        """ Generate an adjacency matrix from the 
            expanded degree sequence arrays (in_stubs & out_stubs).
        """ 
        shuffle(self.in_stubs)
        shuffle(self.out_stubs)
        A = csc_matrix((ones(self.total_edges),
                       (self.in_stubs[:self.total_edges],
                        self.out_stubs[:self.total_edges])),
                        shape=(self.n, self.n))
        return A
        
    
    def yield_edges(self):
        """ Generates a random network, then yields (generator) the 
            edges one by one as a tuple:
                (row_index, column_index, edge_weight)
        """ 

        A = self.generate_adjacency_matrix()
        rows, cols = A.nonzero()
        for r,c in zip(rows, cols):
            yield(r, c, A[r,c])

