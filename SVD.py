import numpy

#with SVD we decompose in U sigma and V
#sigma is the matrix and his diagonal si called singular values of original matrix T
#the diagonal of sigma is a vector, order by magnitude and we care only about k major values
#this teqnique is called also LSA(Latent Semantic Analysis) or LSI(Latent Semnatic Indexing)

m = 3 #terms
n = 100 #documents

T = numpy.zeros ((m,n))

#scan all docs and decide for e.g. if is about "Java island" or "Java programming"
for j in range(m):
	T[0, j] = numpy.random.random()
	T[1, j] = numpy.random.random() * .1
	T[2, j] = numpy.random.random() * .1  
	if numpy.random.random() <.5:   #if means java programming and else means java island
		T[1, j] += T[0, j]
	else:
		T[0, j] *= .5
		T[2, j] += T[0, j]


#calculate vector of eans value for each row
means = [numpy.mean(row) for row in T]

for row, mu in zip (T, means): #zip create a list of pair
	row -= mu

#calculate covariance of T
#COV = T.dot (T.T)   #first T is the name of the matrix and the second T is for transopose

#Singular Value Decomposition  
#U matrix (m x m)
#s vector of the sigma value
#V already transposed (m x n)
U, s, V = numpy.linalg.svd(T, full_matrices = False)
#T in R^(mxn) -> T= U * Sigma * V.T  -> choose k << m -> Uk 0 (u1,...,uk), sigma = diag(o1,...,ok), Vk = (v1,...,vk)
#remeber that every u1..uk and v1..vk are vectors!!!
#with the new truncated matrix (k isntead of m) can evaluate the similarity of the query with my docs
#q in R^(k) -> qk = Uk.T * q -> simk = Vk * sigmak *qk   (q, qk and simk are vectors)

print U
print s