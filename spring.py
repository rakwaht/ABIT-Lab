import Tkinter
import numpy
import numpy.linalg
import math

#########################
#Simulate the points that move like if they are connected
#with springs.
#########################

WIDTH = 500
HEIGHT = 500
K = 1
dT = 1.0e-2
eta = 0.99

#matrix of ideal distance
# d = [
# 	[0.0, 1.0, 1.0, 1.0],
# 	[1.0, 0.0, 1.0, 1.0],
# 	[1.0, 1.0, 0.0, 1.0],
# 	[1.0, 1.0, 1.0, 0.0]
# ]

#n = len(d)

rows = 4
cols = 4
n = rows * cols
d =[[None] * n for i in range(n)]
for i in range(n):
	for j in range(i):
		ri = i / cols
		ci = i % cols
		rj = j / cols
		cj = j % cols
		dr = ri - rj
		dc = ci - cj
		#calculate ideal distance 
		dij = math.sqrt(dr*dr + dc*dc)
		#moltiply with .25 to keep close
		d[i][j] = dij * 0.25
		#set in the distance matrix .25 if two cells are neighbours, remains None otherwise
		# if (ri == rj and (ci == cj-1 or ci == cj+1)) or (ci == cj and (ri == rj+1 or ri == rj-1)):
		# 	d[i][j] = .25

root = Tkinter.Tk()
canvas = Tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

circles = [canvas.create_oval(0, 0, 0, 0, fill='#ff0000') for i in range(n)]

x = numpy.random.uniform(-.5, .5, (n,2))
v = numpy.zeros((n, 2))

def animate ():
	global circles, x, v, canvas, root
	F = numpy.zeros((n, 2))
	E = 0.0
	for i in range(n):
		for j in range(i):
			xi = x[i]
			xj = x[j]
			#eucliadian distance between i and j
			dij = numpy.linalg.norm(xi - xj) 
			#d[i][j] = desired distance
			diff = dij - d[i][j]
			fij = K * diff
			#calculate force vector that pull my points
			#F[i] pull and so F[j] push in the other way same amount
			Fij = fij * (xj - xi) / dij
			F[i] += Fij
			F[j] -= Fij
			#potential energy of the spring
			E += .5 * K * diff * diff
	for i in range(n):
		#speed to animate: (F = m*a) => a = F / m and we suppose m = 1
		#then v = a * t
		#v[i] * eta is the viscouse coeficent that brake our move
		#so the velecoty arrives to 0 and points get balance state
		v[i] = v[i] * eta + F[i] * dT
		x[i] += v[i] * dT
		xx = (x[i, 0] + 1.0) * .5 * WIDTH
		yy = (x[i, 1] + 1.0) * 0.5 * HEIGHT
		canvas.coords(circles[i], xx-5, yy-5, xx+5, yy+5)
	print E
	root.after(1, animate)

root.after(10, animate)

root.mainloop()