import random
import os
from colorconsole import terminal
from Vector2 import Vector2
from pynput import keyboard
from Loader import Loader
from CurrentActions import CurrentActions
from Menu import Menu
from Title import Title
from WinScreen import WinScreen


if __name__ == "__main__":
	screen = terminal.get_terminal()
	screen.clear()
	terminal_size = os.get_terminal_size()

	actions = CurrentActions()
	# runner = Menu(screen, actions, Vector2(terminal_size[0] - 2, terminal_size[1] - 5))
	runner = Title(screen, actions, Vector2(terminal_size[0] - 2, terminal_size[1] - 5))
	# runner = WinScreen(screen, actions, "test map", 124.5678, Vector2(terminal_size[0] - 2, terminal_size[1] - 5))

	listener = keyboard.Listener(on_press=actions.on_press, on_release=actions.on_release)
	listener.start()

	while True:
		runner = runner.update()
		# time.sleep(0.01)

	listener.join()  
