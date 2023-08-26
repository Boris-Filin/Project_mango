from Wall import Wall
from Segment import Segment
from Vector2 import Vector2
import math
import random

def prime_screen(screen_size):
	w = screen_size.x
	h = screen_size.y

	screen = []
	for y in range(h):
		screen.append([])
		for x in range(w):
			screen[y].append(False)

	return screen

def fill_screen(screen, screen_size, points):
	w = screen_size.x
	h = screen_size.y

	# add points to the screen
	for point in points:
		if point.x < w and point.y < h and point.x >= 0 and point.y >= 0:
			screen[point.y][point.x] = True

def display_screen(screen, screen_size):
	w = screen_size.x
	h = screen_size.y

	# ▄▀ █
	for y_iter in range(math.ceil(h / 2)):
		for x in range(w):
			y = math.ceil(h / 2) - y_iter - 1
			upper_fill = screen[y * 2 + 1][x]
			lower_fill = screen[y * 2][x]

			if upper_fill and lower_fill:
				print("█", end='')
			elif upper_fill:
				print("▀", end='')
			elif lower_fill:
				print("▄", end='')
			else:
				print(".", end='')
		print()

points = []
screen_size = Vector2(100, 100)
for i in range(10):
	# x1 = random.random() * screen_size.x
	# y1 = random.random() * screen_size.y
	# x2 = random.random() * screen_size.x
	# y2 = random.random() * screen_size.y
	x1 = 10.1
	y1 = 10.1
	x2 = 10.2
	y2 = 10.2
	# print(int(x1), int(y1), int(x2), int(y2))
	
	wall = Wall(Segment(Vector2(x1, y1), Vector2(x2, y2)))
	new_points = wall.calculate_chunks(2)
	for point in new_points:
		point_vector = Vector2(point[0], point[1])
		if not point_vector in points:
			points.append(point_vector)

screen = prime_screen(screen_size)
fill_screen(screen, screen_size, points)
display_screen(screen, screen_size)
