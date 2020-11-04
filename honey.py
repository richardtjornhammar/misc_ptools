import pandas as pd
import numpy as np
bTriang = lambda n,m : True
bSquare = lambda n,m : (n+m)%2
bHoney  = lambda n,m : (n+m)%3
bTest   = lambda n,m : (n*m)%4
def generate_plaque(N,bFun=bHoney) :
        L,l = 1,1
        a  = np.array( [l*0.5, np.sqrt(3)*l*0.5] )
        b  = np.array( [l*0.5,-np.sqrt(3)*l*0.5] )
        x_ = np.linspace( 1,N,N )
        y_ = np.linspace( 1,N,N )
        Nx , My = np.meshgrid ( x_,y_ )
        Rs = pd.DataFrame( np.array( [ a*n+b*m for n,m in zip(Nx.reshape(-1),My.reshape(-1)) if bFun(n,m) ] ) )
        Rs .columns = ['X','Y']
        return ( Rs )

if __name__ == '__main__' :
        print(generate_plaque(N=20,bFun=bHoney))
