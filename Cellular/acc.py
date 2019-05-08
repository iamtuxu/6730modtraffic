import numpy as np
from var import *
import time
import matplotlib.pyplot as plt


class map(object):
	def __init__(self, input_arr):
		self.cellmap = input_arr
		self.max_y = len(input_arr)
		self.max_x = len(input_arr[0])
		self.systime = 0
		self.spawncount = 0
		self.exitcount = 0

	def put_car(self, coordy, coordx, carcomm, cardelay, cardir):
		self.cellmap[coordy][coordx].add_car(car(carcomm, cardelay, cardir))

	def update(self):
		self.systime += 1
		ref_cellmap = self.construct_ref()
		# set all cars unmoved.
		for y in range(self.max_y):
			for x in range(self.max_x):
				cell = self.cellmap[y][x]
				if cell != X:  # is a road
					if cell.car:  # has a car
						cell.car.moved = False

		for y in range(self.max_y):
			for x in range(self.max_x):
				cell = self.cellmap[y][x]
				if cell != X:  # is a road
					if cell.car:  # has a car, hasn't moved
						if cell.car.moved:
							continue
						cell.car.moved = True
						if cell.dir[cell.car.comm] == None:  # can not execute turn
							ny = y + cell.dir[cell.car.direction][0]
							nx = x + cell.dir[cell.car.direction][1]
						else:
							ny = y + cell.dir[cell.car.comm][0]
							nx = x + cell.dir[cell.car.comm][1]
						if nx < 0 or nx > self.max_x - 1 or ny < 0 or ny > self.max_y - 1:
							# go out of map
							cell.pop_car()
							self.exitcount += 1
						else:
							next_cell = self.cellmap[ny][nx]
							ref_next_cell = ref_cellmap[ny][nx]

							if ref_next_cell == 0:
								if cell.trafficlight:
									if cell.trafficlight_stat == True:
										move_car = cell.pop_car()
										next_cell.add_car(move_car)
								else:
									move_car = cell.pop_car()
									next_cell.add_car(move_car)

					if cell.spawn != None:  # is a spawn point
						if cell.spawncounter != 0:  # not yet the time
							cell.spawncounter -= 1
						else:  # it's the time
							refmap_spawn = self.construct_ref()
							if refmap_spawn[y][x] == 0:
								cell.spawncounter = cell.spawn
								spawncomm = np.random.choice(['L', 'R', 'D'], 1, p=[cell.Lrate, cell.Rrate, cell.Drate])
								self.put_car(y, x, spawncomm, 0, cell.spawndir)
								self.spawncount += 1

					if cell.trafficlight:
						#change state:
						if cell.trafficlight_counter != 0:
							cell.trafficlight_counter -= 1
						else:
							if cell.trafficlight_stat == True:
								cell.trafficlight_stat = False
								cell.trafficlight_counter = cell.trafficlight_stop_period
							else:
								cell.trafficlight_stat = True
								cell.trafficlight_counter = cell.trafficlight_go_period





	def construct_ref(self):
		ref_cellmap = []
		for item in self.cellmap:
			ref_cellmap.append(item.copy())
		for y in range(self.max_y):
			for x in range(self.max_x):
				cell = self.cellmap[y][x]
				if cell != X:  # is a road
					if cell.car == None:
						ref_cellmap[y][x] = 0
					else:
						ref_cellmap[y][x] = 1
		return ref_cellmap

	def update_and_plot(self, n_iter):

		# plt.ion()
		plt.ion()
		for _ in range(n_iter):
			self.update()
			plot_cellmap = np.zeros((self.max_y, self.max_x))
			for y in range(self.max_y):
				for x in range(self.max_x):
					cell = self.cellmap[y][x]
					if cell != X:  # is a road
						if cell.car:  # has a car
							plot_cellmap[y, x] = 2
						else:
							plot_cellmap[y, x] = 1

			plt.title('Iter :{}'.format(self.systime))
			plt.imshow(plot_cellmap)
			plt.pause(0.2)
		plt.ioff()

	def plot(self):
		plot_cellmap = np.zeros((self.max_y, self.max_x))
		for y in range(self.max_y):
			for x in range(self.max_x):
				cell = self.cellmap[y][x]
				if cell != X:  # is a road
					if cell.car:  # has a car
						plot_cellmap[y, x] = 2
					else:
						plot_cellmap[y, x] = 1
		plt.imshow(plot_cellmap)
		plt.show()


	def __str__(self):
		out = ''
		for row in self.cellmap:
			for item in row:
				out += '	'
				out += str(item)
			out += '\n'
		return out


