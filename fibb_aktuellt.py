def Fibbonacci(n):
  if n-2>0:
    return ( Fibbonacci(n-1)+Fibbonacci(n-2) )
  if n-1>0:
    return ( Fibbonacci(n-1) )
  if n>0:
    return ( n )

def F_truth(i):
    return ( Fibbonacci(i)**2+Fibbonacci(i+1)**2 == Fibbonacci(2*i+1))
