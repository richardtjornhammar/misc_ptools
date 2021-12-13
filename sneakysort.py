import numpy as np
import typing
import time


def sneakysort(v:list,method='ordinal',get='order')->list :
    kind = {'average':'quicksort','ordinal':'mergesort'}[method]
    if get == 'order' :
        return ( np.sort(v,kind='mergesort') )
    if get == 'ranks':
        return ( np.argsort(v) )

def qsort ( v:list , left:int=None , right:int=None , comp = lambda a,b:a<=b ) -> list :
    # COMPARISON WITH NATIVE SORTED
    desc__ = """
   [ [1E5 ,   0.02673101 ,    1.22273183 ] ,
     [1E6 ,   0.45836091 ,   16.03984833 ] ,
     [1E7 ,   7.39028406 ,  164.56910157 ] ,
     [1E8 , 106.67638898 , 1862.81661701 ] ]
    """
    w = v.copy()
    import sys
    NREC = sys.getrecursionlimit()
    sys.setrecursionlimit( len(v) )
    recursive_qsort( w , left , right , comp )
    sys.setrecursionlimit(  NREC )
    return ( w )

def recursive_qsort ( v:list , left:int = None , right:int = None , comp = lambda a,b:a<=b ) -> None :
    i:int     = 0
    if left is None :
        left:int  = 0
    if right is None :
        right:int = len(v)-1
    if ( left >= right ) :
        return
    def swap ( w:list,i_:int,j_:int ) -> None :
        tmp_  = w[i_]
        w[i_] = w[j_]
        w[j_] = tmp_
    swap( v , left , int( (left+right)/2) )
    last = left
    for i in range(left+1,right+1) :
        if ( comp(v[i],v[left]) ) :
            last+=1
            swap(v,last,i)
    swap( v,left,last )
    recursive_qsort(v,left,last-1,comp)
    recursive_qsort(v,last+1,right,comp)

from scipy.stats import rankdata
if __name__ == '__main__' :
    N = 1E5
    a = np.round(np.random.rand(int(N)) * N/10)
    c = a.copy()
    print ( a )

    # a = [ 35., 99., 87., 59., 21., 29., 35., 21., 59., 36. ]

    T = []
    T .append( time.time() )
    sorted(a)
    T .append( time.time() )
    b = qsort ( a )
    T .append( time.time() )
    ra = sneakysort(c) #rankdata(c,'average')
    T .append( time.time() )
    print ( np.sum( b-sorted(a) ) )
    print ( np.diff(T) )
    print ( ra )
    """
   [ [1E5 ,   0.02673101 ,    1.22273183 ] ,
     [1E6 ,   0.45836091 ,   16.03984833 ] ,
     [1E7 ,   7.39028406 ,  164.56910157 ] ,
     [1E8 , 106.67638898 , 1862.81661701 ] ]
    """
