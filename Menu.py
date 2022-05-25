from Runner import Runner
from Maze import Maze
import time
from Vector2 import Vector2
import os
from Stage import Stage
from Loader import Loader

class Menu(Stage):
	def __init__(self, actions, size=Vector2(200, 55)):
		self.actions = actions
		self.size = size

		self.prev_frame_time = time.time()
		self.elapsed_time = 0

		self.pointer_pos = 0
		self.menu_type = "user_levels"
		self.fetch_levels()

		self.map_ = []
		self.prime_map()
		self.fill_map()

	def fetch_levels(self):
		if self.menu_type == "user_levels":
			self.levels = os.listdir("Custom_Maps")
		elif self.menu_type == "random_levels":
			self.levels = []
			self.levels.append("Easy")
			self.levels.append("Normal")
			self.levels.append("Hard")
			self.levels.append("Nightmare")
			self.levels.append("Impossible")

	def fill_map(self):
		for y in range(self.size.y):
			for x in range(self.size.x):
				if y == 0 or y == self.size.y - 1 or x == 0 or x == self.size.x - 1:
					self.map_[y][x] = "█"
				else:
					self.map_[y][x] = " "
		x_center = self.size.x // 2
		self.put_string("Choose level:", Vector2(x_center, 5), True)
		self.put_string("(Use ARROW UP or ARROW DOWN to navigate, ARROW LEFT or ARROW RIGHT to switch menus, press SPACE when ready)",
			Vector2(x_center, 7), True)
		if self.menu_type == "user_levels":
			self.put_string("CUSTOM LEVELS >", Vector2(x_center, 9), True)
		elif self.menu_type == "random_levels":
			self.put_string(" < COMPUTER GENERATED MAZES", Vector2(x_center, 9), True)
		self.put_string("Use ESC to quit", Vector2(x_center, 48), True)
		self.put_string("Use W, S to move around", Vector2(x_center, 50), True)
		self.put_string("Use A, D to rotate the camera", Vector2(x_center, 52), True)
		for l in self.levels:
			if not ".txt" in l and self.menu_type == "user_levels":
				self.levels.remove(l)
		for i in range(len(self.levels)):
			height =  12 + i * 3 - self.pointer_pos * 3
			if height <= 10:
				self.put_string(" . . . ", Vector2(x_center, 10), True)
			elif height >= 45:
				self.put_string(" . . . ", Vector2(x_center, 45), True)				
			else:
				if i == self.pointer_pos:
					self.put_string("===>   -= " + self.levels[i].replace(".txt", "") + " =-   <===", Vector2(x_center, height), True)
				else:
					self.put_string("-= " + self.levels[i].replace(".txt", "") + " =-", Vector2(x_center, height), True)

	def stage_update(self):
		if self.actions.has("arrow_up") and self.pointer_pos > 0:
			self.pointer_pos -= 1
			self.actions.remove("arrow_up")
		if self.actions.has("arrow_down") and self.pointer_pos < len(self.levels) - 1:
			self.pointer_pos += 1
			self.actions.remove("arrow_down")
		if self.actions.has("arrow_right") and self.menu_type == "user_levels":
			self.pointer_pos = 0
			self.menu_type = "random_levels"
			self.actions.remove("arrow_right")
			self.fetch_levels()
		if self.actions.has("arrow_left") and self.menu_type == "random_levels":
			self.pointer_pos = 0
			self.menu_type = "user_levels"
			self.actions.remove("arrow_left")
			self.fetch_levels()
		if self.actions.has("continue"):
			self.actions.clear()
			if self.menu_type == "user_levels":
				loaded_map = Loader(self.levels[self.pointer_pos])
				map_name = self.levels[self.pointer_pos].replace(".txt", "")
				is_maze = False
			elif self.menu_type == "random_levels":
				if self.levels[self.pointer_pos] == "Easy":
					loaded_map = Maze(5, 5)
					map_name = "Easy"
				elif self.levels[self.pointer_pos] == "Normal":
					loaded_map = Maze(10, 10)
					map_name = "Normal"
				elif self.levels[self.pointer_pos] == "Hard":
					loaded_map = Maze(10, 15)
					map_name = "Hard"
				elif self.levels[self.pointer_pos] == "Nightmare":
					loaded_map = Maze(30, 30)
					map_name = "Nightmare"
				elif self.levels[self.pointer_pos] == "Impossible":
					loaded_map = Maze(50, 50)
					map_name = "Impossible"
				else:
					loaded_map = Maze(8, 6)
					map_name = "Glitched"
				is_maze = True
			game_runner = Runner(self.actions, loaded_map, map_name, self.size, is_maze)
			self.clear_screen()
			return game_runner

