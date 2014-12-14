#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


from numpy import zeros, ones, array
from numpy.random import shuffle, seed, choice
from scipy.sparse import csc_matrix


class BestRemainingModel:
    """ Class for generating networks using the configuration model.


        - yield_edges() : Calls generate_adjacency_matrix(), then iterates over the
                        edges, returning 
    """


    def __init__(self, in_degree_seq, out_degree_seq, ranking_seq, n=None, rnd_seed=None, alpha=0.001): 
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
        self.alpha = alpha

        # Preprocess ranking
        self.raw_ranking = ranking_seq
        ranking = array(ranking_seq)
        ranking -= ranking.min()
        ranking /= ranking.max()
        ranking = 1.0 - ranking # 1.0 is now the highest, 0. the lowest
        self.ranking = ranking

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
        """ Generate an adjacency matrix
        """ 
        sources = zeros(self.total_edges)
        destinations = zeros(self.total_edges)

        remaining_in = [(self.ranking[x], x) for x in self.in_stubs]
        remaining_out = [(self.ranking[x], x) for x in self.out_stubs]

        for i in xrange(self.total_edges):

            p_in = array([r[0]+self.alpha for r in remaining_in])
            p_out = array([r[0]+self.alpha for r in remaining_out])
            p_in /= p_in.sum()
            p_out /= p_out.sum()

            selected_in = choice(len(remaining_in), p=p_in)
            selected_out = choice(len(remaining_out), p=p_out)

            sources[i] = remaining_out[selected_out][1]  # hired from 
            destinations[i] = remaining_in[selected_in][1]  # hired by

            del remaining_in[selected_in]
            del remaining_out[selected_out]

        A = csc_matrix((ones(self.total_edges),
                       (sources,
                        destinations)),
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

