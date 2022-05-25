import math
from Vector2 import Vector2
from Segment import Segment
from Equation import Equation

class Camera():
	def __init__(self, runner, pos=Vector2(), rotation=0,
		screen_size=Vector2(200, 55), fov=Vector2(90, 80), **kwargs):

		self.runner = runner
		self.pos = pos.cast()
		self.rotation = rotation
		self.fov = fov
		self.clamp_fov()

		self.screen_size = screen_size.cast()
		self.screen = []
		self.objects = []

		self.depth_buffer = []
		self.wall_buffer = []
		self.gradient_buffer = []
		self.init_gradient_buffer()

		self.player_height = 1.5 if not "player_height" in kwargs else kwargs["player_height"]
		self.wall_height = 2.5 if  not "wall_height" in kwargs else kwargs["wall_height"]

		self.camera_height = self.player_height
		self.is_moving = False
		self.oscillation_amplitude = 0.1
		self.oscillation_offset = 0
		self.oscillation_speed = 4

		self.gradient = "█" * 2 + "▓" * 3 + "▒" * 3 + "░" * 3 +" "
		self.render_distance = 10

		self.initialize_screen()
		# self.update()

	def initialize_screen(self):
		for y in range(self.screen_size.y):
			self.screen.append([])
			for x in range(self.screen_size.x):
				self.screen[y].append(" ")

	def init_gradient_buffer(self):
		left_border = math.tan(math.radians(self.fov.x / 2))
		step = 2 * left_border / self.screen_size.x
		for x in range(self.screen_size.x):
			x_i = - left_border + step / 2 + step * x
			self.gradient_buffer.append(x_i)

	def clamp_fov(self):
		if self.fov.x < 10:
			self.fov.x = 10
		if self.fov.x > 170:
			self.fov.x = 170

	def send_screen(self):
		return self.screen
				
	def update_objects(self, objects):
		self.objects = objects
			
	def update(self, elapsed_time):
		if self.oscillation_offset != 0 and not self.is_moving:
			tmp = self.oscillation_offset // math.pi
			self.oscillation_offset += self.oscillation_speed * elapsed_time
			if self.oscillation_offset // math.pi > tmp:
				self.oscillation_offset = 0

		self.vert()
		self.frag()

		self.is_moving = False

	def vert(self):
		alpha = math.radians(self.rotation - 90)
		cos_a = math.cos(alpha)
		sin_a = math.sin(alpha)
		tan_a = math.tan(alpha)

		fov_tan = math.tan(math.radians(self.fov.x / 2))

		self.depth_buffer = [-1 for i in range(self.screen_size.x)]
		self.wall_buffer = [-1 for i in range(self.screen_size.x)]

		for i in range(len(self.objects)):
			segment = self.objects[i].segment
			point_a = self.transform_point(segment.pos_a, cos_a, sin_a)
			point_b = self.transform_point(segment.pos_b, cos_a, sin_a)

			depth_a = point_a.y
			depth_b = point_b.y

			if depth_a > self.render_distance and depth_b > self.render_distance or depth_a < 0 and depth_b < 0:
				continue

			if point_a == Vector2() or point_b == Vector2():
				continue


			left = Vector2(self.gradient_buffer[0], 1)
			right = Vector2(self.gradient_buffer[-1], 1)

			a_NE = left.cross(point_a) < 0
			a_NW = right.cross(point_a) > 0
			is_a_inside = a_NE and a_NW
			b_NE = left.cross(point_b) < 0
			b_NW = right.cross(point_b) > 0
			is_b_inside = b_NE and b_NW

			if not (a_NE or b_NE) or not (a_NW or b_NW):
				continue

			width_at_a = depth_a * fov_tan
			width_at_b = depth_b * fov_tan

			eq = Equation.from_points(point_a, point_b)

			# When both are inside (render normally)
			if is_a_inside and is_b_inside:
				column_a = int((point_a.x + width_at_a) * self.screen_size.x / (2 * width_at_a))
				column_b = int((point_b.x + width_at_b) * self.screen_size.x / (2 * width_at_b))
			# When ONLY A is outside
			elif is_b_inside:
				column_a = self.handle_point_outside_fov(eq, a_NE, a_NW)
				column_b = int((point_b.x + width_at_b) * self.screen_size.x / (2 * width_at_b))
			# When ONLY B is outside
			elif is_a_inside:
				column_a = int((point_a.x + width_at_a) * self.screen_size.x / (2 * width_at_a))
				column_b = self.handle_point_outside_fov(eq, b_NE, b_NW)
			# When neither are in sight
			else:
				# Discard the verrtical case (never drawn)
				if eq.b == 0:
					continue
				# if the line passes above the camera
				if eq.c / eq.b < 0 and point_a.x * point_b.x < 0:
					column_a = 0
					column_b = self.screen_size.x - 1
				# The line is out of sight
				else:
					continue

			if column_a == -1 or column_b == -1:
				continue

			wall_length = abs(column_b - column_a)
			for j in range(wall_length + 1):
				column = column_a + int(math.copysign(j, column_b - column_a))
				if column < 0 or column > self.screen_size.x - 1:
					continue
				if wall_length == 0:
					depth = min(depth_a, depth_b)
				else:
					t = j / wall_length
					div = eq.a * self.gradient_buffer[column] + eq.b
					if div == 0:
						depth = -1
					else:
						depth = - eq.c / div
					# depth = depth_a + t * (depth_b - depth_a)
				if depth <= 0 or depth > self.render_distance:
					continue
				if self.depth_buffer[column] == -1 or self.depth_buffer[column] > depth:
					self.depth_buffer[column] = depth
					self.wall_buffer[column] = i

	def handle_point_outside_fov(self, eq, ne, nw):
		# Point below the camera
		if not (ne or nw):
			# When the wall passes directly through the camera
			if eq.c == 0:
				return -1
			# To the right of the camera (x-intercept > 0)
			if eq.c / eq.a < 0:
				return self.screen_size.x - 1
			# To the left of the camera (x-intercept < 0)
			return 0
		# Point in the right quadrant
		elif ne:
			return self.screen_size.x - 1
		# Point in the left quadrant (the only remaining case)
		return 0

	def frag(self):
		self.oscillation_offset %= math.tau
		self.camera_height = self.player_height + math.sin(self.oscillation_offset) * self.oscillation_amplitude

		du0 = (self.wall_height - self.camera_height) / math.tan(math.radians(self.fov.y / 2))
		dd0 = self.camera_height / math.tan(math.radians(self.fov.y / 2))

		for x in range(self.screen_size.x):
			depth = self.depth_buffer[x]

			if depth == -1:
				for y in range(self.screen_size.y):
					self.screen[y][x] = self.gradient[-1]
				continue

			# Calculate the upper and lower proportion of the screen to be filled
			pix_u = int(self.screen_size.y * du0 / depth)
			pix_d = int(self.screen_size.y * dd0 / depth)

			# Calculate which colour from the gradient to use
			fac = math.floor(depth / self.render_distance * (len(self.gradient) - 1))

			wall = self.objects[self.wall_buffer[x]]
			
			# Filling - one of the tags; almost never used
			if len(wall.filling) != 1:
				char_ = self.gradient[fac]
			else:
				char_ = wall.filling

			# Slabbing - adding half-pixels ▄ and ▀ to smoothen the walls
			slabbed_u = pix_u % 2 and wall.slabbable
			slabbed_d = pix_d % 2 and wall.slabbable

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
					self.screen[y][x] = self.gradient[-1]

	def transform_point(self, point, cos_a, sin_a):
		x = point.x * cos_a + point.y * sin_a - self.pos.x * cos_a - self.pos.y * sin_a
		y = - point.x * sin_a + point.y * cos_a + self.pos.x * sin_a - self.pos.y * cos_a
		new_point = Vector2(x, y)
		return new_point

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
			self.oscillation_offset += direction.magnitude * self.oscillation_speed
			self.is_moving = True
		return not intersection

	def move(self, magnitude, precision=5):
		direction = Vector2.polar_to_cartesian(magnitude / precision, self.rotation)
		for i in range(precision):
			if not self.displace(direction):
				break