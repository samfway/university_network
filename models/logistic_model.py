#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


from numpy import array, exp, mean, delete, inf, dot
from numpy.random import randn, choice
from university_network.misc.scoring import sse_rank_diff


def sigmoid(x):
    return 1. / (1. + exp(-x))


class LogisticModelSimulator:
    def __init__(self, cand_pools, job_pools, school_info, ranking='pi',
                 features=[None, 'pi'], weights=[0,1.0], iters=10, reg=0.):
        self.cand_pools = cand_pools
        self.job_pools = job_pools
        self.school_info = school_info
        self.ranking = ranking
        self.features = features
        self.weights = weights
        self.model = LogisticModel()
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


class LogisticModel:

    def __init__(self):
        pass

    def simulate_hiring(self, candidates, positions, school_info, ranking='pi',
                        features=[None, 'pi'], weights=[0, 1.0]):
        """ Simulate faculty hiring under the sigmoid (logistic regression) model.
            
            Algorithm:
            [ FILL THIS OUT ]

            Returns a list of tuples:
            [(candidate, position), (candidate, position), ... ] 

            Inputs:
            - 'candidates' is a list of faculty profiles. 
            - 'positions' is a list of school names.
            - 'school_info' is a dict indexed by school name, providing
              information like rank, region, etc. 

            As an assumption, I will say that any unranked school is effectively
            tied for last place. A small amount of noise is added to their ranking
            to serve as a tie-breaker. Haven't heard of that school? We'll assume
            the hiring committee hasn't either, and you get no bonus points for 
            prestige.
        """ 
        if len(features) != len(weights):
            raise ValueError('Feature/weight vectors must be of equal length.')
        if features[0] is not None:
            raise ValueError('First feature must be None (offset term)')
        weights = array(weights)

        rankings = array([school_info[s][ranking] for s in school_info])
        rankings.sort()
        worst_ranking = rankings[-1]
        best_ranking = rankings[0]
        delta = mean(rankings[1:] - rankings[0:-1])
        scale = lambda x: 1. - (x-best_ranking)/(worst_ranking-best_ranking+delta)
        # Delta ensures all schools have a positive rank
        
        jobs = positions[:]
        job_ranks = []
        for j in jobs:
            if j in school_info:
                job_ranks.append(scale(school_info[j][ranking]))
            else:
                job_ranks.append(scale(worst_ranking))
        job_ranks = array(job_ranks)

        candidate_pool = candidates[:]
        candidate_ranks = []
        for f in candidates:
            place, year = f.phd()
            if place in school_info:
                candidate_ranks.append(scale(school_info[place][ranking]))
            else:
                candidate_ranks.append(scale(worst_ranking))
        candidate_ranks = array(candidate_ranks)

        hires = [] 

        while jobs:
            # Select job
            job_p = job_ranks.copy()
            job_p /= job_p.sum()
            job_ind = choice(xrange(len(job_p)), p=job_p)
            job_rank = job_ranks[job_ind]

            # Select candidate
            cand_p = array([sigmoid(sum(weights * array([1, candidate_rank-job_rank])))
                            for candidate_rank in candidate_ranks])
            cand_p /= cand_p.sum()
            cand_ind = choice(xrange(len(cand_p)), p=cand_p)

            # Save then remove from lists
            hires.append((candidate_pool[cand_ind], jobs[job_ind]))

            del candidate_pool[cand_ind]
            del jobs[job_ind]
            candidate_ranks = delete(candidate_ranks, cand_ind)
            job_ranks = delete(job_ranks, job_ind)

        return hires

