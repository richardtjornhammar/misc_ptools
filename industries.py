import pandas as pd

def add_to_dict(k,v,d):
	if k in d :
		d [ k ].append(v)
	else :
		d [ k ] = [v]
	return ( d )

def parse_industry_information( filename = 'industries.txt', bWrite = True ):
	print ( 'READING INDUSTRY SECTOR DATA' )
	#
	crop_b = lambda k : k if not k[0 ] ==' ' else k[1: ]
	crop_e = lambda k : k if not k[-1] ==' ' else k[:-1]
	parent_child , child_parent = {} , {}
	long_story = ""
	linear_content = []
	with open ( filename , 'r' ) as input :
		for line in input :
			long_story += line
			if '»' in line :
				k , v = line.split('»')[:-1]
				k = crop_b(k); k = crop_e(k)
				v = crop_b(v); v = crop_e(v)
				linear_content.append ( v )			
				parent_child = add_to_dict ( k , v , parent_child )
				child_parent = add_to_dict ( v , k , child_parent )
	stock_sep	= ','
	sdf 		= None
	#
	for iw in range(len(linear_content)) :
		w = linear_content[iw]
		story = long_story.split(w)[1]
		short_story = story
		if iw+1<len(linear_content) :
			u = linear_content[iw+1]
			short_story = story.split(u)[0]
		matrix = short_story.split('Report')[2].split('\n\n')[0].split('\t')
		stocks = [ m  for m in matrix if not '\n' in m and not '$' in m and not '%' in m and len(m)>1 and not '/' in m ]
		if sdf is None :
			sdf  = pd.DataFrame( [ stock_sep.join(stocks) , stock_sep.join(child_parent[w]) ] ,
						columns=[w] , index=['symbols','parent'] ).T
		else :
			tdf_ = pd.DataFrame( [ stock_sep.join(stocks) , stock_sep.join(child_parent[w]) ] ,
						columns=[w] , index=['symbols','parent'] ).T
			sdf  = pd.concat([ tdf_ ,sdf ])
	print ( sdf )
	if bWrite :
		sdf.to_csv('market_sectors_and_industries.csv','\t')
		sdf.to_html('market_sectors_and_industries.html')
	return(sdf)
	
if __name__ == '__main__' :
	parse_industry_information( filename = 'industries.txt', bWrite = True )
