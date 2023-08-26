from Segment import Segment
from Vector2 import Vector2
from Equation import Equation	
import math


class Wall():
	def __init__(self, segment, tags={}):
		self.segment = segment
		self.tags = {} if tags is None else tags

		self.filling = "" if self.tags.get("fill") is None else self.tags["fill"]
		# self.slabbable = True
		self.slabbable = True if self.tags.get("slab") is None else self.tags["slab"].lower() == "true"
		self.is_exit = False if self.tags.get("is_exit") is None else self.tags["is_exit"].lower() == "true"

	def calculate_chunks(self, chunk_width):
		chunks = []
		# pos_a = Vector2(self.segment.pos_a.x / chunk_width, self.segment.pos_a.y / chunk_width)
		# pos_b = Vector2(self.segment.pos_b.x / chunk_width, self.segment.pos_b.y / chunk_width)
		pos_a = self.segment.pos_a / chunk_width
		pos_b = self.segment.pos_b / chunk_width

		equation = Equation.from_points(pos_a, pos_b)

		if pos_a.x > pos_b.x:
			pos_a, pos_b = pos_b, pos_a

		if math.floor(pos_a.x) == math.floor(pos_b.x):
			min_ = math.floor(min(pos_a.y, pos_b.y))
			max_ = math.floor(max(pos_a.y, pos_b.y))
			for y in range(min_, max_ + 1):
				chunks.append((math.floor(pos_a.x), y))
			return chunks

		last_y = equation.get_y(pos_a.y)
		for x in range(math.floor(pos_a.x), math.floor(pos_b.x) + 1):
			if x == math.floor(pos_b.x):
				y = math.floor(pos_b.y)
			else:
				y = math.floor(equation.get_y(x + 1))

			min_ = math.floor(min(y, last_y))
			max_ = math.floor(max(y, last_y))
			for y_iter in range(min_, max_ + 1):
				chunks.append((x, y_iter))
			last_y = y
		
		return chunks

