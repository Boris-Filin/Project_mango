import random
import time
from colorconsole import terminal
from Camera import Camera
from Loader import Loader
from Vector2 import Vector2
from WinScreen import WinScreen

class Runner():
	def __init__(self, screen, actions, loaded_map, map_name, size=Vector2(200, 55), is_maze=False):
		# loaded_map = Loader(map_name)
		objects = loaded_map.objects
		self.map_name = map_name
		self.initial_pos = loaded_map.player_pos
		self.initial_rotation = loaded_map.player_rotation
		self.escaped = False

		# screen.set_color(15, 0)
		self.camera = Camera(self, self.initial_pos, self.initial_rotation, size)
		self.camera.update_objects(objects)
		self.camera.update()
		self.map_ = self.camera.send_screen()

		self.actions = actions
		self.screen = screen
		self.size = size

		self.player_speed = 2
		self.player_rotation_speed = 90

		self.elapsed_time = 0
		self.last_time = time.time()
		self.start_time = time.time()

		self.loaded_map = loaded_map
		self.is_maze = is_maze
		if is_maze:
			self.visual_map = str(loaded_map).split("\n")
			self.maze_size = Vector2(loaded_map.w, loaded_map.h)
			self.map_name += " maze"


	def print_map(self):
		self.screen.gotoXY(1, 1)
		print()
		if self.is_maze:
			self.loaded_map.update_player_pos(self.camera.pos)
			self.visual_map = str(self.loaded_map).split("\n")
		for y in range(len(self.map_)):
			strip = "".join(self.map_[y])
			if self.is_maze and y <= self.maze_size.y:
				strip = "   " + self.visual_map[y] + strip[self.maze_size.x * 2 + 5:]
			print(strip)

		print("     FPS:", int(1 / self.elapsed_time), " ")

		# if self.visual_map != None:
		# 	self.loaded_map.update_player_pos(self.camera.pos)
		# 	self.visual_map = str(self.loaded_map)
		# 	self.screen.gotoXY(0, 1)
		# 	print(self.visual_map)

	def update(self):
		self.elapsed_time = time.time() - self.last_time
		self.last_time = time.time()		

		if self.actions.has("quit"):
			self.screen.clear()
			self.screen.gotoXY(1, 1)
			quit()

		self.player_movement()

		self.camera.update()

		if self.escaped:
			return WinScreen(self.screen, self.actions, self.map_name, time.time() - self.start_time, self.size)

		self.print_map()

		return self

	def player_movement(self):
		if self.actions.has("left"):
			self.camera.rotation += self.player_rotation_speed * self.elapsed_time
			self.camera.rotation %= 360
		if self.actions.has("right"):
			self.camera.rotation -= self.player_rotation_speed * self.elapsed_time
			self.camera.rotation %= 360
		if self.actions.has("back"):
			self.camera.move(-self.player_speed * self.elapsed_time)
		if self.actions.has("forward"):
			self.camera.move(self.player_speed * self.elapsed_time)

	def escape(self):
		self.escaped = True