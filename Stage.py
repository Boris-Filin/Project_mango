import time


class Stage():
	def fill_map():
		pass

	def prime_map(self):
		self.map_ = []
		for y in range(self.size.y):
			self.map_.append([])
			for x in range(self.size.x):
				self.map_[y].append(" ")

	def print_map(self):
		self.screen.gotoXY(1, 1)
		for y in range(self.size.y):
			print()
			for x in range(self.size.x):
				print(self.map_[y][x], end='')
		print()

	def put_string(self, s, pos, centered=False):
		for i in range(len(s)):
			try:
				if centered:
					self.map_[pos.y][pos.x - len(s) // 2 + i] = s[i]
				else:
					self.map_[pos.y][pos.x + i] = s[i]
			except:
				pass

	def update(self):
		self.elapsed_time = time.time() - self.prev_frame_time
		self.prev_frame_time = time.time()

		if self.actions.has("quit"):
			self.screen.clear()
			self.screen.gotoXY(1, 1)
			quit()

		next_stage = self.stage_update()
		if next_stage != None:
			return next_stage

		self.fill_map()
		self.print_map()
		if self.elapsed_time != 0:
			print("     FPS:", int(1 / self.elapsed_time), " ")

		return self

	def stage_update(self):
		pass