class road(object):
	def __init__(self, dir, spawnint=None, spawndir=None, spawndelay=0, trafficlight=None, trafficlight_stop=0, trafficlightinit = True):
		self.car = None
		self.dir = dir

		self.spawn = spawnint
		if spawnint != None:
			self.spawncounter = spawndelay
			self.Lrate = 0.1
			self.Rrate = 0.1
			self.Drate = 0.8
			self.spawndir = spawndir

		self.trafficlight = trafficlight


		if trafficlight:
			self.trafficlight_stat = trafficlightinit
			self.trafficlight_go_period = trafficlight
			self.trafficlight_stop_period = trafficlight_stop
			self.trafficlight_counter = trafficlight

	def add_car(self, car):
		self.car = car

	def pop_car(self):
		out = self.car
		self.car = None
		return out

	def __str__(self):
		if self.car == None:
			return 'N'
		else:
			return str(self.car.comm)


class car(object):
	def __init__(self, comm, delay, direction):
		self.direction = direction
		if comm == 'L':
			self.comm = (direction - 1) % 4
		if comm == 'R':
			self.comm = (direction + 1) % 4
		elif comm == 'D':
			self.comm = direction
		self.delay = delay
		self.moved = False

	def __str__(self):
		return '1'


# dy,dx
if __name__ == '__main__':
	from var import *
	input_map = [[X, X, road(N), X, X],
				 [X, X, road(N), X, X],
				 [road(W), road(W), road(NW), X, X],
				 [X, X, road(N), X, X],
				 [X, X, road(N, 2, 0), X, X]]

	input_map = [[X, X, X, road(S, 1, 2, spawndelay=4), road(N), X, X, X],
				 [X, X, X, road(S), road(N), X, X, X],
				 [X, X, X, road(S), road(N), X, X, X],
				 [road(W), road(W), road(W), road(SW), road(NW), road(W), road(W), road(W, 1, 3)],
				 [road(E, 1, 1), road(E), road(E), road(SE), road(NE), road(E), road(E), road(E)],
				 [X, X, X, road(S), road(N), X, X, X],
				 [X, X, X, road(S), road(N), X, X, X],
				 [X, X, X, road(S), road(N, 1, 0), X, X, X]
				 ]

	# input_map = [[X, X, X, road(S, 0, 2), road(N), X, X, X],
	# 			 [X, X, X, road(S), road(N), X, X, X],
	# 			 [X, X, X, road(S,trafficlight=10,trafficlight_stop=10,trafficlightinit=True), road(N), X, X, X],
	# 			 [road(W), road(W), road(W), road(SW), road(NW), road(W,trafficlight=10,trafficlight_stop=10,trafficlightinit=False), road(W), road(W, 0, 3)],
	# 			 [road(E, 0, 1), road(E), road(E,trafficlight=10,trafficlight_stop=10,trafficlightinit=False), road(SE), road(NE), road(E), road(E), road(E)],
	# 			 [X, X, X, road(S), road(N,trafficlight=10,trafficlight_stop=10,trafficlightinit=True), X, X, X],
	# 			 [X, X, X, road(S), road(N), X, X, X],
	# 			 [X, X, X, road(S), road(N, 0, 0), X, X, X]
	# 			 ]

	input_map = [[X, X, X, road(S,0,2), road(N), X, X, X],
				 [X, X, road(S), road(SW), road(N), X, X, X],
				 [X, X, road(S), road(S, trafficlight=10, trafficlight_stop=10, trafficlightinit=True), road(N), road(W), road(W), X],
				 [road(W), road(W), road(W), road(SW), road(NW),road(W, trafficlight=10, trafficlight_stop=10, trafficlightinit=False), road(NW), road(W,1,3)],
				 [road(E,1,1), road(SE), road(E, trafficlight=10, trafficlight_stop=10, trafficlightinit=False),road(SE), road(NE), road(E), road(E), road(E)],
				 [X, road(E), road(E), road(S), road(N, trafficlight=10, trafficlight_stop=10, trafficlightinit=True), road(N), X, X],
				 [X, X, X, road(S), road(NE), road(N), X, X],
				 [X, X, X, road(S), road(N, 0, 0), X, X, X]
				 ]




	game = map(input_map)
	# game.update_and_plot(50) # How many iters you want to stimulate


for x in range(50):
	game.update()
	print(game)
	time.sleep(0.2)
# while True:
# 		game.update()
# 		print(game)
#
# 		time.sleep(0.5)
