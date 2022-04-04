import random
from Vector2 import Vector2
from Rect import Rect
from Colours import coloured, TxtColour, BgColour
from Segment import Segment
from Wall import Wall

class Maze():
	def __init__(self, w = 6, h = 6, cell_size = 2):
		self.map_ = []
		self.w = w
		self.h = h
		self.cell_size = cell_size

		self.chamber_queue = []
		self.lines = []
		self.cells = []
		self.objects = []
		self.player_pos = Vector2()
		self.player_rotation = random.random() * 360
		self.exit_pos = 0
		self.exit_wall = 0

		self.walls_colour = "magenta"
		self.exit_colour = "red"
		self.player_colour = "red"

		self.generate()
		self.convert_to_walls()
		self.visual_map = str(self)

				
	def generate(self):
		self.lines.append(Rect(Vector2(0, 0), Vector2(self.w, 0)))
		self.lines.append(Rect(Vector2(self.w, 0), Vector2(self.w, self.h)))
		self.lines.append(Rect(Vector2(0, self.h), Vector2(self.w, self.h)))
		self.lines.append(Rect(Vector2(0, 0), Vector2(0, self.h)))

		self.chamber_queue.append(Rect(Vector2(), Vector2(self.w, self.h)))
		while len(self.chamber_queue) > 0:
			self.split_chamber(self.chamber_queue.pop(0))
		self.put_exit()
		self.put_player()
		self.update_cells()

	def get_walls(self):
		self.convert_to_walls()
		return self.objects

	def convert_to_walls(self):
		for i in range(len(self.lines)):
			line = self.lines[i]
			segment = Segment(line.a * self.cell_size, line.b * self.cell_size)
			if i < len(self.lines) - 1:
				wall = Wall(segment)
			else:
				wall = Wall(segment, {"fill": ".", "slab": "false", "is_exit": "true"})
			self.objects.append(wall)

