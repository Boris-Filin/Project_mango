import re
from Vector2 import Vector2
from Segment import Segment
from Wall import Wall

class Loader():
	def __init__(self, file_name, screen):
		self.lines = self.load_file(file_name)
		self.objects = []
		self.player_pos = Vector2()
		self.player_rotation = 0
		self.decode_lines()

		self.screen = screen

		self.visual_map = None

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
			line_text = re.sub(r"[,()]", "", line)
			line = line_text.split()
			try:
				if line[0] == "s":
					pos_a = Vector2(float(line[1]), float(line[2]))
					pos_b = Vector2(float(line[3]), float(line[4]))
					tags = self.handle_tags(line_text)
					segment = Segment(pos_a, pos_b)
					wall = Wall(segment, tags)
					self.objects.append(wall)
				if line[0] == "p":
					self.player_pos = Vector2(float(line[1]), float(line[2]))
				if line[0] == "r":
					self.player_rotation = float(line[1])
			except:
				continue
		if len(self.objects) == 0:
			quit()

	def handle_tags(self, line):
		tags_text = re.search(r"\{.*\}", line)
		if tags_text == None:
			return {}
		tags = {}
		tags_strings = re.sub(r"\{|\}", "", tags_text.group(0)).split(";")
		for tag_string in tags_strings:
			tag = tag_string.strip()
			if not ":" in tag:
				continue
			key = tag[:tag.find(":")]
			val = tag[tag.find(":") + 1:]
			tags[key] = val


		return tags