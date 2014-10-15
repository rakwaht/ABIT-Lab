#! /usr/bin/python
#
# Parse the text of a web pag and extract a list of terms removing tags and punctuation.
#
# Test case: parse the script's standard input


# Remove HTML tags and punctuation, capitalize letters
def extract_terms (text):
	# Storage of all words in text
	words = []
	# Finite state machine, scanning all characters of text:
	# 0 = whitespace, 1 = word, 2 = tag
	state = 0
	for c in text:
		if state == 0:
			if c.isalpha() or c.isdigit() or c == '\'':
				word = ''
				state = 1
			elif c == '<':
				state = 2
		elif state == 1:
			if c == '<':
				state = 2
			elif not (c.isalpha() or c.isdigit() or c == '\''):
				state = 0
			if state != 1:
				words.append (word)
		else:
			if c == '>':
				state = 0
		if state == 1:
			word += c.upper()
	if state == 1:
		words.append (word)
	return words

if __name__ == '__main__':

	import sys
	import pprint

	pprint.pprint (extract_terms (sys.stdin.read()))
