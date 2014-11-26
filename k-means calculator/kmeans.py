#! /usr/bin/python

#k-means clustering is a method of vector quantization, 
#originally from signal processing, that is popular for cluster
#analysis in data mining. k-means clustering aims to partition n 
#observations into k clusters in which each observation belongs 
#to the cluster with the nearest mean, serving as a 
#prototype of the cluster. 

#INSTRUCTION
#
#RUN:
#"python kmeans.py"
#view output with "less clustering%something%" with i numerber between the range of iteration
#in %something" wtire _NumberOfCluster_IterationNumber
#
#VIEW RESULT WITH GNUPLOT
#gnuplot %one_name_of_the_file_with_cmd_extension%
#e.g "gnuplot clustering_003_009.cmd"
#
#ERROR PLOT
#run: python kmeans.py > error
#open gnuplot
#run: plot "error" w l

import random
import math



dimensions = 2
clouds = 5
centers = [[random.uniform(-1.0, 1.0) for j in range(dimensions)] for c in range(clouds)]

#sigma parameter control the spread of each cluster
sigma = .1
#number of cluster
K_max= 5
#numer of points
n = 1000

#function that given a point and a list of prototype give as output the index of the closest
#prototype for this point and also the corresponding distance
def closest_prototype_index(point, mu):
	#intial min distance = huge number
	min_distance = 1.0e30
	min_c = 1.0e30
	for c in range(len(mu)):
		dist = 0.0
		for i in range(len(point)):
			d = point[i] - mu[c][i]
			dist += d * d
		if dist < min_distance:
			min_distance = dist
			min_c = c
	return min_c, min_distance




#create random points
m = len(centers[0])
points = []
for i in range(n):
	c = random.randint(0, len(centers) - 1)
	points.append ([random.gauss (centers[c][j], sigma) for j in range(m)])


#print '\n'.join('\t'.join(str(v) for v in point) for point in points)

for K in range(1, K_max+1):

	cluster = [random.randint(0, K-1) for i in range(n)]

	#foreach iteration we raise our centroid sepration
	for iteration in range(10):
		#i need K vector mu(prototype mu == mean) of length 
		mu = [[0.0]*m for i in range(K)]

		#count how many points belonges foreach cluster
		count = [0] * K

		#take every point and assign it to the prototype
		for i in range(n):
			c = cluster[i]
			point = points[i]
			for j in range(m):
				mu[c][j] += point[j]
			count[c] += 1

		#for all cluster and for all coordinates we normalize the prototype
		for c in range(K):
			for j in range(m):
				if count[c]:
					mu[c][j] /= count[c]

		#write result in a file to plot (concat iteration)
		f = open("clustering_%03d_%03d" % (K,iteration), "w")
		#foreach point write cluster and coordinates
		for i in range(n):
			f.write ("c%d %s\n" % (cluster[i], ' '.join(str(v) for v in points[i])));
		#scac cluster index
		for c in range(K):
			f.write("p%d %s\n" % (c, ' '.join(str(v) for v in mu[c])))
		f.close()

		#create command file for gnuplot
		f = open("clustering_%03d_%03d.cmd" % (K,iteration), "w")
		f.write("plot "
			 + ','.join('"<grep c%d clustering_%03d_%03d" using 2:3 title "Cluster %d"' 
			 	% (c, K, iteration,c) for c in range(K))
			 + ','
			 + ','.join('"<grep p%d clustering_%03d_%03d" using 2:3 title "Prototype %d"'
			    % (c, K, iteration, c) for c in range(K))
		)

		f.close()

		cluster = [closest_prototype_index(point, mu)[0] for point in points]
	
	#foreach number of K we try to compute the errors and print it
	E = 0.0
	for point in points:
		E += closest_prototype_index(point, mu)[1]
	print "%d %f" % (K, math.sqrt(E/n))


