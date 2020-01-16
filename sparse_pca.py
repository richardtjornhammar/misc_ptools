class sPCA( object ) :
    #
    # THIS CLASS PERFORMS A SPARSE PCA
    # IT USES THE SPARSE SVD ALGORITHM
    # FOUND IN SCIPY
    #
    def __init__ ( self,X,k=2,fillna=None ) :
        from scipy.sparse import csc_matrix
        from scipy.sparse.linalg import svds
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

    def fit_transform ( self , X=None ) :
        X = self.X_
        if not X is None : # DID THE USER SUPPLY NEW DATA
            X = self.interpret_input(X)
        Xc = X - np.mean( X , 0 )
        u, s, v = svds ( csc_matrix(Xc, dtype=float) , k=self.k_ )
        S = np.diag( s )

        self.F_   = np.dot(u,S)
        self.var_ = s ** 2 / Xc.shape[0]
        self.explained_variance_ratio_ = self.var_/self.var_.sum()
        self.U_ , self.S_ , self.V_ = u,s,v
        self.components_ = self.V_
        
        return ( self.F_ )
