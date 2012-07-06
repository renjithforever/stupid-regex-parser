#! /usr/bin/python
"""
LinkedTree-Parser: a simple parser based on a basic finite automaton engine.
 
Copyright (c) 2011 Renjith P Ravindran (renjithforever@gmail.com)
 
LinkedTree-Parser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, the version 3 of the License.

This library(LinkedTree-Parser) is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this.  If not, see <http://www.gnu.org/licenses/>.

----------------------------------------------------------------- 
This parser can handle grammer that comes under regular expressions, and was written as the base parser for a machine translation project (malayalam to english traslation) of Mrs. Latha Nair (CUSAT).

Currently the regex engine does not support charecter classes or other regex features provided by grep or other similar tools.



"""

import types
import logger
import sys
# Log everything, and send it to stderr.
if __name__=="__main__":
	log.basicConfig(filename='parser.log',filemode='w',level=log.DEBUG,format='%(levelname)s:%(message)s')




class TermNode:
	"""
	node object for the linked list.
	"""
	def __init__(self):
		self.term=None
		self.attribute={}
		self.next=None
		self.prev=None
		self.children=[]


class Parser:
	"""
	main class for the parser
	"""
	def __init__(self):
		self.reset()

	def reset(self):
		self.cur=None
		self.start=None
		self.matchedTerms=[]
		self.currentRule=[]
		self.currentSearch_kleenCount=0
		self.debugFlag=False
		self.currentTrans=''

	def currentRuleTerm(self,rt_pointer):
		"""
		returns the current rule term and its type(posi,kleen) from currentRule
		"""
		if '+' in self.currentRule[rt_pointer]:
			return self.currentRule[rt_pointer].replace('+',''),'+'
		elif '*' in self.currentRule[rt_pointer]:
			return self.currentRule[rt_pointer].replace('*',''),'*'
		elif '~' in self.currentRule[rt_pointer]:
			return self.currentRule[rt_pointer].replace('~',''),'~'
			# ~ indicates a rule that is to be skipped, a spl case check matched().
		else:
			return self.currentRule[rt_pointer],''

	def doDebug(self,choice=True):
		"""
		a switch that controls writing debug info to file
		"""
		if isinstance(choice,bool):
			self.debugFlag=choice



	def addTerm(self,term,attribute=False):
		"""
		adds nodes to linked list from input.
		"""
		newTerm=TermNode()
		if self.start==None:
			self.start=newTerm
			newTerm.term=term.upper()

			if attribute:
				attribute=attribute.split(",")
				key1=attribute[0].split(':')[0]
				value1=attribute[0].split(':')[1]
				key2=attribute[1].split(':')[0]
				value2=attribute[1].split(':')[1]
				newTerm.attribute[key1]=value1
				newTerm.attribute[key2]=value2

			
		else:
			newTerm.term=term.upper()
			if attribute:

				attribute=attribute.split(",")
				key1=attribute[0].split(':')[0]
				value1=attribute[0].split(':')[1]
				key2=attribute[1].split(':')[0]
				value2=attribute[1].split(':')[1]
				newTerm.attribute[key1]=value1
				newTerm.attribute[key2]=value2
			self.cur.next=newTerm
			newTerm.prev=self.cur
		
		self.cur=newTerm

	def search(self,key):
		"""
		wrapper func that starts a rule search on the linked list.
		"""
		node=self.start
		self.currentRule=key.split(' ')
		self.matchedTerms=[]
		
		parseResult=self.matched2(node,0,False,False)


		if parseResult==0 :
			return 0
		elif parseResult==-1:
			logger.misc_debug(self,"error","search():: some error happed and matched() returned error!")
			return -1
		else:
			return self.matchedTerms
	

						
	def matched2(self,ip_pointer,rt_pointer,kleen_loop,posi_loop):
		"""
		this is the heart, the regex engine.
		"""
		if(ip_pointer == None and rt_pointer < len(self.currentRule) and not kleen_loop 
				and not posi_loop and self.currentRuleTerm(rt_pointer)[1]!='*'):
			msg="	#[A]input reaches end without rule term overflowing and kllen and \
					posi are down."
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return 0

		if(ip_pointer == None and rt_pointer < len(self.currentRule) and not kleen_loop 
				and not posi_loop and self.currentRuleTerm(rt_pointer)[1]=='*'):
			msg="	#[A]input reaches end without rule term overflowing and kllen \
					and posi are down."
			msg+="\n#checking for kleen is to avoid Negetive in this:rule=A B C*:\
					ip=A B..here the ip maybecome null and rule may not over flow.\
					.still its valid as last term was kleen!!!!!"
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return self.matched2(ip_pointer,rt_pointer+1,kleen_loop,posi_loop)
		elif(rt_pointer == len(self.currentRule) and len(self.matchedTerms)>0):
			msg="	#[B]rule terms have overflowed..meaning all rule terms have been \
					successfully matched."
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return 1

		elif(rt_pointer == len(self.currentRule) and len(self.matchedTerms)==0):
			msg="	#[B]rule terms have overflowed...and no matches ..this is a fringe \
					case..like rule=A*,input =B"
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return 0

		elif(kleen_loop and ip_pointer !=None):
			if(rt_pointer==len(self.currentRule)-1 and ip_pointer.term == self.currentRuleTerm(rt_pointer)[0]):
				msg="	#[C1]current rule term is the last one and there is a sub term\
						match, and there could be more."
				msg+="\n	#state changes to E if no more input"
				msg+="\n	#state changes to same C1 if input has more terms."
				self.matchedTerms.append(ip_pointer)
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer.next,rt_pointer,kleen_loop,posi_loop)
			elif(rt_pointer==len(self.currentRule)-1 and ip_pointer != self.currentRuleTerm(rt_pointer)[0] 
					and len(self.matchedTerms)>0):
				msg="	#[C2] ...kleen loop termination when last rule term is a kleen term."
				msg+="\n	#because kleen is 0 or more ..we simply skip it. and state changes to E."
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer+1,kleen_loop,posi_loop)
				return self.matched2(ip_pointer,rt_pointer+1,kleen_loop,posi_loop)
			elif(rt_pointer==len(self.currentRule)-1 and ip_pointer != self.currentRuleTerm(rt_pointer)[0] 
					and len(self.matchedTerms)==0):
				msg="	#[C2.5] ...kleen loop termination when last rule term is a kleen term \
						and no previos matches."
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer+1,kleen_loop,posi_loop)
				return self.matched2(ip_pointer.next,rt_pointer,kleen_loop,posi_loop)
			elif(ip_pointer.term != self.currentRuleTerm(rt_pointer)[0] and len(self.matchedTerms)<1):
				msg="	#[C3] . 0 sub matches so far.. ie. searching for Initial hooking."
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer.next,rt_pointer,kleen_loop,posi_loop)
			elif(ip_pointer.term != self.currentRuleTerm(rt_pointer)[0] and len(self.matchedTerms)>0):
				msg="	#[C4]. straighforward kleen loop termination "
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer,rt_pointer+1,False,posi_loop)
			elif(ip_pointer.term == self.currentRuleTerm(rt_pointer)[0]):
				msg="	#[C5]. kleen term in loop matches...will continue untill C4"
				self.matchedTerms.append(ip_pointer)
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer.next,rt_pointer,kleen_loop,posi_loop)
		elif(kleen_loop and ip_pointer == None and len(self.matchedTerms)<1):
			msg="	#[D] a kleen loop reaches end of input in search of init hooking."
			msg+="\n	#input is reset and kleen rule term is skipped and kleen flag dropped."
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			mod=self.currentRule[rt_pointer]
			mod=mod.replace("*","~")
			self.currentRule.pop(rt_pointer)
			self.currentRule.insert(rt_pointer,mod)
			return self.matched2(self.start,rt_pointer+1,False,posi_loop)
		elif(kleen_loop and ip_pointer == None and len(self.matchedTerms)>0):
			msg="	#[E]previously hooked rule causes end of input in kleen loop."
			msg+="\n	#if this was the last rule term state change leads to B"
			msg+="\n	#if not,state change leads to A"
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return self.matched2(ip_pointer,rt_pointer+1,False,posi_loop)

		elif(posi_loop and ip_pointer !=None):
			if (ip_pointer.term == self.currentRuleTerm(rt_pointer)[0]):
				msg="	#[F1] a posi term matches.. simple.. :)"
				self.matchedTerms.append(ip_pointer)
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer.next,rt_pointer,kleen_loop,posi_loop)
			elif(ip_pointer.term != self.currentRuleTerm(rt_pointer)[0] and len(self.matchedTerms)==0):
				msg="	#[F1.5] posi term donot match and mathed terms is empty ..Negative"
				logger.stateMachine_debug(self,msg,ip_pointer.next,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer.next,rt_pointer,kleen_loop,posi_loop=False)
			elif(ip_pointer.term != self.currentRuleTerm(rt_pointer)[0] 
					and self.matchedTerms[-1].term==self.currentRuleTerm(rt_pointer)[0]):
				msg="	#[F2] posi term donot match but matched the previous input term..\
						good enough. ie. 1 or more match"
				msg+="\n	# this is a posi loop termination before end of input."
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer,rt_pointer+1,kleen_loop,posi_loop=False)
		
			elif(ip_pointer.term != self.currentRuleTerm(rt_pointer)[0] 
					and self.matchedTerms[-1].term !=self.currentRuleTerm(rt_pointer)[0]):
				msg="	#[F3] here we have a 0 posi term match ..which means trouble."
				msg+="\n	#discard prevous matches and reset rule pointer and continue with input pointer"
				self.matchedTerms=[]
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer,0,kleen_loop,posi_loop=False)
		elif (posi_loop and ip_pointer == None and self.matchedTerms[-1].term == self.currentRuleTerm(rt_pointer)[0] ):
			msg="	#[G] posi loop termination with end of input"
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return self.matched2(ip_pointer,rt_pointer+1,kleen_loop,posi_loop=False)

		elif(self.currentRuleTerm(rt_pointer)[1]=='*'):
			msg="	#[H] initiating a kleen loop"
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return self.matched2(ip_pointer,rt_pointer,kleen_loop=True,posi_loop=False)
		elif(self.currentRuleTerm(rt_pointer)[1]=='+'):
			msg="	#[I] initiating a posi loop"
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return self.matched2(ip_pointer,rt_pointer,kleen_loop=False,posi_loop=True)
		elif(self.currentRuleTerm(rt_pointer)[1]=='~'):
			msg="	#[M]..skipping the not available kleen term "
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return self.matched2(ip_pointer,rt_pointer+1,kleen_loop=False,posi_loop=posi_loop)
		elif(self.currentRuleTerm(rt_pointer)[1] == '' and ip_pointer.term == self.currentRuleTerm(rt_pointer)[0]):
			msg="	#[J] a basic rule term matches... peace!"
			self.matchedTerms.append(ip_pointer)
			logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
			return self.matched2(ip_pointer.next,rt_pointer+1,kleen_loop,posi_loop)
		elif(self.currentRuleTerm(rt_pointer)[1] == '' and ip_pointer.term != self.currentRuleTerm(rt_pointer)[0]):
			if self.matchedTerms:
				self.matchedTerms=[]
				msg="	#[K] basic rule term fails to match discard previous matches,\
						reset rule pointer and continue ip pointer"
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer,0,kleen_loop,posi_loop)
			else:
				msg="	#[L] basic rule term fails to match ..no previous matches so skipping,\
						reset rule pointer and increment pointer"
				logger.stateMachine_debug(self,msg,ip_pointer,rt_pointer,kleen_loop,posi_loop)
				return self.matched2(ip_pointer.next,0,kleen_loop,posi_loop)
		else:

			logger.stateMachine_debug(self,"what crap!!",ip_pointer,rt_pointer,kleen_loop,posi_loop)



	def printList(self): 
		"""
		prints the items in the list
		"""
		node=self.start
		nodes=''
		while node:
			print node.term,
			nodes+=node.term+' '
			node=node.next

	def insert(self,term,children):
		"""
		inserts rhs of the matched rule as a node after deleting the macthed nodes
		"""

		prev_node=children[0].prev
		next_node=children[len(children)-1].next
		node=TermNode()
		node.term=term
		if children[0]==self.start:
			self.start=node
		if prev_node:
			prev_node.next=node
	
		if next_node:
			next_node.prev=node
		node.next=next_node
		node.prev=prev_node
		for child in children:
			child.next=None
			child.prev=None
			node.children.append(child)



		
	def distToStart(self,match):
		"""
		used to find the distance as number of nodes from start of list to first matched node.
		this is used to make decsion on which match to choose.
		"""
		dist=1
		if match[0]==self.start:
			return 0
		else:
			node=match[0]
			while node.prev!=self.start:
				dist=dist+1
				node=node.prev
		
		return dist
	
	

	def print_parseTree(self):
		"""
		print parse tree
		"""
		self.depthFirstTrav(self.start)

	def depthFirstTrav(self,node,attributeKey=None):
		"""
		depth first traversal is used to get all the node tags in order.
		"""
		if not attributeKey:
			if node == None:
				sys.stderr.write("tree empty!!!")
				return 0
			if len(node.children)==0:
				sys.stdout.write(node.term.encode("utf-8"))
				return 1
			else:
				sys.stdout.write(node.term+'(')
				for c_index in range(len(node.children)):
					if c_index == (len(node.children) - 1):
						self.depthFirstTrav(node.children[c_index])
						sys.stdout.write(')')
					else:
						self.depthFirstTrav(node.children[c_index])
						sys.stdout.write(', ')
		
				
				return 1
		else:
			if node == None:
				logger.misc_debug(self,"critical","TREE EMPTY!!! :P")
				return 0
			if len(node.children)==0:
				self.currentTrans+=node.attribute[attributeKey].encode("utf-8")+" "

				return 1
			else:
				for c_index in range(len(node.children)):
					if c_index == (len(node.children) - 1):
						self.depthFirstTrav(node.children[c_index],attributeKey)
					else:
						self.depthFirstTrav(node.children[c_index],attributeKey)
		
				
				return 1
	



	def parse(self,grammar,traceReduction=True):
		"""
		parses the input(as a list) based on `grammar`

		"""
	#and let the parsing begin
		mainLoopIter=0
		while(True):
			mainLoopIter+=1
			logger.parser_debug(self,"__________________________________main loop: %%__",mainLoopIter)
			reduce=None
			match=None
			dist=None
			for k,v in grammar.items():
				logger.parser_debug(self,"\tSTART SEARCH FOR:%%",k)
				matchedTerms=self.search(k)
				if matchedTerms!=-1 and matchedTerms!=0:
					logger.parser_debug(self,"\tMATCH FOUND, rule= %%",k)
					terms=''
					for term in matchedTerms:
						terms+=term.term+' '
					logger.parser_debug(self,"\tMATCHED TERMS ARE..%%",terms)
					logger.parser_debug(self,"\tABOVE TERMS SHALL REDUCE TO: %%",v)
					if v=='START' and not self.start.next == None:
						continue
					d=self.distToStart(matchedTerms)
					logger.parser_debug(self,"\tDISTANCE of the TERMS: %%",d)
					if dist==None or d<dist:#implements the left to right scanning of inputs
						dist=d
						logger.parser_debug(self,"\tTHIS MATCH IS MORE TO THE LEFT THAN PREVIOUS\nCHOOSING THIS(policy:left - right scanning)")
						match=matchedTerms
						reduce=v
					elif d==dist:
						if len(matchedTerms)>len(match):#implements the policy of choosing the longest reduction
							match=matchedTerms
							logger.parser_debug(self,"\tTHIS MATCH IS AT SAME DIST TO PREVIOUS BUT IS LONGER THAN PREVIUOS\n CHOOSING THIS(policy: use longest match)")
							reduce=v
						elif len(matchedTerms)==len(match):#possibly this will never happen..as all(not really..:P) ambigous rules are elimintaed in ruleTable expansion
							match=matchedTerms
							logger.parser_debug(self,"\tTHIS MATCH IS AT SAME DIST TO PREVIOUS AS WELL AS HAS SAME LENGHTH..AMBIGUITY!")
							reduce=v
					
						
				else:
					logger.parser_debug(self,"\tSEARCH RETURNS FALSE")	
					pass
			if reduce =='START':
				logger.parser_debug(self,"\tSUCCESS: REDUCTION COMPLETED")
				break
			if match==None:
				logger.misc_debug(self,"error","\tREDUCTION FAILED!!!")
				return False
			matchedString=''
			for term in match:
				matchedString+=term.term+' '

			logger.parser_debug(self,"\tTHIS MATCH FINALLY CHOSEN FOR REDUCTION!!: matched=%%  reduced=%%\n",matchedString,reduce)
			self.insert(reduce,match)
			
			if traceReduction:
				#self.printList()
				#print ""
				pass
			logger.parser_debug(self,"\n")

		return True


	def customAlteration_of_parseTree(self,alterFunc,table):
		"""
		a this wrapper function will let a non member funtion alter the parse tree, to custom needs.
		"""
		node=self.start

		alterFunc(node,table)



	def init_tokenStream(self,stream,tokenSeperator=' ',customFunc=None,lookUp=None):
		"""
		Token stream is converted into a linked list, also can act as a wraper for a custom function
		"""
		if isinstance(customFunc,types.FunctionType) and isinstance(lookUp,dict):
			return customFunc(self,stream,tokenSeperator,lookUp)
		else:
			if len(stream) == 0:
				sys.stderr.write("\nstream empty!")
				return 0


			tokens=stream.split(tokenSeperator)
			for token in tokens:
				self.addTerm(token)

			return 1

	def print_leafNodeAttributes(self,key="engTrans"):
		"""
		leaf nodes would contain all the initial nodes and would have their translatiosn too.
		"""
		start=self.start

		self.depthFirstTrav(start,key)

