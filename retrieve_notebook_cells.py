#	RESCUE TOOL FOR JUPYTER NOTEBOOKS
#	GET ALL CODE OUT OF CELLS AND DUMP
#	TO COMMAND PROMPT
#
import ast
import sys

class SomeFile(object):
	def __init__(self):
		self.name  = ""
		self.datas = {}		# INPUT STRING FROM READ
		self.datal = list([])	# LIST OF TAGGED ENTRIES
		self.datae = {} 	# EVALUATED DATA
		self.datap = ""		# PRUNED DATA STRING
		self.data  = {} 	# DATA WE WANT TO RETURN

	def reading ( self ):
		with open( self.name, 'r') as f:
			s = f.read()
			self.datas = s

	def convert_stringdata ( self ):
		self.datae = ast.literal_eval(self.datas)

	def writing ( self ):
        	target = open('return_'+self.name, 'a')
        	target.write(str(self.datap))
        	print ( self.data )

	def print_on_1tag ( self , tag_str ):
		sp_str=self.datas.split(tag_str)
		print ( sp_str[1][2:-1] )

	def retrieve_between( self, tag1 , tag2 ):
		sp_str1   = self.datas.split(tag1)
		sp_str2   = self.datas.split(tag2)
		n = len(sp_str1)-1
		pad = 6
		for i in range(n) :
			if i<n :
				self.datap += "\n\n######## NEW CELL\n\n"
				nsp = sp_str1[i].split(tag2)[0]
				all_lines= nsp.split('\\n"')
				clean_lines = [ (line.split('\n    "')) for line in all_lines ]
				for line in clean_lines:
					self.datap += line[-1]+'\n'


if __name__ == '__main__' :
	notebook = SomeFile()
	fname = sys.argv[1]
	notebook.name = fname
	notebook.reading()
	notebook.retrieve_between('"source": [','"\n   ]')
	print( notebook.datap )

