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
import numpy  as np
import pandas as pd

def simple_bokeh_scatter(X,Y, info_df = None, title='', axis=0, default_color=None,backend='webgl' ):
    from bokeh.plotting import figure, output_file, ColumnDataSource
    from bokeh.models   import HoverTool, Range1d, Text, Row
    from bokeh.models   import Arrow, OpenHead, NormalHead, VeeHead, Line
    #
    add = None
    if default_color is None:
        default_color = '#ff0000'
    if 'pandas' in str(type(info_df)) :
       if axis==1 :
           info_df = info_df.T
       add = {}
       for idx in info_df.index.values:
           add = {**add,**{ str(idx) : info_df.loc[idx].values }}
    if add is None :
        data = { **{'x' : X , 'y' : Y , 'color': [ default_color for v in X] } }
    else :
        if 'list' in str(type(default_color)):
            cols = default_color
        else:
            cols = [ default_color for v in X]
        data = { **{'x' : X , 'y' : Y , 'color': cols } , **add }
    source = ColumnDataSource ( data = data )
    ttips = [   ("index "  , "$index"   ) ,
                ("(x,y) "  , "(@x, @y)" ) ]
    if not add is None :
        for key in add.keys() :
            ttips.append( ( str(key) , '@'+str(key) ) )
    hover = HoverTool ( tooltips = ttips )
    p = figure ( plot_width=600 , plot_height=600 , 
           tools = [hover,'box_zoom','wheel_zoom','pan','reset','save'],
           title = title ) 
    p.circle( 'x' , 'y' , size=12, source=source , color='color' )
    p.output_backend = backend
    return( p )


class APCA ( object ) :
    #
    # THIS CLASS PERFORMS A PCA
    # IT USES THE SPARSE SVD ALGORITHM
    # FOUND IN SCIPY.
    #
    def __init__ ( self , X=None , k=-1 , fillna=None , transcending=True) :
        from scipy.sparse import csc_matrix
        from scipy.sparse.linalg import svds
        self.svds_ , self.smatrix_ = svds , csc_matrix
        self.components_ = None
        self.F_ = None
        self.U_ , self.S_, self.V_ = None,None,None
        self.evr_ = None
        self.var_ = None
        self.fillna_ = fillna
        self.X_   = self.interpret_input(X)
        self.k_   = k
        self.transcending_ = transcending

    def interpret_input ( self,X ) :
        if 'pandas' in str(type(X)) :
            for idx in X.index :
                X.loc[idx] = [ np.nan if 'str' in str(type(v)) else v for v in X.loc[idx].values ]
            if 'float' in str(type(self.fillna_)) or 'int' in str(type(self.fillna_)) :
                X = X.fillna(self.fillna_)
            self.X_ = X.values
        else :
            self.X_ = X
        return ( self.X_ )

    def fit ( self , X=None ) :
        self.fit_transform( X=X )

    def fit_transform ( self , X=None ) :
        if X is None:
            X = self.X_
        if not X is None :
            X = self.interpret_input(X)
        Xc = X - np.mean( X , 0 )
        if self.k_<=0 :
            k_ = np.min( np.shape(Xc) ) - 1
        else:
            k_ = self.k_
        u, s, v = self.svds_ ( self.smatrix_(Xc, dtype=float) , k=k_ )
        if self.transcending_ :
            u, s, v = self.transcending_order(u,s,v)
        S = np.diag( s )
        self.F_   = np.dot(u,S)
        self.var_ = s ** 2 / Xc.shape[0]
        self.explained_variance_ratio_ = self.var_/self.var_.sum()
        self.U_ , self.S_ , self.V_ = u,s,v
        self.components_ = self.V_
        return ( self.F_ )

    def transcending_order(self,u,s,v) :
        return ( u[:,::-1],s[::-1],v[::-1,:] )

    def apply_matrix( self , R ) :
        self.U_ = np.dot( self.U_,R.T  )
        self.V_ = np.dot( self.V_.T,R.T ).T
        self.F_ = np.dot( self.F_,R.T )
        self.components_ = self.V_
        return ( self.F_ )
