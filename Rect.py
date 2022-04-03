from Vector2 import Vector2


class Rect():
	def __init__(self, a, b):
		self.a = Vector2(min(a.x, b.x), min(a.y, b.y))
		self.b = Vector2(max(a.x, b.x), max(a.y, b.y))

	@property
	def width(self):
		return self.b.x - self.a.x

	@property
	def height(self):
		return self.b.y - self.a.y

	def __str__(self):
		return "Rectangle ({}, {}), ({}, {})".format(self.a.x, self.a.y, self.b.x, self.b.y)

