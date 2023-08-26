import math
import random
from Vector2 import Vector2


# initiate screen
def prime_screen(screen_size):
	w = screen_size.x
	h = screen_size.y

	screen = []
	for y in range(h):
		screen.append([])
		for x in range(w):
			screen[y].append(False)

	return screen

def prime_screen(screen_size):
	w = screen_size.x
	h = screen_size.y

	screen = []
	for y in range(h):
		screen.append([])
		for x in range(w):
			screen[y].append(' ')

	return screen

# add details to the screen
def fill_screen(screen, screen_size, points, player_pos, player_angle):
	w = screen_size.x
	h = screen_size.y

	# add points to the screen
	for point in points:
		if point.x < w and point.y < h and point.x > 0 and point.y > 0:
			screen[point.y][point.x] = True

	# add player and player line of sight
	screen[player_pos.y][player_pos.x] = True
	for i in range(15):
		x = int(player_pos.x + i * math.sin(math.radians(player_angle)))
		y = int(player_pos.y + i * math.cos(math.radians(player_angle)))

def fill_screen2(screen, screen_size, points, player_pos, player_angle):
	w = screen_size.x
	h = screen_size.y

	center = Vector2(w // 2, h // 2)

	# add points to the screen
	for point in points:
		if point.x < w and point.y < h and point.x > 0 and point.y > 0:
			# val = Vector2(0, 1).dot(point - center)
			# val = Vector2(0, 1).cross(point - center)
			dir1 = Vector2(-2, 1)
			dir2 = Vector2(2, 1)
			val1 = dir1.cross(point - center) < 0
			val2 = dir2.cross(point - center) > 0
			val = val1 and val2

			if val:
				screen[point.y][point.x] = '+'
			else:
				screen[point.y][point.x] = ' '
			# if val < 0:
			# 	screen[point.y][point.x] = 'N'
			# elif val == 0:
			# 	screen[point.y][point.x] = '0'
			# else:
			# 	screen[point.y][point.x] = 'P'

	# add player and player line of sight
	screen[center.y][center.x] = 'X'

# display screen
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

def display_screen2(screen, screen_size):
	w = screen_size.x
	h = screen_size.y

	# ▄▀ █
	for y_iter in range(h):
		y = h - y_iter - 1
		for x in range(w):
			print(screen[y][x], end=' ')
		print()



def transform_point(point, player_pos, cosa, sina):
	x = point.x * cosa + point.y * sina - player_pos.x * cosa - player_pos.y * sina
	y = - point.x * sina + point.y * cosa + player_pos.x * sina - player_pos.y * cosa
	new_point = Vector2(int(x), int(y))
	return new_point

def test1():
	screen_size = Vector2(100, 100)

	points = []
	for i in range(15):
		points.append(Vector2(random.randint(0, 99), random.randint(0, 99)))

	player_pos = Vector2(15, 10)
	player_angle = 60

	screen = prime_screen(screen_size)
	fill_screen(screen, screen_size, points, player_pos, player_angle)
	display_screen(screen, screen_size)
	print('\n' * 5)

	new_points = []
	cosa = math.cos(math.radians(-player_angle))
	sina = math.sin(math.radians(-player_angle))

	for point in points:
		new_point = transform_point(point, player_pos, cosa, sina)
		new_points.append(new_point + Vector2(screen_size.x // 2))

	screen = prime_screen(screen_size)
	fill_screen(screen_size, new_points, Vector2(screen_size.x // 2, 0), 0)
	display_screen(screen, screen_size)


def test2():
	screen_size = Vector2(100, 100)

	points = []
	for i in range(5000):
		points.append(Vector2(random.randint(0, 99), random.randint(0, 99)))

	player_pos = Vector2(15, 10)
	player_angle = 60

	screen = prime_screen2(screen_size)
	fill_screen2(screen, screen_size, points, player_pos, player_angle)
	display_screen2(screen, screen_size)

test2()