import pandas as pd
import numpy as np
import itertools

def SubArraysOf(Array,Array_=None):
    if Array_ == None :
        Array_ = Array[:-1]
    if Array == []:
        if Array_ == []:
            return([])
        return( SubArraysOf(Array_,Array_[:-1]) )
    return([Array]+SubArraysOf(Array[1:],Array_))

def grouper(inputs, n, fillvalue=None):
    # nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # list(better_grouper(nums, 4))
    iters = [iter(inputs)] * n
    return it.zip_longest(*iters, fillvalue=fillvalue)

def grouper(inputs, n):
    iters = [iter(inputs)] * n
    return zip(*iters)

if __name__ == '__main__' :
    info = """
       CREATES GROUP DEFINITIONS FROM ALL
       SUBSET PERMUTATIONS OF A NUMBER OF ANALYTES
    """
    filename = './7analytes.nfo'
    AnalyteArray_ = []
    with open( filename ) as input :
        for line in input :
            line_ = line.replace('\n','')
            if len(line_)>0 :
                AnalyteArray_.append( line_ )
    permutation_array = list(itertools.permutations(AnalyteArray_))
    SubArrays = SubArraysOf( AnalyteArray_ )
    I = 0
    for AnalyteArray in SubArrays:
        for sa in SubArrays :
            I += 1
            print ( 'S-ARR'+str(I) ,' \t' + 'N' + str(len(sa)) + '\t' + '\t'.join(sa) )
