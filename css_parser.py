#!/usr/bin/python
# ------------------------------------------------------------
# CSSP: CSS Preprocessor (bitremix.com/p/cssp)
# Ver: 0.0.1
# Copyright 2010 Francisco Pinzon: (pacho@bitremix.com)
# ------------------------------------------------------------
#
#css_parser.py
#This file is part of CSSP.
#
#CSSP is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.
#
#CSSP is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with CSSP.  If not, see <http://www.gnu.org/licenses/>.
#
# ------------------------------------------------------------
from css_lexer import tokens
import ply.yacc as yacc
import sys
import logging

DEBUG=False

#dictionary of constants
constants={}
#directory of plain rules
plain_rules=[]
#directory of directionable rules
directionable_rules={}


#Root of the BNF Hierarchy. Represents the cssp document.
def p_doc(t):
	'doc : constant_block rule_block'
	t[0]=plain_rules

#The cssp document is composed by two blocks. The first is of constant definitions and the second is of the classic css selectors.
def p_blocks(t):
	'''constant_block : constant_block constant_definition
					|
		rule_block : rule_block rule 
					| '''
	pass
	
#Represents the constant definitions.
def p_constant_definition(t):
	'constant_definition : DOLLAR STRING EQUALS STRING'
	tokenConsole("constant_definition",t)
	constants[t[2]]=t[4]

#Represents the constant name. Only for non-declarative purposes.
def p_constant_name(t):
	'constant_name : DOLLAR STRING'
	tokenConsole("constant_name",t)
	t[0]=constants[t[2]]

#Function to use a list as a dictionary. The list is composed by tuples where the first element acts as the dictionary key, and thee second is the object.
def getIndexByKey(tup,key):
	for a in tup:
		if(a[0]==key):
			return tup.index(a)
	raise KeyError(str(key)+" not found in "+str(tup))

#Represents the set of rule name, selector and properties.
def p_rule(t):
	'rule : rule_declaration LCURL properties_block RCURL'
	props=t[3]
	try:
		if(t[1][0]!=None):
			dr=directionable_rules[t[1][0]] 
			directionable_rules[t[1][0]]=props
	except KeyError:
		pass
	try:
		if(t[1][1]!=None):
			num=getIndexByKey(plain_rules,t[1][1])
			obj=plain_rules.pop(num)
			obj[1]=props
			plain_rules.insert(num,obj)
	except KeyError:
		pass

	#console(str(plain_rules))
	#console(str(directionable_rules))

#Represents a rule declaration,its name (for make it directionable) and its selector.
def p_rule_declaration(t):
	'rule_declaration : rule_name new_rule selector new_selector'
	t[0]=[t[1],t[3]]

#For calling inline from the function before.
def p_new_rule(t):
	'new_rule :'
	if(t[-1]!=None):
		directionable_rules[t[-1]]=[]

#For calling inline from the function before.	
def p_new_selector(t):
	'new_selector :'
	if(t[-1]!=None):
		plain_rules.append([t[-1],[]])
		
#To replace a rule calling by its name.
def p_rule_name(t):
	'''rule_name : AT STRING
				| '''
	try:
		t[0]=t[2]
	except IndexError:
		t[0]=None

#Represents a CSS selector.
def p_selector(t):
	'''selector : STRING
				| STRING COLON STRING
				| '''
	if(len(t)==2):
		t[0]=t[1]
	elif(len(t)==4):
		t[0]=t[1]+":"+t[3]
	else:	
		t[0]=None

#For joining lists and objects indiferently.
def add(t1,t2):
	if(type(t1[0])==list):
		if(type(t2)!=list):
			t1.append(t2)
			return t1
		else:
			t1.extend(t2)
			return t1
	else:
		return [t1,t2]
		
#Represents the block of properties inside a rule and/or a selector
def p_properties_block(t):
	'''properties_block : properties_block property
						| property'''

	if(len(t)==3):
		#Because of the left recursivity the list is returned reversed.
		if(t[1]!=None):
			t[2]=add(t[1],t[2])
		t[0]=t[2]
	else:
		t[0]=t[1]

#Represents a CSS property.
def p_property(t):
	'''property : STRING COLON STRING SEMICOLON
				| STRING COLON constant_name SEMICOLON'''
	t[0]=[[t[1],t[3]]]

#Represents the calling of a rule.
def p_rule_property(t):
	'property : AT STRING'
	try:
		t[0]=list(directionable_rules[t[2]])
	except KeyError as e:
		console("Error: Rule"+e+"not defined.")
		
#Error handling function.
def p_error(t):
	console("error:"+str(t))

#Funtion to print to the console
def console(msg):
	print msg

#Funtion to print a lexical token to the console.
def tokenConsole(name,t):
	if(DEBUG):
		console(name+":"+str(list(t)))


##################################################LOGGER
logging.basicConfig(
	level=logging.DEBUG,
	filename="log.txt",
	filemode="w",
	format="%(filename)10s:%(lineno)4d:%(message)s"
)
log=logging.getLogger()
##################################################END LOGGER
def printState():
	console("\t\tCONSTANTS")
	console(constants)
	console("\t\tPLAIN RULES")
	console(plain_rules)
	console("\t\tDIRECTIONABLE RULES")
	console(directionable_rules)
	console("\n\n\n")

#############################################CSS WRITING
def css(data):
	out=""
	for a in data:
		out+=str(a[0])+"{\n"
		if(a[1]!=None):
			for b in a[1]:
				out+="\t"+b[0]+":"+b[1]+";\n"
		out+="}\n"
	return out
			
##############################################STANDALONE CAPABILITIES
def parse(line):
	return yacc.yacc().parse(line,debug=log)	

if __name__=='__main__':
	archive=open(sys.argv[1],'r')
	data=archive.read()
	data=parse(data)
	if(DEBUG):
		printState()
	data=css(data)
	archive.close()
	archive=open(sys.argv[2],'w')
	archive.write(data)
