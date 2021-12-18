import pygame
import random
import time
from multiprocessing import Process
from colorconsole import terminal
from threading import Thread
from GameMap import GameMap
from Camera import Camera
from Loader import Loader
from Tools import Vector2, Segment
from pynput import keyboard


screen = terminal.get_terminal()
screen.clear()
pygame.init()

class Runner():
	def __init__(self, actions, map_name, size=Vector2(200, 55)):
		loaded_map = Loader(map_name)
		objects = loaded_map.objects
		self.initial_pos = loaded_map.player_pos
		self.initial_rotation = loaded_map.player_rotation
		self.done = False

		screen.set_color(15, 0)
		self.camera = Camera(self.initial_pos, self.initial_rotation, size)
		self.camera.update_objects(objects)
		self.camera.update()
		self.map_ = self.camera.send_screen()

		self.actions = actions

	def print_map(self):
		screen.gotoXY(1, 1)
		print()
		for y in range(len(self.map_)):
			# print()
			# for x in range(len(self.map_[y])):
			# 	print(self.map_[y][x], end='')
			print("".join(self.map_[y]))

	def update(self):
		if self.done:
			screen.clear()
			screen.gotoXY(1, 1)
			quit()

		self.player_movement()

		self.camera.update()
		self.map_ = self.camera.send_screen()
		self.print_map()

	def on_press(self, key):
		if key == keyboard.Key.esc:
			self.done = True
			return False
		try:
			keychar = key.char
			if keychar == "a":
				self.actions.add("left")
			if keychar == "s":
				self.actions.add("back")
			if keychar == "w":
				self.actions.add("forward")
			if keychar == "d":
				self.actions.add("right")
		except:
			pass

	def on_release(self, key):
		try:
			keychar = key.char
			if keychar == "a":
				self.actions.remove("left")
			if keychar == "s":
				self.actions.remove("back")
			if keychar == "w":
				self.actions.remove("forward")
			if keychar == "d":
				self.actions.remove("right")
		except:
			pass

	def player_movement(self):
		if self.actions.has("left"):
			self.camera.rotation += 5
		if self.actions.has("right"):
			self.camera.rotation -= 5
		if self.actions.has("back"):
			self.camera.move(-0.1)
		if self.actions.has("forward"):
			self.camera.move(0.1)


class CurrentActions():
	def __init__(self):
		self.actions = []

	def add(self, action):
		if not action in self.actions:
			self.actions.append(action)

	def remove(self, action):
		if action in self.actions:
			self.actions.remove(action)

	def has(self, action):
		if action in self.actions:
			return True
		return False

	def leave_only(self, action):
		self.actions = [action]


# if __name__ == "__main__":
# 	actions = CurrentActions()

# 	runner = Runner(actions)
# 	while True:	
# 		runner.update()
# 		time.sleep(0.01)