# Wall indicies: North - 0; East - 1; South - 2; West - 3.
	def put_exit(self):
		self.exit_wall = random.randint(0, 3)
		if self.exit_wall == 0 or self.exit_wall == 2:
			self.exit_pos = random.randint(0, self.w - 1)
		elif self.exit_wall == 1 or self.exit_wall == 3:
			self.exit_pos = random.randint(0, self.h - 1)
		if self.exit_wall == 0 or self.exit_wall == 2:
			old_wall = self.lines.pop(self.exit_wall)
			left_wall = Rect(old_wall.a, Vector2(self.exit_pos, old_wall.a.y))
			right_wall = Rect(Vector2(self.exit_pos + 1, old_wall.b.y), old_wall.b)
			exit_wall = Rect(Vector2(self.exit_pos, old_wall.a.y), Vector2(self.exit_pos + 1, old_wall.b.y))
			if right_wall.width != 0:
				self.lines.insert(self.exit_wall, right_wall)
			if left_wall.width != 0:
				self.lines.insert(self.exit_wall, left_wall)
			self.lines.append(exit_wall)
		elif self.exit_wall == 1 or self.exit_wall == 3:
			old_wall = self.lines.pop(self.exit_wall)
			upper_wall = Rect(old_wall.a, Vector2(old_wall.a.x, self.exit_pos))
			lower_wall = Rect(Vector2(old_wall.b.x, self.exit_pos + 1), old_wall.b)
			exit_wall = Rect(Vector2(old_wall.a.x, self.exit_pos), Vector2(old_wall.b.x, self.exit_pos + 1))
			if upper_wall.height != 0:
				self.lines.insert(self.exit_wall, upper_wall)
			if lower_wall.height != 0:
				self.lines.insert(self.exit_wall, lower_wall)
			self.lines.append(exit_wall)

	def put_player(self):
		if self.exit_wall == 0:
			self.player_pos = Vector2(random.randint(0, self.w - 1), random.randint(self.h // 2 + 1, self.h - 1))
		elif self.exit_wall == 1:
			self.player_pos = Vector2(random.randint(0, self.w // 2), random.randint(0, self.h - 1))
		elif self.exit_wall == 2:
			self.player_pos = Vector2(random.randint(0, self.w - 1), random.randint(0, self.h // 2))
		elif self.exit_wall == 3:
			self.player_pos = Vector2(random.randint(self.w // 2 + 1, self.w - 1), random.randint(0, self.h - 1))
		self.player_pos += Vector2(0.5, 0.5)
		self.player_pos *= self.cell_size

	def update_player_pos(self, new_pos):
		self.player_pos = new_pos // self.cell_size

	def split_chamber(self, chamber):
		a = chamber.a
		b = chamber.b
		balance_offset = 0.25
		if chamber.width == chamber.height:
			vertical_chance = 0.5
		elif chamber.width < chamber.height:
			vertical_chance = 0.5 - balance_offset
		else:
			vertical_chance = 0.5 + balance_offset

		vertical = random.random() < vertical_chance
		# print(a.x + 1, b.x - 1)
		if vertical:
			line_x = random.randint(a.x + 1, b.x - 1)
			new_chamber_1 = Rect(a, Vector2(line_x, b.y))
			new_chamber_2 = Rect(Vector2(line_x, a.y), b)
			self.try_queueing_chamber(new_chamber_1)
			self.try_queueing_chamber(new_chamber_2)

			line_break = random.randint(a.y, b.y - 1)
			line_1 = Rect(Vector2(line_x, a.y), Vector2(line_x, line_break))
			line_2 = Rect(Vector2(line_x, line_break + 1), Vector2(line_x, b.y))

			if line_1.height != 0:
				self.lines.append(line_1)
			if line_2.height != 0:
				self.lines.append(line_2)
		else:
			line_y = random.randint(a.y + 1, b.y - 1)
			new_chamber_1 = Rect(a, Vector2(b.x, line_y))
			new_chamber_2 = Rect(Vector2(a.x, line_y), b)
			self.try_queueing_chamber(new_chamber_1)
			self.try_queueing_chamber(new_chamber_2)

			line_break = random.randint(a.x, b.x - 1)
			line_1 = Rect(Vector2(a.x, line_y), Vector2(line_break, line_y))
			line_2 = Rect(Vector2(line_break + 1, line_y), Vector2(b.x, line_y))

			if line_1.width != 0:
				self.lines.append(line_1)
			if line_2.width != 0:
				self.lines.append(line_2)

	def try_queueing_chamber(self, chamber):
		if chamber.b.x - chamber.a.x < 2:
			return
		if chamber.b.y - chamber.a.y < 2:
			return
		self.chamber_queue.append(chamber)

# Cells: (NothWall, WestWall)

	def update_cells(self):
		self.cells = []
		for y in range(self.h + 1):
			self.cells.append([])
			for x in range(self.w + 1):
				self.cells[y].append([False, False])

		for i in range(len(self.lines) - 1):
			line = self.lines[i]
			a = line.a
			b = line.b
			vertical = a.x == b.x
			if vertical:
				for y in range(b.y - a.y):
					self.cells[a.y + y][self.w - (a.x)][1] = True
			else:
				for x in range(b.x - a.x):
					self.cells[a.y][self.w - (a.x + x) - 1][0] = True

	def __str__(self):
		res = ""
		for y in range(self.h + 1):
			if y != 0:
				res += "\n"
			for x in range(self.w + 1):
				cell = self.cells[y][x]
				char = "  "
				if cell[0] and cell[1]:
					char = "█▀"
				elif cell[0] and not cell[1]:
					char = "▀▀"
				elif not cell[0] and cell[1]:
					char = "█ "
				else:
					if x > 0:
						if self.cells[y][x - 1][0]:
							char = "▀ "
					if y > 0:
						if self.cells[y - 1][x][1]:
							char = "▀ "

				is_coloured = False

				if x == self.w - int(self.player_pos.x) - 1 and y == int(self.player_pos.y):
					if char[1] == "▀":
						char = char[0] + coloured(char[1], bg = self.player_colour)
					else:
						char = char[0] + coloured("▄", col = self.player_colour)
					char += coloured(clear = True)
				res += char

		return res




# ▄▀█
