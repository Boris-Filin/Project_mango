import re
from Vector2 import Vector2
from Segment import Segment

class Loader():
	def __init__(self, file_name):
		self.lines = self.load_file(file_name)
		self.objects = []
		self.player_pos = Vector2()
		self.player_rotation = 0
		self.decode_lines()

	def load_file(self, file_name):
		try:
			with open("Custom_Maps/" + file_name, "r") as file:
				lines = file.readlines()
				return lines
		except:
			return []

	def decode_lines(self):
		for l in self.lines:
			line = l.strip().lower()
			line = re.sub(r"[,();]", "", line)
			line = line.split()
			try:
				if line[0] == "s":
					pos_a = Vector2(float(line[1]), float(line[2]))
					pos_b = Vector2(float(line[3]), float(line[4]))
					segment = Segment(pos_a, pos_b)
					self.objects.append(segment)
				if line[0] == "p":
					self.player_pos = Vector2(float(line[1]), float(line[2]))
				if line[0] == "r":
					self.player_rotation = float(line[1])
			except:
				continue
