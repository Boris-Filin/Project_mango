from Menu import Menu
from Stage import Stage
from Vector2 import Vector2
import time
from TitleArt import art1


class Title(Stage):
	def __init__(self, screen, actions, size=Vector2(200, 55)):
		# screen.set_color(15, 0)
		self.screen = screen
		self.actions = actions
		self.size = size
		self.map_ = []
		self.prime_map()
		# self.fill_map()
		self.art_slices = art1.split("\n")
		self.art_slices = list(filter(lambda s: s != "", self.art_slices))

		self.elapsed_time = 0
		self.prev_frame_time = time.time()

	def fill_map(self):
		for y in range(self.size.y):
			for x in range(self.size.x):
				if y == 0 or y == self.size.y - 1 or x == 0 or x == self.size.x - 1:
					self.map_[y][x] = "█"
				else:
					self.map_[y][x] = " "

		x_center = self.size.x // 2
		y_center = self.size.y // 2
		for y in range(len(self.art_slices)):
			self.put_string(self.art_slices[y], Vector2(x_center, y_center - len(self.art_slices) // 2 + y), True)
		self.put_string("Press SPACE when ready", Vector2(x_center, y_center + len(self.art_slices) // 2 + 3), True)


	def stage_update(self):
		if self.actions.has("continue"):
			self.actions.clear()
			return Menu(self.screen, self.actions, self.size)


