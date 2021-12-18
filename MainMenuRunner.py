import random
import time
import os
from colorconsole import terminal
from Runner import Runner
from Vector2 import Vector2
from pynput import keyboard


class MainMenuRunner():
	def __init__(self, actions, size=Vector2(200, 55)):
		screen.set_color(15, 0)
		self.actions = actions
		self.size = size
		self.stage = 0
		self.map = []
		self.fill_map_stage0()
		self.pointer_pos = 0
		self.done = False

	def print_map(self):
		screen.gotoXY(1, 1)
		for y in range(self.size.y):
			print()
			for x in range(self.size.x):
				print(self.map[y][x], end='')
		print()


	def fill_map_stage0(self):
		self.map = []
		for y in range(self.size.y):
			self.map.append([])
			for x in range(self.size.x):
				if y == 0 or y == self.size.y - 1 or x == 0 or x == self.size.x - 1:
					self.map[y].append("█")
				else:
					self.map[y].append(" ")

		x_center = self.size.x // 2
		self.put_string("Please resize your screen so that the white outline looks like a rectangle", Vector2(x_center, 25), True)
		self.put_string("Press SPACE when ready", Vector2(x_center, 27), True)
		self.put_string("The project is dedicated to Dmitry Filin!", Vector2(x_center, 15), True)
		self.put_string("HAPPY BIRTDAY! =D", Vector2(x_center, 17), True)

	def fill_map_stage1(self):
		for y in range(self.size.y):
			for x in range(self.size.x):
				if y == 0 or y == self.size.y - 1 or x == 0 or x == self.size.x - 1:
					self.map[y][x] = "█"
				else:
					self.map[y][x] = " "
		x_center = self.size.x // 2
		self.put_string("Choose level:", Vector2(x_center, 5), True)
		self.put_string("(Use ARROW UP or ARROW DOWN to navigate, press SPACE when ready)", Vector2(x_center, 7), True)
		self.put_string("Use ESC to quit", Vector2(x_center, 48), True)
		self.put_string("Use W, S to move around", Vector2(x_center, 50), True)
		self.put_string("Use A, D to rotate the camera", Vector2(x_center, 52), True)
		for l in self.levels:
			if not ".txt" in l:
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

	def put_string(self, s, pos, centered=False):
		for i in range(len(s)):
			try:
				if centered:
					self.map[pos.y][pos.x - len(s) // 2 + i] = s[i]
				else:
					self.map[pos.y][pos.x + i] = s[i]
			except:
				pass

	def update(self, listener):
		if self.done:
			screen.clear()
			screen.gotoXY(1, 1)
			quit()

		if not self.stage == 2:
			self.print_map()
		if self.stage == 0:
			if self.actions.has("continue"):
				self.stage = 1
				self.actions.clear()
				self.levels = os.listdir("Custom_Maps")
				self.fill_map_stage1()
		if self.stage == 1:
			if self.actions.has("up") and self.pointer_pos > 0:
				self.pointer_pos -= 1
				self.actions.remove("up")
				self.fill_map_stage1()
			if self.actions.has("down") and self.pointer_pos < len(self.levels) - 1:
				self.pointer_pos += 1
				self.actions.remove("down")
				self.fill_map_stage1()
			if self.actions.has("continue"):
				self.actions.clear()
				self.game_runner = Runner(screen, self.actions, self.levels[self.pointer_pos], self.size)
				screen.clear()
				listener.on_press = self.game_runner.on_press
				listener.on_release = self.game_runner.on_release
				self.stage = 2
		if self.stage == 2:
			self.game_runner.update()

	def on_press(self, key):
		if key == keyboard.Key.esc:
			self.done = True
			return False
		if self.stage == 0:
			if key == keyboard.Key.space:
				self.actions.add("continue")
		if self.stage == 1:
			if key == keyboard.Key.up:
				self.actions.add("up")
			if key == keyboard.Key.down:
				self.actions.add("down")
			if key == keyboard.Key.space:
				self.actions.add("continue")

	def on_release(self, key):
		pass

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

	def clear(self):
		self.actions = []


if __name__ == "__main__":
	screen = terminal.get_terminal()
	screen.clear()
	terminal_size = os.get_terminal_size()

	actions = CurrentActions()
	runner = MainMenuRunner(actions, Vector2(terminal_size[0] - 2, terminal_size[1] - 2))

	listener = keyboard.Listener(on_press=runner.on_press, on_release=runner.on_release)
	listener.start()

	while True:	
		runner.update(listener)
		time.sleep(0.03)

listener.join()  
