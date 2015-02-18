#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


from numpy import zeros, ones, array, exp, hstack
from numpy.random import shuffle, seed, choice, random
from scipy.sparse import csc_matrix

def sigmoid(x):
    return 1 / (1 + exp(-x))

class PickSigmoidModel:
    """ Class for generating networks using the configuration model.


        - yield_edges() : Calls generate_adjacency_matrix(), then iterates over the
                        edges, returning 
    """


    def __init__(self, 
                 in_degree_seq, 
                 out_degree_seq, 
                 ranking_seq, 
                 n=None, 
                 rnd_seed=None,
                 alpha=10,
                 self_consideration=1): 
        """ Prepare model for generating networks 

            Crucial info:
            - Rankings are shifted and scaled into the range (0, 1) where 1 is the *BEST* ranking!
            - self.in_stubs is a vector denoting the in-degrees of each node. If v has in-degree ==  k_v,
              v appears in the in_stubs vector k_v times. 
            - self.out_stubs works the same as in_stubs except for out-degree.
            
        """ 
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
        self.self_consideration = self_consideration

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

        remaining_in.sort(reverse=True)  # Candidates sorted by rank
        remaining_out.sort(reverse=True)  # Candidates sorted by rank

        for i in xrange(self.total_edges):

            # Select which job to fill
            p_in = array([r_in[0] for r_in in remaining_in])  # ranks
            c_in = array([r_in[1] for r_in in remaining_in])  # indices
            p_in /= p_in.sum()
            selected_in = choice(xrange(len(p_in)), p=p_in)
            in_rank = remaining_in[selected_in][0]
            in_ind = remaining_in[selected_in][1]
            
            # Select candidate to fill the job
            p_out = array([sigmoid(self.alpha*(out_rank-in_rank)) if out_ind != in_ind else
                           sigmoid(self.alpha*(out_rank-in_rank)) + self.self_consideration
                           for out_rank, out_ind in remaining_out])
            p_out /= p_out.sum()
            selected_out = choice(xrange(len(p_out)), p=p_out)

            # Record hire and remove job/candidate from pool.
            destinations[i] = remaining_in[selected_in][1]  # hired by
            sources[i] = remaining_out[selected_out][1]  # hired from 
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

