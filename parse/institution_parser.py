#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

"""
Parsing of university record files.  
"""


from university_network.misc.util import Struct, custom_cast


def parse_institution_records(fp):
    """ Parse a university record file.
        Inputs:
          + fp - an *open* file pointer containing 
                 university/institution records.  
        
        Yields:
          + A dictionary linking an institution name 
            to the attributes stored in the file.

        Example:  
            >>> institutions = parse_institution_records(X)
            >>> print institutions['Carnegie Mellon University'].USN2010
                1
            >>> print institutions['Harvard University'].pi
                6.12
            >>> print institutions['Yale University'].Region
                'Northeast'

        NOTE:  Attributes are just the column names in the 
               institution records file.  
    """
    institutions = {} 
    detect_header = True
    for line in fp:
        line = line.strip()
        if not line:  continue  # skip empty lines

        if detect_header:
            detect_header = False
            if not line.startswith('# '):
                raise ValueError('File does not appear to be a valid '
                                 'institution records file!') 
            line = line[2:]  # Remove leading "# "
            fields = line.split('\t')
            if 'institution' not in fields:
                raise ValueError('Records file missing `institution` field!')
            num_fields = len(fields)
            institution_field_ind = fields.index('institution')
            info_fields = [f for i,f in enumerate(fields) if i != institution_field_ind]
            info_fields_ind = [i for i in xrange(num_fields) if i != institution_field_ind]
        else:
            fields = line.strip().split('\t')
            if len(fields) != num_fields:
                raise ValueError('Missing/extra fields in line: %s' % line)
            info_values = [custom_cast(fields[i]) for i in info_fields_ind]
            institution = fields[institution_field_ind]
            institution_record = dict(zip(info_fields, info_values))
            institutions[institution] = Struct(**institution_record)

    return institutions 

