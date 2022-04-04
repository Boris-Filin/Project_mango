from Runner import Runner
from colorconsole import terminal
from Loader import Loader
import os
from Main import CurrentActions
from Vector2 import Vector2
from pynput import keyboard


if __name__ == "__main__":
	screen = terminal.get_terminal()
	screen.clear()
	terminal_size = os.get_terminal_size()

	levels = os.listdir("Custom_Maps")
	loaded_map = Loader(levels[0], screen)

	actions = CurrentActions()
	runner = Runner(screen, actions, loaded_map, Vector2(terminal_size[0] - 2, terminal_size[1] - 5))

	listener = keyboard.Listener(on_press=runner.on_press, on_release=runner.on_release)
	listener.start()

	while True:	
		runner.update()
		# time.sleep(0.01)

	listener.join()


# class C1():
# 	def __init__(self, **kwargs):
# 		self.m(**kwargs)

# 	def m(self, x, y, answ):
# 		# print(kwargs.get("answ"))
# 		print(answ)
# 		# for a in args:
# 		# 	print(a)
# 		# print(x)



# c = C1(x=1, y=2, answ=42)


# print(handle_tags("s 1 1 0 0 {slab:True, fill:#}"))