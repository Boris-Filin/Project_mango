import math
from Vector2 import Vector2


class Equation:
	def __init__(self, a=0, b=0, c=0):
		self.a = a
		self.b = b
		self.c = c

# classmethod is a different type of constructor.
# It allows for the equation to be derived from two points.
	@classmethod
	def from_points(cls, pos_a, pos_b):
		dx = pos_b.x - pos_a.x
		dy = pos_b.y - pos_a.y
		a = dy
		b = - dx
		if dx == 0:
			a = 1
			c = - pos_a.x
		elif dy == 0:
			b = 1
			c = - pos_a.y
		else:
			c = (pos_a.y - (dy / dx) * pos_a.x) * dx
		return cls(a, b, c)

# The previously derived formuli
	def count_intersection(self, equation):
		div = (self.a * equation.b - equation.a * self.b)
		if div == 0:
			return None
		x = (self.b * equation.c - equation.b * self.c) / div
		y = (self.c * equation.a - equation.c * self.a) / div

		return Vector2(x, y)

	def __str__(self):
		return str(self.a) + "x + " + str(self.b) + "y + " + str(self.c)