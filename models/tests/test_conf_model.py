#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Unit tests for faculty network parsing. """

from university_network.models.configuration_models import ConfigurationModel
from unittest import TestCase, main


class cm_tests(TestCase):
    """ Test configuration model. """
    def setUp(self):
       pass 

    def test_cm(self):
        cm = ConfigurationModel([3, 1], [2, 5])
        A = cm.generate_adjacency_matrix()
        self.assertEqual(A.sum(), 4.0)  # 4 incoming edges, seven out

if __name__ == '__main__':
    main()
