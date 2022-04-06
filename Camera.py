import math
from Vector2 import Vector2
from Segment import Segment


class Camera():
	def __init__(self, runner, pos=Vector2(), rotation=0,
		screen_size=Vector2(200, 55), fov=Vector2(120, 80), **kwargs):

		self.runner = runner
		self.pos = pos.cast()
		self.rotation = rotation
		self.fov = fov

		self.screen_size = screen_size.cast()
		self.screen = []
		self.objects = []

		self.player_height = 1.5 if not "player_height" in kwargs else kwargs["player_height"]
		self.wall_height = 2.5 if  not "wall_height" in kwargs else kwargs["wall_height"]

		self.du0 = (self.wall_height - self.player_height) / math.tan(math.radians(self.fov.y / 2))
		self.dd0 = self.player_height / math.tan(math.radians(self.fov.y / 2))

		self.initialize_screen()
		self.update()

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
		# The depth gradient
		gradient = "█" * 2 + "▓" * 3 + "▒" * 3 + "░" * 3 +" "
		
		render_distance = 8

		iter_ang = self.fov.x / self.screen_size.x
		
		for x in range(self.screen_size.x):
			# Ray angle for every vertical strip on the screen
			current_angle = self.rotation - iter_ang * x + self.fov.x / 2
			# Ray calculation
			direction = Vector2.polar_to_cartesian(render_distance, current_angle)
			ray = Segment(self.pos, self.pos + direction)

			# Any wall within render distance will overwrite it
			dist = render_distance + 1
			# Default no collisions
			collision = None

			# Checking an intersecction with every wall in the sene
			for object_ in self.objects:
				segment = object_.segment
				# If the ray intersects the wall, using vector calculation
				if ray.intersects(segment):
					# Calculate the distance to the wall
					new_dist = ray.count_intersection(segment) - self.pos
					# If it is closer than the current closest wall, write new distance
					if new_dist.magnitude < dist:
						dist = new_dist.magnitude
						collision = object_

			# If no walls, fill the screen with background colour
			if collision is None:
				for y in range(self.screen_size.y):
					self.screen[y][x] = gradient[-1]
				continue

			if dist != 0:
				# Calculate the upper and lower proportion of the screen to be filled
				pix_u = int(self.screen_size.y * self.du0 / dist)
				pix_d = int(self.screen_size.y * self.dd0 / dist)
			else:
				pix_u = self.screen_size.y // 2 + 1
				pix_d = self.screen_size.y // 2 + 1

			# Calculate which colour from the gradient to use
			fac = math.floor(dist / render_distance * (len(gradient) - 1))
			
			# Filling - one of the tags; almost never used
			if len(collision.filling) != 1:
				char_ = gradient[fac]
			else:
				char_ = collision.filling

			# Slabbing - adding half-pixels ▄ and ▀ to smoothen the walls
			slabbed_u = pix_u % 2 and collision.slabbable
			slabbed_d = pix_d % 2 and collision.slabbable

			# The lowest and highest points on the screen to be filled
			min_ = max(int(self.screen_size.y / 2) - pix_u // 2 + 1, 0)
			max_ = min(int(self.screen_size.y / 2) + pix_d // 2, self.screen_size.y)

			# Paint the vertical strip between the maximum and minimum pixels
			for y in range(self.screen_size.y):
				if y >= min_ and y <= max_:
					self.screen[y][x] = char_
				# Add slabs
				elif y == min_ - 1 and slabbed_u:
					self.screen[y][x] = "▄"
				elif y == max_ + 1 and slabbed_d:
					self.screen[y][x] = "▀"
				# Fill the rest with the background colour
				else:
					self.screen[y][x] = gradient[-1]

	def displace(self, direction):
		move = Segment(self.pos, self.pos + direction)
		intersection = False
		for object_ in self.objects:
			if object_.segment.intersects(move):
				intersection = True
				if object_.is_exit:
					self.runner.escape()
		if not intersection:
			self.pos += direction
		return not intersection

	def move(self, magnitude, precision=5):
		direction = Vector2.polar_to_cartesian(magnitude / precision, self.rotation)
		for i in range(precision):
			if not self.displace(direction):
				break