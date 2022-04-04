from pynput import keyboard


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

	def on_press(self, key):
		if key == keyboard.Key.esc:
			self.add("quit")
		if key == keyboard.Key.space:
			self.add("continue")
		if key == keyboard.Key.up:
			self.add("arrow_up")
		if key == keyboard.Key.down:
			self.add("arrow_down")
		if key == keyboard.Key.left:
			self.add("arrow_left")
		if key == keyboard.Key.right:
			self.add("arrow_right")
		try:
			keychar = key.char
			if keychar == "a":
				self.add("left")
			if keychar == "s":
				self.add("back")
			if keychar == "w":
				self.add("forward")
			if keychar == "d":
				self.add("right")
		except:
			pass

	def on_release(self, key):
		if key == keyboard.Key.space:
			self.remove("continue")
		if key == keyboard.Key.up:
			self.remove("arrow_up")
		if key == keyboard.Key.down:
			self.remove("arrow_down")
		if key == keyboard.Key.left:
			self.remove("arrow_left")
		if key == keyboard.Key.right:
			self.remove("arrow_right")
		try:
			keychar = key.char
			if keychar == "a":
				self.remove("left")
			if keychar == "s":
				self.remove("back")
			if keychar == "w":
				self.remove("forward")
			if keychar == "d":
				self.remove("right")
		except:
			pass