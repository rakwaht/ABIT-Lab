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
#open *.png and slide down to view the changes
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
import subprocess


dimensions = 2
clouds = 5
#centers = [[random.uniform(-1.0, 1.0) for j in range(dimensions)] for c in range(clouds)]
centers = [
	[1.0, -1.0],
	[-1.0, 1.0],
	[1.0, 1.0],
	[-1.0, -1.0]
]
#sigma parameter control the spread of each cluster
sigma = .4
#numer of points
n = 1000
#costant for the push of the prototype 
eta = .5
#we use matrix ETA to describe correlation between the prototypes
#ETA[i,j] == 1 if i == j
#ETA[i,j] == 0.5 if i is correlated to j
#ETA[i,j] == 0 if i doesn't have relationship with j
ETA = [
	[1.0, 0.5, 0.5, 0.0],
	[0.5, 1.0, 0.0, 0.5],
	[0.5, 0.0, 1.0, 0.0],
	[0.0, 0.5, 0.5, 1.0]
]

#number of prototype (exactly the number of ETA column / rows)
K = 4


#function that given a point and a list of prototype give as output the index of the closest
#prototype for this point and also the corresponding square of its distance
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
#reperat the clustering procedure K_max times (inclusive)
mu = []
for j in range(K):
	i = random.randint(0, n-1)
	mu.append(list(points[i]))

for iteration in range(1000):
	#select random point in dataset
	i = random.randint(0, n-1)
	#find index of th closest prototype with the function
	point = points[i]
	c = closest_prototype_index(point, mu)[0]
	#
	for c1 in range(K):
		#foreach coordinates in my point move them towards the selected point
		#based on constant and ETA that is the correlation matrix
		for j in range(m):
			mu[c][j] += eta * ETA[c][c1] * (point[j] - mu[c][j])

	if iteration % 10 == 0:
		#output result in a file to plot (concat iteration)
		f = open("clustering", "w")
		#foreach point write cluster and coordinates
		for i in range(n):
			f.write ("c%d %s\n" % (closest_prototype_index(points[i], mu)[0], ' '.join(str(v) for v in points[i])));
		#scac cluster index
		for c in range(K):
			f.write("p%d %s\n" % (c, ' '.join(str(v) for v in mu[c])))
		f.close()

		#write a file with the pair of every point correlated (based on ETA)
		f = open('lines', 'w')
		for i in range(K):
			for j in range(i):
				if ETA[i][j] > 0.0:
					f.write ('%f %f\n%f %f\n\n' % (mu[i][0], mu[i][1], mu[j][0], mu[j][1]))
		f.close()

		#create command file for gnuplot
		f = open("clustering.cmd", "w")
		f.write("set term png\nset output \"%03d.png\"\nplot " % iteration
			 + ','.join('"<grep c%d clustering" using 2:3 title "Cluster %d"' 
			 	% (c, c) for c in range(K))
			 + ','
			 + ','.join('"<grep p%d clustering" using 2:3 title "Prototype %d" ps 10'
			    % (c, c) for c in range(K))
			 + ', "lines" with lines linetype 1'
		)

		f.close()
		#call gnuplot with parameter our file
		subprocess.call(['gnuplot', 'clustering.cmd'])
		#cluster = [closest_prototype_index(point, mu)[0] for point in points]

#at the end of clustering procedure compute the quantization error
E = 0.0
for point in points:
	E += closest_prototype_index(point, mu)[1]
print "%d %f" % (K, math.sqrt(E/n))


