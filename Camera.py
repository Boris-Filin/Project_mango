import math
from Tools import Vector2, Segment, Ray
from Angle import Angle


class Camera():
	def __init__(self, pos=Vector2(), rotation=Angle(),
		screen_size=Vector2(200, 55), fov=Vector2(120, 80), **kwargs):
			self.pos = pos.cast()
			self.rotation = rotation
			self.fov = fov
			self.screen_size = screen_size.cast()
			self.screen = []
			self.objects = []
			self.initialize_screen()
			self.update()
			self.player_height = 1.5 if not "player_height" in kwargs else kwargs["player_height"]
			self.wall_height = 2.5 if  not "wall_height" in kwargs else kwargs["wall_height"]

			self.du0 = (self.wall_height - self.player_height) / math.tan(math.radians(self.fov.y / 2))
			self.dd0 = self.player_height / math.tan(math.radians(self.fov.y / 2))

	def initialize_screen(self):
		for y in range(self.screen_size.y):
			self.screen.append([])
			for x in range(self.screen_size.x):
				# self.screen[y] = " " * self.screen_size.x
				self.screen[y].append(" ")
				
	def send_screen(self):
		return self.screen
				
	def update_objects(self, objects):
		self.objects = objects
			
	def update(self):
		gradient = "█▓▒░ "

		render_distance = 8
		iter_ang = self.fov.x / self.screen_size.x
		for x in range(self.screen_size.x):
			current_angle = self.rotation - iter_ang * x + self.fov.x / 2
			direction = Vector2.polar_to_cartesian(0.1, current_angle.rad)
			ray = Ray(self.pos, direction)

			dist = render_distance + 1

			for object_ in self.objects:
				if ray.intersects(object_):
					new_dist = ray.count_intersection(object_)
					if new_dist != None:
						dist = min(new_dist.magnitude, dist)
			if dist > render_distance:
				brightness = None
			else:
				brightness = (render_distance - dist) / 2

			if brightness and brightness >= 0:

				ru = self.du0 / dist
				rd = self.dd0 / dist

				pix_u = int(self.screen_size.y * ru)
				pix_d = int(self.screen_size.y * rd)

				if brightness >= 4:
					char_ = gradient[0]
				elif brightness >= 0:
					fac = math.floor((4 - brightness) / 4 * (len(gradient) - 1))
					char_ = gradient[fac]
				else:
					char_ = gradient[-1]

				slabbed_u = pix_u % 2
				slabbed_d = pix_d % 2

				min_ = max(int(self.screen_size.y / 2) - pix_u // 2 + 1, 0)
				max_ = min(int(self.screen_size.y / 2) + pix_d // 2, self.screen_size.y)

				for y in range(self.screen_size.y):
					if y >= min_ and y <= max_:
						self.screen[y][x] = char_
					elif y == min_ - 1 and slabbed_u:
						self.screen[y][x] = "▄"
					elif y == max_ + 1 and slabbed_d:
						self.screen[y][x] = "▀"
					else:
						self.screen[y][x] = gradient[-1]
			else:
				for y in range(self.screen_size.y):
					self.screen[y][x] = gradient[-1]

	def displace(self, direction):
		move = Segment(self.pos, self.pos + direction)
		intersection = False
		for object_ in self.objects:
			if object_.intersects(move):
				intersection = True
		if not intersection:
			self.pos += direction
		return not intersection

	def move(self, magnitude, precision=10):
		direction = Vector2.polar_to_cartesian(magnitude / precision, self.rotation.rad)
		for i in range(precision):
			if not self.displace(direction):
				break
		
	def test_print(self):
		for y in range(len(self.screen)):
			print(".", end='')
			for x in range(len(self.screen[0])):
				print(self.screen[y][x], end='')
			print(".")

