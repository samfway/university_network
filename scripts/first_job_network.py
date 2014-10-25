#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

from university_network.misc.util import add_weighted_edge
from university_network.parse.faculty_parser import parse_faculty_records
from university_network.parse.institution_parser import parse_institution_records
import networkx as nx
import matplotlib.pyplot as plt


def load(institution_fp, faculty_fp):
    """ Create weighted, directed graph where edges (A->B) are the number 
        of PhDs from school A who got their first non-postdoc job at B. 
    """ 
    G = nx.DiGraph()
    institutions = parse_institution_records(institution_fp)
    add_edges(G, faculty_fp)
    return G


def add_edges(G, faculty_fp):
    """  Load a network of faculty placement where...
         +  NODES are institutions.
         +  An EDGE between institution A and B indicates that
            a PhD from A got their first non-postdoc position at B. 
         +  The weight of the edges is simply the number of individuals
            with the same career path (PhD from A, first job at B)
    """ 
    for rec in parse_faculty_records(faculty_fp):
        phd_loc, phd_year = rec.phd()
        job_loc, job_year = rec.first_job()

        if phd_loc is not None and phd_loc != '.' \
           and job_loc is not None and job_loc != '.':
            add_weighted_edge(G, (phd_loc, job_loc))
        

if __name__ == '__main__':
    inst_fp = open('/Users/samway/Documents/Work/ClausetLab/faculty_network/data'
                   '/replicationData_all/ComputerScience_vertexlist.txt', 'rU')
    facu_fp = open('/Users/samway/Documents/Work/ClausetLab/faculty_network/data/'
                   'allFaculty_BS_CS_HS-shortform_txt/allFaculty_CS_n5762_19-Apr-'
                   '2012-shortform.txt', 'rU')
    G = load(inst_fp, facu_fp)
    
    grab = ['Stanford University', 'UC Berkeley', 'MIT', 'California Institute of Technology',
            'Harvard University', 'Cornell University', 'Carnegie Mellon University', 
            'Princeton University', 'Yale University', 'University of Washington', 
            'University of Illinois, Urbana Champaign', 'University of Wisconsin, Madison']
    H = G.subgraph(grab)
    pos = nx.graphviz_layout(H, prog='dot')
    nx.draw(H,pos,edgelist=H.edges(),node_size=500,with_labels=True)
    plt.show()

    # Write out GML file for visualizing.
    #nx.write_gml(G,"test.gml")
