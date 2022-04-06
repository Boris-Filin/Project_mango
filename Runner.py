import random
import time
from colorconsole import terminal
from Camera import Camera
from Loader import Loader
from Vector2 import Vector2
from WinScreen import WinScreen

class Runner():
	def __init__(self, screen, actions, loaded_map, map_name, size=Vector2(200, 55), is_maze=False):
		objects = loaded_map.objects
		self.map_name = map_name
		self.initial_pos = loaded_map.player_pos
		self.initial_rotation = loaded_map.player_rotation
		self.escaped = False

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
		# Go to upper left corner
		print("\033[1;1H")
		print()

		# Minimap rendering
		if self.is_maze:
			self.loaded_map.update_player_pos(self.camera.pos)
			self.visual_map = str(self.loaded_map).split("\n")

		# Output the horizontal line
		for y in range(len(self.map_)):
			strip = "".join(self.map_[y])
			if self.is_maze and y <= self.maze_size.y:
				strip = "   " + self.visual_map[y] + strip[self.maze_size.x * 2 + 5:]
			print(strip)

		# Output FPS count for debugging purposes
		print("     FPS:", int(1 / self.elapsed_time), " ")


	def update(self):
		# Calculate the time since the last frame
		self.elapsed_time = time.time() - self.last_time
		self.last_time = time.time()		

		# Check if ESCAPE was pressed
		if self.actions.has("quit"):
			self.screen.clear()
			self.screen.gotoXY(1, 1)
			quit()

		# Move player
		self.player_movement()

		# Check if the maze was completed		
		if self.escaped:
			return WinScreen(self.screen, self.actions,
				self.map_name, time.time() - self.start_time, self.size)

		# RENDER THE IMAGE
		self.camera.update()

		# output the rendered image
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