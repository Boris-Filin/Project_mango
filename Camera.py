import math
from Vector2 import Vector2
from Segment import Segment
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
				self.screen[y].append(" ")
				
	def send_screen(self):
		return self.screen
				
	def update_objects(self, objects):
		self.objects = objects
			
	def update(self):
		gradient = "█" * 2 + "▓" * 3 + "▒" * 3 + "░" * 3 +" "
		# floor = "░"
		render_distance = 8

		iter_ang = self.fov.x / self.screen_size.x
		
		for x in range(self.screen_size.x):
			
			current_angle = self.rotation - iter_ang * x + self.fov.x / 2
			direction = Vector2.polar_to_cartesian(render_distance, current_angle.rad)
			ray = Segment(self.pos, self.pos + direction)

			dist = render_distance + 1

			for object_ in self.objects:
				if ray.intersects(object_):
					new_dist = ray.count_intersection(object_) - self.pos
					if new_dist != None:
						dist = min(new_dist.magnitude, dist)

			if dist <= render_distance:

				pix_u = int(self.screen_size.y * self.du0 / dist)
				pix_d = int(self.screen_size.y * self.dd0 / dist)

				fac = math.floor(dist / render_distance * (len(gradient) - 1))
				char_ = gradient[fac]

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
						# if y >= self.screen_size.y * 0.61:
						# 	self.screen[y][x] = floor
			else:
				for y in range(self.screen_size.y):
					self.screen[y][x] = gradient[-1]
					# if y >= self.screen_size.y * 0.61:
					# 	self.screen[y][x] = floor

	def displace(self, direction):
		move = Segment(self.pos, self.pos + direction)
		intersection = False
		for object_ in self.objects:
			if object_.intersects(move):
				intersection = True
		if not intersection:
			self.pos += direction
		return not intersection

	def move(self, magnitude, precision=5):
		direction = Vector2.polar_to_cartesian(magnitude / precision, self.rotation.rad)
		for i in range(precision):
			if not self.displace(direction):
				break