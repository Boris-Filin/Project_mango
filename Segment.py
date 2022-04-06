import math
from Vector2 import Vector2
from Equation import Equation


class Segment():
	def __init__(self, pos_a, pos_b):
		self.pos_a = pos_a
		self.pos_b = pos_b
		self.normal = (pos_a - pos_b).normal
		self.equation = Equation.from_points(pos_a, pos_b)

	def intersects(self, segment):
		if self.normal.dot(segment.pos_a - self.pos_a) * self.normal.dot(segment.pos_b - self.pos_a) > 0:
			return False
		if segment.normal.dot(self.pos_a - segment.pos_a) * segment.normal.dot(self.pos_b - segment.pos_a) > 0:
			return False
		return True

	def count_intersection(self, segment):
		return self.equation.count_intersection(segment.equation)