import math

def P(N,M=None,p=None) :
    if p is None :
        p = 1
    if M is None :
        M = N
    if (M%(N-1))==0 or ((M%p)==0 and p>=2) :
        return ( M,N-1,p )
    else :
       if (p-1)*(N+1)>=M*2:
           return ( '*',M,N-1,p )
       return ( P(N-1,M=M,p=p+1) )


def P0(N,M=None,p=None) :
    if p is None :
        p = 1
    if M is None :
        M = N
    if (M%(N-1))==0 or ((M%p)==0 and p>=2) :
        return ( N == 2 )
    else :
       return ( P0(N-1,M=M,p=p+1) )


def P1(N,M=None,p=None) :
    if p is None :
        p = 1
    if M is None :
        M = N
    if (M%(N-1))==0 or ((M%p)==0 and p>=2) :
        return ( N==2 )
    else :
       if math.log(p) > math.log(M)*0.5:
           return ( True )
       return ( P1(N-1,M=M,p=p+1) )


if __name__=='__main__':
    #
    # NO RECURSION DEPTH PROBLEM WITH P1(N)
    for i in range(100000):
        N = i+2
        print ( N , P1(N) )
    N = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
    print ( N,P1(N) )
