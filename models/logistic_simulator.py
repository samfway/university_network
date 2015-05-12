#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


from numpy import array, exp, mean, delete, inf, dot
from numpy.random import randn, choice
from university_network.models.logistic_model import LogisticModel
from university_network.misc.scoring import sse_rank_diff


class LogisticModelSimulator:
    def __init__(self, cand_pools, job_pools, school_info, model=LogisticModel, ranking='pi',
                 features=[None, 'pi'], weights=[0,1.0], iters=10, reg=0.):
        self.cand_pools = cand_pools
        self.job_pools = job_pools
        self.school_info = school_info
        self.ranking = ranking
        self.features = features
        self.weights = weights
        self.model = model()
        self.iterations = iters 
        self.num_pools = len(cand_pools)
        self.regularization = reg

        if len(cand_pools) != len(job_pools):
            raise ValueError("Job/Candidate pools must be of equal length!")

        self.worst_rank = 0
        for s in school_info:
            if ranking in school_info[s] and school_info[s][ranking] > self.worst_rank:
                self.worst_rank = school_info[s][ranking]


    def simulate(self, weights):
        total_err = 0.0

        # L2 Regularization Penalty
        w = array(weights[1:])
        l2_penalty = dot(w,w) * self.regularization        

        for t in xrange(self.iterations):
            for i in xrange(self.num_pools):
                hires = self.model.simulate_hiring(self.cand_pools[i],
                                                   self.job_pools[i],
                                                   self.school_info,
                                                   self.ranking,
                                                   self.features,
                                                   weights)
                total_err += sse_rank_diff(hires, self.school_info, self.worst_rank)
                total_err += l2_penalty
        return total_err

