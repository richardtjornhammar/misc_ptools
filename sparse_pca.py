"""
Copyright 2020 RICHARD TJÖRNHAMMAR

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import numpy as np
import pandas as pd

class sPCA( object ) :
    #
    # THIS CLASS PERFORMS A SPARSE PCA
    # IT USES THE SPARSE SVD ALGORITHM
    # FOUND IN SCIPY
    #
    def __init__ ( self,X,k=-1,fillna=None ) :
        from scipy.sparse import csc_matrix
        from scipy.sparse.linalg import svds
        self.svds_,self.smatrix_ = svds,csc_matrix
        self.components_ = None
        self.F_ = None
        self.U_ , self.S_, self.V_ = None,None,None
        self.evr_ = None
        self.var_ = None
        self.fillna_ = fillna
        self.X_   = self.interpret_input(X)
        self.k_   = k

    def interpret_input ( self,X ) :
        if 'pandas' in str(type(X)) :
            for idx in X.index :
                X.loc[idx] = [ np.nan if 'str' in str(type(v)) else v for v in X.loc[idx].values ]
            if 'float' in str(type(self.fillna_)) or 'int' in str(type(self.fillna_)) :
                X = X.fillna(self.fillna_)
            self.X_ = X.values
        else :
            self.X_ = X
        return( self.X_ )

    def fit ( self , X=None ) :
        self.fit_transform( X=X )

    def fit_transform ( self , X=None ) :
        X = self.X_
        if not X is None : # DID THE USER SUPPLY NEW DATA
            X = self.interpret_input(X)
        Xc = X - np.mean( X , 0 )
        if self.k_<=0:
            k_ = np.min(np.shape(X))-1
        else:
            k_ = self.k_
        u, s, v = self.svds_ ( self.smatrix_(Xc, dtype=float) , k=k_ )
        S = np.diag( s )
        self.F_   = np.dot(u,S)
        self.var_ = s ** 2 / Xc.shape[0]
        self.explained_variance_ratio_ = self.var_/self.var_.sum()
        self.U_ , self.S_ , self.V_ = u,s,v
        self.components_ = self.V_        
        return ( self.F_ )
