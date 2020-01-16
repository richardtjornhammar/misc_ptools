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


def simple_bokeh_scatter(X,Y,names=None,title=''):
    from bokeh.plotting import figure, output_file, ColumnDataSource
    from bokeh.models   import HoverTool, Range1d, Text, Row
    from bokeh.models   import Arrow, OpenHead, NormalHead, VeeHead, Line
    #
    if not names is None :
       add = { 'name' : names } 
    #
    source = ColumnDataSource ( data ={ **{'x' : X , 'y' : Y , 'color': ['#ff0000' for v in X] } , **add } )
    ttips = [   ("index "  , "$index"   ) ,
                ("(x,y) "  , "(@x, @y)" ) ]
    #
    if not names is None :
        for key in add.keys() :
            ttips.append( ( str(key) , '@'+str(key) ) )
    #
    hover = HoverTool ( tooltips = ttips )
    #
    p = figure ( plot_width=600 , plot_height=600 , 
           tools = [hover,'box_zoom','wheel_zoom','pan','reset','save'],
           title = title ) 
    p.circle( 'x' , 'y' , size=12, source=source , color='color' )
    p.output_backend='webgl'
    return(p)
