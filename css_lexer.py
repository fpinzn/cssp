#!/usr/bin/python
# ------------------------------------------------------------
# CSSP: CSS Preprocessor (bitremix.com/p/cssp)
# Ver: 0.0.1
# Copyright 2010 Francisco Pinzon: (pacho@bitremix.com)
# ------------------------------------------------------------
#
#css_lexer.py
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
import ply.lex as lex

# List of token names that reserved words.
tokens=[
	'COMMENT',
	'DOLLAR',
	'AT',
	'EQUALS',
	'RCURL',
	'LCURL',
	'COLON',
	'SEMICOLON',
	'STRING'
]

#List of ignored characters
t_ignore = ' \t\r'

#Token value assignation
t_LCURL=r'\{'
t_RCURL=r'\}'
t_EQUALS=r'='
t_DOLLAR=r'[$]'
t_AT=r'@'
t_COLON=r':'
t_SEMICOLON=r';'
t_STRING='([A-Za-z0-9 ]|[,_>.#"%()!*]|[-]|\'|[[]|[]])+'

#Comment handling rule
def t_COMMENT(t):
	r'/\*(.|\n)*?[*]/'
	pass

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# NewLine handling rule
def t_newline(t):
	r'\n+'
	t.lexer.lineno+=t.value.count("\n")

lexer=lex.lex();


###############################STANDALONE CAPABILITIES
def lex_line(line):
	lexer.input(line)
	while True:
		tok=lexer.token()
		if not tok:break
		print tok
		
if __name__=='__main__':
	print '\t\tCSS LEXER'
	while True:
		lex_line(raw_input("css_lexer>"))
