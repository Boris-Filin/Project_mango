from Stage import Stage
from Vector2 import Vector2
import time
import math
from TitleArt import art1
# from Menu import Menu


class WinScreen(Stage):
	def __init__(self, screen, actions, map_name, final_time=0, size=Vector2(200, 55)):
		# screen.set_color(15, 0)
		self.screen = screen
		self.actions = actions
		self.size = size
		self.map_ = []
		self.prime_map()

		self.map_name = map_name
		self.final_time = final_time

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
		self.put_string("CONGRATULATIONS!", Vector2(x_center, y_center - 2), True)
		self.put_string("You have beaten the {}!".format(self.map_name), Vector2(x_center, y_center), True)
		minutes = math.floor(self.final_time / 60)
		seconds = math.floor(self.final_time - minutes * 60)
		milliseconds = int(self.final_time % 1 * 1000)
		self.put_string("Final time: {}:{}.{}".format(minutes, seconds, milliseconds), Vector2(x_center, y_center + 2), True)

	def stage_update(self):
		if self.actions.has("continue"):
			self.actions.clear()
			# return Menu(self.screen, self.actions, self.size)


