#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Unit tests for faculty network parsing. """

from university_network.parse.faculty_parser import parse_faculty_records

from StringIO import StringIO
from unittest import TestCase, main

def get_test_records():
    return StringIO(
"""
>>> record 1\n
# facultyName : Joe Shmoe\n
# email       : js@asu.edu\n
# sex         : M\n
# department  : Information and Computer Science\n
# place       : Arizona State University\n
# current     : Associate Professor\n
# [Education]\n
# degree      : BS\n
# place       : Stanford University\n
# field       : Computer Science\n
# years       : ????-1994\n
# [Education]\n
# degree      : PhD\n
# place       : Stanford University\n
# field       : Information Technology\n
# years       : ????-2000\n
# [Faculty]\n
# rank        : PostDoc\n
# place       : Arizona State University\n
# years       : 2000-2000\n
# [Faculty]\n
# rank        : Assistant Professor\n
# place       : MIT\n
# years       : 2000-2005\n
# recordDate  : 9/29/2011\n
\n
>>> record 2\n
# facultyName : Bob Roberts\n
# email       : br@cse.tamu.edu\n
# sex         : M\n
# department  : Computer Science\n
# place       : Texas A&M\n
# current     : Emeritus\n
# [Education]\n
# degree      : PhD\n
# place       : University of New Mexico\n
# field       : Computer and Information Sciences\n
# years       : ????-????\n
# [Faculty]\n
# rank        : Full Professor\n
# place       : Texas A&M\n
# years       : 1996-2008\n
# [Faculty]\n
# rank        : Emeritus\n
# place       : Texas A&M\n
# years       : 2008-2011\n
# recordDate  : 10/6/2011\n""")


class logLikelihoodTests(TestCase):
    """ Test parsing of log-likelihood calculation. """
    def setUp(self):
       pass 


    def test_parse(self):
        X = get_test_records()
        records = parse_faculty_records(X)

        first_record = records.next()
        self.assertEqual(first_record.facultyName, 'Joe Shmoe')
        self.assertEqual(first_record.email, 'js@asu.edu')
        self.assertEqual(first_record.sex, 'M')
        self.assertEqual(first_record.department, 'Information and Computer Science')
        self.assertEqual(first_record.place, 'Arizona State University')
        self.assertEqual(first_record.current, 'Associate Professor')
        self.assertEqual(first_record.education[0].degree, 'BS')
        self.assertEqual(first_record.education[0].place, 'Stanford University')
        self.assertEqual(first_record.education[0].field, 'Computer Science')
        self.assertEqual(first_record.education[0].years, '????-1994')
        self.assertEqual(first_record.education[0].start_year, None)
        self.assertEqual(first_record.education[0].end_year, 1994)
        self.assertEqual(len(first_record.education), 2)
        self.assertEqual(len(first_record.faculty), 2)
        self.assertEqual(first_record.faculty[1].rank, 'Assistant Professor')
        self.assertEqual(first_record.faculty[1].place, 'MIT')
        self.assertEqual(first_record.faculty[1].years, '2000-2005')
        self.assertEqual(first_record.faculty[1].start_year, 2000) 
        self.assertEqual(first_record.faculty[1].end_year, 2005) 
        self.assertEqual(first_record.recordDate, '9/29/2011')

        second_record = records.next()
        self.assertEqual(len(second_record.education), 1) 
        self.assertEqual(len(second_record.faculty), 2) 
        self.assertEqual(second_record.education[0].place, 'University of New Mexico') 
        self.assertEqual(second_record.faculty[1].rank, 'Emeritus') 


if __name__ == '__main__':
    main()
