import math
from Tools import Vector2, Segment, Ray
from Angle import Angle


class Camera():
	def __init__(self, pos=Vector2(), rotation=Angle(),
		screen_size=Vector2(200, 55), fov=Vector2(120, 80)):
			self.pos = pos.cast()
			self.rotation = rotation
			self.fov = fov
			self.screen_size = screen_size.cast()
			self.screen = []
			self.objects = []
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
		gradient = "▓@%#+=*:-."
		# gradient = "$@B%8&WM#|()1[]?-_+~\"^`,'."
		# gradient = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1[]?-_+~<>i!lI;:,\"^`'."
		# gradient = "█▓▒░ "
		render_distance = 100
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
				brightness = 4 - (dist + 1) / 2

			if brightness:
				y_iter_ang = self.fov.y / self.screen_size.y
				for y in range(0, self.screen_size.y - 1):
					vertical_angle = Angle(y_iter_ang * y - self.fov.y / 2)
					h = - dist * math.tan(vertical_angle.rad) + 1.5
					if h >= 0 and h <= 2.5:
						if brightness:
							if brightness >= 4:
								self.screen[y][x] = gradient[0]
							elif brightness >= 0:
								try:
									fac = math.floor((4 - brightness) / 4 * len(gradient))
									self.screen[y][x] = gradient[fac]
								except:
									print(fac, brightness)
							else:
								self.screen[y][x] = gradient[-1]
					else:
						self.screen[y][x] = " "
			else:
				for y in range(self.screen_size.y):
					self.screen[y][x] = " "

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
			
			

# █, ▓, ▒, ░,  
#
