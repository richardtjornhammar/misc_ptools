def Fibonacci(n):
  if n-2>0:
    return ( Fibonacci(n-1)+Fibonacci(n-2) )
  if n-1>0:
    return ( Fibonacci(n-1) )
  if n>0:
    return ( n )

def F_truth(i):
    return ( Fibonacci(i)**2+Fibonacci(i+1)**2 == Fibonacci(2*i+1))


if __name__=='__main__':
    N_ = 11
    print ( [ Fibonacci(i) for i in range(1,N_) ] )
    print ( [ F_truth(i) for i in range(1,N_) ] )
