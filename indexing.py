#! /usr/bin/python
#
# Build a direct and an inverted index from the documents contained in a list
# (or, equivalently, yielded by an iterator)
#
# Test code: build the direct and inverted index of a set of downloaded documents
#
# Example:
# python indexing.py http://en.wikipedia.org/wiki/Business_intelligence 100

#############################################################

import math
import parser

# Create the direct index
def get_index (document_list):

	index = []
	# As long as there are unvisited URLs (and a maximum of MAX_VISITED downloads)
	for document in document_list:
		# Take terms from the text
		document['terms'] = parser.extract_terms(document['text'])
		# Now document text is not needed anymore
		del document['text']
		# The document ID is its position within the direct index
		docid = document['id'] = len(index)
		index.append (document)
	return index

# Return all terms with number of occurrences
def terms_with_count (terms):
	count = {}
	for term in terms:
		if term in count:
			count[term] += 1
		else:
			count[term] = 1
	return count

# Invert the direct index
def invert_index (direct_index):

	# inverted index of the document corpus.
	# The index maps each term to a list of triplets
	# (doc_index, occurrences, term_frequency)
	inverted_index = {}

	# As long as there are unvisited URLs and a maximum of MAX_VISITED downloads
	for document in direct_index:

		docid = document['id']
		terms = document['terms']

		count = terms_with_count (terms)

		# Add the temporary count to the global inverted index
		for t, c in count.items():
			tf = float(c)/len(terms)
			if t in inverted_index:
				inverted_index[t]['occurrences'].append ((docid, c, tf))
			else:
				inverted_index[t] = {
					# The document ID is its position within the inverted index
					'termid': len(inverted_index),
					'occurrences': [(docid, c, tf)]
				}

	# Now add the IDF of each term in its corresponding inverted index entry
	n_documents = float(len(direct_index))
	for t, l in inverted_index.items():
		# Compute the term's IDF
		idf = math.log (n_documents / len(l['occurrences']))
		if idf > 0:
			l['idf'] = idf
		else:
			# If IDF == 0, remove term from inverted index
			del inverted_index[t]

	return inverted_index

# Given an inverted index, compute the IDF threshold value such that a given fraction
# of terms is above that level
def IDF_threshold (inverted_index, term_fraction = .99):
	# Sort all IDFs by ascending value
	idf_list = sorted([l['idf'] for l in inverted_index.values()])
	# Find the appropriate position in the list
	threshold_index = int(len(idf_list)*(1-term_fraction))
	# Return the value in the sorted list
	return idf_list[threshold_index]

if __name__ == '__main__':

	import sys
	import crawler

	seed = sys.argv[1]
	n_pages = int(sys.argv[2])

	print 'Downloading and indexing documents...'
	direct_index = get_index (crawler.recursive_download (seed, n_pages))
	print len(direct_index), ' documents downloaded.'
	print 'Now computing the inverted index...'
	inverted_index = invert_index (direct_index)
	print len(inverted_index), 'terms indexed.'
	print '99% IDF threshold is', IDF_threshold (inverted_index, .99)
