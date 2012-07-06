#!/usr/bin/python
"""
library to perform various file to python conversions
 
Copyright (c) 2011 Renjith P Ravindran (renjithforever@gmail.com)
 
This python library is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, the version 3 of the License.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this.  If not, see <http://www.gnu.org/licenses/>.
"""
import codecs

class FormatError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


def remove_comments(file,oneLine='#',multiStart='#---',multiEnd='---#'):
	"""
	take in s file object,removes comments as defined by arguemenmts and returns the file content as string
	"""
	try:
		fileBlk=file.read()
		while fileBlk.find(multiStart)>-1:
			comment_start=fileBlk.find(multiStart)
			comment_end=fileBlk[comment_start+len(multiStart):].find(multiEnd)+comment_start+len(multiEnd)+len(multiStart)
			comment=fileBlk[comment_start:comment_end]
			if comment:
				fileBlk=fileBlk.replace(comment,'')
		fileBlk=fileBlk.replace("\n\n","\n").lstrip("\n").rstrip("\n").lstrip().rstrip()

		while fileBlk.find(oneLine)>-1:
			comment_start=fileBlk.find(oneLine)
			comment_end=fileBlk[comment_start:].find("\n")+comment_start
			comment=fileBlk[comment_start:comment_end]
			if comment:
				fileBlk=fileBlk.replace(comment,'')

		fileBlk=fileBlk.replace("\n\n","\n").lstrip("\n").rstrip("\n").lstrip().rstrip()
		return fileBlk
	except IOError:
		print "sorry file not found!"





def dictionary(file,field_seperator=' ',record_seperator='\n'):
	"""
	converts a given file of data into a python dictionary;
	
	arguements:
		file => the given data file
		field_seperator => whatever that separates two fields , eg ',' , ' ' , '|' etc default =' '
		record_seperator => whatever that seperates a record, default new line

	fill should be as below:
		
		<field1><field_seperator><field2><field_seperator>
		<record_seperator>
		<field1><field_seperator><field2><field_seperator>

	the resultant dictionary will hav the first field as the key and the following field as value.
	if there are more than 2 fields per record then then the dictionary value will hold a python list with fields except the first one as elements. 
	
	"""
	dict={}
	try:
		
		if record_seperator != '\n':
			pass# will deal with this later!
		else:
			file=remove_comments(file)
			file=file.split("\n")
			for line in file:
				line=line.rstrip('\n')# removinf the trailing newline char
				if not line:
					continue 
				fields = line.split(field_seperator)
				if len(fields) <2:
					raise FormatError("")
				dict_key = fields.pop(0)
				if len(fields) > 1:
					dict_value = fields
				else:
					dict_value = fields[0]
				dict[dict_key] = dict_value

			return dict
	except  IOError:
		print "sorry, file not found"
	except FormatError:
		print "sorry given file has a wrong format"



def dictionary_spl(file,field_seperator=' ',record_seperator='\n'):
	"""
	converts a given file of data into a python dictionary;
	
	arguements:
		file => the given data file
		field_seperator => whatever that separates two fields , eg ',' , ' ' , '|' etc default =' '
		record_seperator => whatever that seperates a record, default new line

	fill should be as below:
		
		<field1><field_seperator><field2><field_seperator>
		<record_seperator>
		<field1><field_seperator><field2><field_seperator>

	the resultant dictionary will hav the first field as the key and the following field as value.
	if there are more than 2 fields per record then then the dictionary value will hold a python list with fields except the first one as elements. 
	
	"""
	dict={}
	try:
		
		if record_seperator != '\n':
			pass# will deal with this later!
		else:
			file=remove_comments(file)
			file=file.split("\n")
			for line in file:
				line=line.rstrip('\n')# removinf the trailing newline char
				if not line:
					continue 
				fields = line.split(field_seperator)
				if len(fields) <2:
					raise FormatError("")
				dict_key = fields.pop(0)
				#print dict_key

				if dict_key in dict:
					value=[]
					value.append(fields[0])
					value.append(fields[1])
					dict[dict_key].append(value)
				else:
					dict[dict_key]=[]
					value=[]
					value.append(fields[0])
					value.append(fields[1])
					dict[dict_key].append(value)

			return dict
	except  IOError:
		print "sorry, file not found"
	except FormatError:
		print "sorry given file has a wrong format"


#--------------------------------------------------------------------------------------------------------------------------------

def list(file,record_seperator="\n"):
	"""
	takes in a file object and returns the lines in it as a python list
	"""

	try:
		new_list=[]
		file=remove_comments(file)
		#print file
		file=file.split(record_seperator)
		for line in file:
			new_list.append(line)
		return new_list
	except Exception,e:
		print e
#---------------------------------------------------------------

def dictionary_forGrammar(file,lhsRhs_seperator='=>',orRule_seperator='|',record_seperator='\n'):
	"""
	this is for the parser not to be used generally..
	"""
	dict={}
	multiComment=False
	try:
		if record_seperator != '\n':
			pass# will deal with this later!
		else:
			file=remove_comments(file)
			file=file.split("\n")
			for line in file:
				

				rhs=line.split(lhsRhs_seperator)[0]
				if not rhs:
					raise FormatError("")
				lhs=line.split(lhsRhs_seperator)[1].split(orRule_seperator)
				if not lhs:
					raise FormatError("")
				for term in lhs:
					if dict.has_key(term):
						raise FormatError("")
					if term == '':
						continue
					dict[term]=rhs


			if multiComment:
				raise FormatError("")

			return dict
	except  IOError:
		print "sorry, file not found"
	except FormatError:
		print "sorry given file has a wrong format"

#--------------------------------------------------------------------------------------------------------------------------------
import cPickle as pickle
"""
testing.
"""
if __name__ == '__main__':
		"""
		dict=list(codecs.open("t.txt","r","utf-8"))
		print ",".join(dict).encode("utf-8")
		str=remove_comments(open("grammar.txt","r"))
		print "-----------"
		print str
		"""
		f=codecs.open("../mal2eng0/t2.txt","r","utf-8")
		dict =dictionary_spl(f,",")
		print dict
