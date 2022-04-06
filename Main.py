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
	os.system("")
	x, y = os.get_terminal_size()

	actions = CurrentActions()
	runner = Title(actions, Vector2(x - 1, y - 4))

	listener = keyboard.Listener(on_press=actions.on_press, on_release=actions.on_release)
	listener.start()

	while True:
		runner = runner.update()

	listener.join()  
