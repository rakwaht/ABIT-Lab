#! /usr/bin/python
#
# Usage:
# python search_engine.py seed_URL n_pages [optional fraction of terms to use]
#
# Example:
# python search_engine.py http://en.wikipedia.org/wiki/Business_intelligence 100 .95

import sys
import random

import crawler
import parser
import indexing
import TFIDF
import jaccard

#############################################################

seed = sys.argv[1]
n_pages = int(sys.argv[2])
term_fraction = None if len(sys.argv) < 4 else float(sys.argv[3])

print 'Downloading and indexing documents'
direct_index = indexing.get_index (crawler.recursive_download (seed, n_pages))
print len(direct_index), ' documents downloaded.'
print 'Now computing the inverted index'
inverted_index = indexing.invert_index (direct_index)
print len(inverted_index), 'terms indexed.'

# For convenience, remember the number of terms and documents
n_documents = len(direct_index)
n_terms = max(t['termid'] for t in inverted_index.values()) + 1

# Compute the optional IDF threshold
idf_threshold = None if not term_fraction else indexing.IDF_threshold (inverted_index, term_fraction)
if idf_threshold:
	print "IDF threshold set at", idf_threshold

#############################################################

# Display the contents of the index, term by term
'''
for t, l in inverted_index.items():
	# Write it
	sys.stdout.write ('Term: %s, ID: %d, IDF: %.5f\n'
				% (t, l['termid'], l['idf']))
	# Dor all documents appearing in the inverted index
	for d, c, tf in l['occurrences']:
		# write the document triplet
		sys.stdout.write ('\tDoc ID: %03d, # occurrences: %5d, TF: %.8f\n'
				% (d, c, tf))
exit()
'''
##############################################################

print 'Computing TFIDF representations of documents in the corpus'
TFIDFs = TFIDF.compute_all_TFIDFs (inverted_index, idf_threshold)

# Print all cosine similarities between documents
'''
similarities = [[TFIDF.cosine_similarity(d1,d2) for d2 in TFIDFs] for d1 in TFIDFs]
print similarities
exit()
'''

# Given a query, compute its TFIDF representation
print 'Computing query\'s TFIDF representation'

query = 'business became meaningful'
query_terms = parser.extract_terms (query)
q_TFIDF = TFIDF.compute_new_TFIDF (query_terms, inverted_index, idf_threshold)

# Warn if the query is empty due to a high IDF threshold
if len(q_TFIDF) == 0:
	print '*** WARNING *** Empty query, IDf threshold too high'

'''
print q_TFIDF
exit()
'''

######################################################################

print 'Computing set representations of documents in the corpus'
sets = jaccard.compute_all_sets (inverted_index, idf_threshold)

# Print all jaccard similarities between documents
similarities = [[jaccard.jaccard_coefficient(d1,d2) for d2 in sets] for d1 in sets]
'''
print similarities
exit()
'''

# Compute the query's set representation
print 'Computing query\'s set representation'
q_set = jaccard.compute_new_set (query_terms, inverted_index, idf_threshold)

'''
print q_set
exit()
'''

print 'Computing document ranking based on increasing Euclidean distance from query in TFIDF space'
euclidean_ranking = [(i, TFIDF.Euclidean_distance (q_TFIDF, TFIDFs[i])) for i in range(n_documents)]
euclidean_ranking.sort (key = lambda t: t[1])

print 'Computing document ranking based on decreasing cosine similarity with query in TDIDF space'
cosine_ranking = [(i, TFIDF.cosine_similarity (q_TFIDF, TFIDFs[i])) for i in range(n_documents)]
cosine_ranking.sort (key = lambda t: t[1], reverse = True)

print 'Computing document ranking based on decreasing Jaccard coefficient with query'
jaccard_ranking = [(i, jaccard.jaccard_coefficient (q_set, sets[i])) for i in range(n_documents)]
jaccard_ranking.sort (key = lambda t: t[1], reverse = True)

print 'Resulting top rankings:\nEuclidean\t\tCosine\t\t\tJaccard'
for i in range(10):
	print '%d\t%f\t%d\t%f\t%d\t%f' % (
		euclidean_ranking[i][0],
		euclidean_ranking[i][1],
		cosine_ranking[i][0],
		cosine_ranking[i][1],
		jaccard_ranking[i][0],
		jaccard_ranking[i][1])

'''
#calculate inverted index of given ranking
def invert_ranking (rk):
    return [[docid for docid,key in rk].index(i)
            for i in range(n_documents)]

euclidean_inverse_ranking = invert_ranking (euclidean_ranking)
cosine_inverse_ranking = invert_ranking (cosine_ranking)
jaccard_inverse_ranking = invert_ranking (jaccard_ranking)


#print in a file caluculated inverted index
f = open ('ranking.txt','w')
for docid in range(n_documents):
    f.write ('%d\t%d\t%d\t%d\n' % (
                docid,
                euclidean_inverse_ranking[docid],
                cosine_inverse_ranking[docid],
                jaccard_inverse_ranking[docid]
            ))
f.close()
'''

#estimate jaccard coeficients with permutation and probability
n_perm = 20
P = [range(n_terms) for i in range(n_perm)]
#create n_perm random permutation
for p in P:
    random.shuffle(p)

#create a list of all min for every doc
minima = [
          [min (p[termid] for termid in s) for p in P]
          for s in sets
        ]

#count the equality of permutation for 2 files
def count_equalities (a, b):
    c=0
    for i in range(len(a)):
        if a[i] == b[i]:
            c += 1
    return c

'''
#estimate jaccard with probability by count equalitisi in minma divided by total attempt
#for every pair of docs
jaccard_estimate = [
    [
                    float(count_equalities(m1, m2))/n_perm for m2 in minima
     ]
     for m1 in minima
]

#compare jaccard_estimate with jaccard_similarity in a file
#you con plot with gnuplot to understand
f = open("jaccard.txt", "w")
for i in range(n_documents):
    for j in range(n_documents):
        f.write('%f\t%f\n' % (similarities[i][j], jaccard_estimate[i][j]))
f.close()
'''

#for all perm i take the min for the query set (q_sset)
q_minima = [min (p[termid] for termid in q_set) for p in P]

approximate_jaccard_ranking = [[i, float(count_equalities(q_minima, minima[i]))/n_perm] for i in range(n_documents)]

jaccard_ranking.sort(key = lambda t: t[1], reverse = True)



#calculate inverted index of given ranking
def invert_ranking (rk):
    return [[docid for docid,key in rk].index(i)
            for i in range(len(rk))]

euclidean_inverse_ranking = invert_ranking (euclidean_ranking)
cosine_inverse_ranking = invert_ranking (cosine_ranking)
jaccard_inverse_ranking = invert_ranking (jaccard_ranking)
approximate_jaccard_inverse_ranking = invert_ranking (approximate_jaccard_ranking)



#print in a file caluculated inverted index
f = open ('ranking.txt','w')
for docid in range(n_documents):
    f.write ('%d\t%d\t%d\t%d\t%d\n' % (
                                   docid,
                                   euclidean_inverse_ranking[docid],
                                   cosine_inverse_ranking[docid],
                                   jaccard_inverse_ranking[docid],
                                   approximate_jaccard_inverse_ranking[docid]
                                   ))
f.close()

