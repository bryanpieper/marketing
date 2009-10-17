#!/bin/env python2.6

""" 
Email list A/B splitter. Uses randomization to generate list samples.

Copyright (c) 2009 Bryan Pieper, http://www.thepiepers.net/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import os, sys

def list_ab_split(src_list_file, list_a_file=sys.stdout, list_b_file=sys.stdout, 
                  list_other_file=sys.stdout, sample_size=0.10):
    """ 
    A/B list generator.  Creates 3 lists from the given 'src_list'.  Each of the A/B
    samples are random selection from the src_list that will not exceed the given
    'sample_size' percentage.  Intended to keep the list intact.  Does not care
    about the list delimiter.

    @param src_list_file: the given source list file
    @param list_a_file: the output file for List A
    @param list_b_file: the output file for List B
    @param list_other_file: the output file for remainder list entries
    @param sample_size: the percentage (0 - .5) of the list sample size (the samples cannot exceed
        the size of the given list)
    """
    if sample_size >= 0.5 or sample_size < 0:
        raise ValueError, 'Sample size must be between 0 and 0.5'
    
    from types import ListType, TupleType
    full_list = None
        
    # create list copy and trim the return chars
    if type(src_list_file) in (ListType, TupleType):
        full_list = [fline.strip() for fline in src_list_file[:]]
    else:
        full_list = [fline.strip() for fline in src_list_file]
    
    import random
    random.seed(os.urandom(2048*10))
    random.shuffle(full_list)
    sample_len = sample_size * len(full_list)

    for i, line in enumerate(full_list):
        if i > sample_len:
            print >> list_other_file, line
            continue
        if i % 2:
            print >> list_a_file, line
        else:
            print >> list_b_file, line



if __name__ == '__main__':
    import time
    if len(sys.argv) > 1:
        list_file = open(sys.argv[1], 'r')
        list_name = os.path.splitext(list_file.name)
    
        list_a = open(''.join([list_name[0], '_a', list_name[1]]), 'w+')
        list_b = open(''.join([list_name[0], '_b', list_name[1]]), 'w+')
        list_other = open(''.join([list_name[0], '_other', list_name[1]]), 'w+')
        
        print 'Generating A/B Lists'
        start = time.time()
        list_ab_split(list_file, list_a, list_b, list_other)
        end = time.time()
        
        print ' List A:', list_a.name
        print ' List B:', list_b.name
        print ' The rest:', list_other.name
        print 'Completed in %0.2f seconds' % (end - start)
        
        list_a.close()
        list_b.close()
        list_other.close()
    else:
        raise ValueError, 'Please provide an input list file'
