import math
from Angle import Angle


class Vector2:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	@property
	def magnitude(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

	@property
	def unit(self):
		if self.magnitude == 0:
			return Vector2()
		return Vector2(self.x / self.magnitude, self.y / self.magnitude)

	@property
	def normal(self):
		return Vector2(self.y, -self.x)

	def dot(self, vector):
		return self.x * vector.x + self.y * vector.y

	def angle(self, vector):
		return Angle(math.acos(self.dot(vector) / (self.magnitude * vector.magnitude)), in_rads=True)

	def cast(self):
		return Vector2(self.x, self.y)

	def __add__(self, vector):
		return Vector2(self.x + vector.x, self.y + vector.y)

	def __iadd__(self, vector):
		self.x += vector.x
		self.y += vector.y
		return self

	def __sub__(self, vector):
		return Vector2(self.x - vector.x, self.y - vector.y)

	def __isub__(self, vector):
		self.x -= vector.x
		self.y -= vector.y
		return self

	def __mul__(self, val):
		return Vector2(self.x * val, self.y * val)

	def __imul__(self, val):
		self.x *= val
		self.y *= val
		return self

	def __div__(self, val):
		if val == 0:
			raise ZeroDivisionError
		return Vector2(self.x / val, self.y / val)

	def __idiv__(self, val):
		if val == 0:
			raise ZeroDivisionError
		self.x /= val
		self.y /= val
		return self

	def __str__(self):
		return "Vector2: x = {}, y = {}".format(self.x, self.y)

	@staticmethod
	def polar_to_cartesian(r, rad):
		return Vector2(r * math.cos(rad), r * math.sin(rad))

class Equation:
	def __init__(self, a=0, b=0, c=0):
		self.a = a
		self.b = b
		self.c = c
		self.a2b2 = math.sqrt(a ** 2 + b ** 2)

	def make_equation(self, pos_a, pos_b):
		dx = pos_b.x - pos_a.x
		dy = pos_b.y - pos_a.y
		self.a = dy
		self.b = - dx
		if dx == 0:
			self.a = 1
			self.c = - pos_a.x
		elif dy == 0:
			self.b = 1
			self.c = - pos_a.y
		else:
			self.c = (pos_a.y - (dy / dx) * pos_a.x) * dx
		self.a2b2 = math.sqrt(self.a ** 2 + self.b ** 2)

	def count_intersection(self, equation):
		a1 = self.a
		b1 = self.b
		c1 = self.c
		a2 = equation.a
		b2 = equation.b
		c2 = equation.c
		div = (a1 * b2 - a2 * b1)
		if div == 0:
			return None
		x = (b1 * c2 - b2 * c1) / div
		y = (c1 * a2 - c2 * a1) / div
		return Vector2(x, y)

	def dist_to_point(self, vector):
		return abs(self.a * vector.x + self.b * vector.y + self.c) / self.a2b2

	def __str__(self):
		return str(self.a) + "x + " + str(self.b) + "y + " + str(self.c)

class Segment():
	def __init__(self, pos_a, pos_b):
		self.pos_a = pos_a
		self.pos_b = pos_b
		self.normal = (pos_a - pos_b).normal
		if self.pos_a.x > self.pos_b.x:
			self.pos_a, self.pos_b = self.pos_b, self.pos_a
		self.equation = Equation()
		self.equation.make_equation(pos_a, pos_b)
		self.direction = pos_a - pos_b

	def set_vertices(self, new_pos_a, new_pos_b):
		self.pos_a = new_pos_a
		self.pos_b = new_pos_b
		self.equation.make_equation(pos_a, pos_b)
		self.direction = Vector2(pos_a.x - pos_b.x, pos_a.y - pos_b.y)
	
	def intersects(self, segment):
		if self.normal.dot(segment.pos_a - self.pos_a) * self.normal.dot(segment.pos_b - self.pos_a) > 0:
			return False
		if segment.normal.dot(self.pos_a - segment.pos_a) * segment.normal.dot(self.pos_b - segment.pos_a) > 0:
			return False
		return True

	def check_point(self, vector):
		return self.direction.dot(vector - self.pos_a) * self.direction.dot(vector - self.pos_b) < 0

	def count_intersection(self, segment):
		return self.equation.count_intersection(segment.equation)

	def dist_to_point(self, vector, do_dot_stuff=True):
		return min((self.pos_a - vector).magnitude, (self.pos_b - vector).magnitude, self.equation.dist_to_point(vector))

class Ray():
	def __init__(self, pos, direction):
		self.pos = pos
		self.direction = direction.unit
		self.normal = direction.normal
		self.equation = Equation()
		self.equation.make_equation(pos, pos + direction)

	def count_intersection(self, segment):
		intersection = self.equation.count_intersection(segment.equation)
		if intersection == None or not self.check_point(intersection):
			return None
		return intersection - self.pos

	def intersects(self, segment):
		if self.normal.dot(segment.pos_a - self.pos) * self.normal.dot(segment.pos_b - self.pos) >= 0:
			return False
		return True

	def check_point(self, vector):
		return self.direction.dot(vector - self.pos) >= 0

	def if_matches(self, new_pos):
		return self.direction.dot(new_pos - self.pos) >= 0

if __name__ == "__main__":
	# a = Vector2(2, 3)
	# b = Vector2(-3, 2)
	# print(a, b)
	# print(a + b)
	# a *= 3
	# print(a, b)
	# print("DP", a.dot(b))
	# print("Angle", a.angle(b))
	# print(a.normal)
	r = MathRay(Vector2(1, 1), Vector2(2, 1))
	s1 = Segment(Vector2(6, 1), Vector2(3, 3))
	print(r.intersects(s1))
	print(r.count_intersection(s1))

