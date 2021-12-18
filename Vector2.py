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