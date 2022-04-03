def coloured(text="", col="", bg="", clear=True):
	res = text
	txt_col = TxtColour.colour_names.get(col)
	bg_col = BgColour.colour_names.get(bg)
	if txt_col != None:
		res = txt_col + res
	if bg_col != None:
		res = bg_col + res
	if clear:
		res += TxtColour.Clear
	return res

class TxtColour():
	Black = "\u001b[30m"
	Red = "\u001b[31m"
	Green = "\u001b[32m"
	Yellow = "\u001b[33m"
	Blue = "\u001b[34m"
	Magenta = "\u001b[35m"
	Cyan = "\u001b[36m"
	White = "\u001b[37m"

	BrightBlack = "\u001b[30;1m"
	BrightRed = "\u001b[31;1m"
	BrightGreen = "\u001b[32;1m"
	BrightYellow = "\u001b[33;1m"
	BrightBlue = "\u001b[34;1m"
	BrightMagenta = "\u001b[35;1m"
	BrightCyan = "\u001b[36;1m"
	BrightWhite = "\u001b[37;1m"

	Clear = "\u001b[0m"

	colour_names = {
		"black": Black,
		"red": Red,
		"green": Green,
		"yellow": Yellow,
		"blue": Blue,
		"magenta": Magenta,
		"cyan": Cyan,
		"white": White,

		"bright_black": BrightBlack,
		"bright_red": BrightRed,
		"bright_green": BrightGreen,
		"bright_yellow": BrightYellow,
		"bright_blue": BrightBlue,
		"bright_magenta": BrightMagenta,
		"bright_cyan": BrightCyan,
		"bright_white": BrightWhite,

		"clear": Clear
	}



class BgColour():
	Black = "\u001b[40m"
	Red = "\u001b[41m"
	Green = "\u001b[42m"
	Yellow = "\u001b[43m"
	Blue = "\u001b[44m"
	Magenta = "\u001b[45m"
	Cyan = "\u001b[46m"
	White = "\u001b[47m"

	BrightBlack = "\u001b[40;1m"
	BrightRed = "\u001b[41;1m"
	BrightGreen = "\u001b[42;1m"
	BrightYellow = "\u001b[43;1m"
	BrightBlue = "\u001b[44;1m"
	BrightMagenta = "\u001b[45;1m"
	BrightCyan = "\u001b[46;1m"
	BrightWhite = "\u001b[47;1m"

	Clear = "\u001b[0m"

	colour_names = {
		"black": Black,
		"red": Red,
		"green": Green,
		"yellow": Yellow,
		"blue": Blue,
		"magenta": Magenta,
		"cyan": Cyan,
		"white": White,

		"bright_black": BrightBlack,
		"bright_red": BrightRed,
		"bright_green": BrightGreen,
		"bright_yellow": BrightYellow,
		"bright_blue": BrightBlue,
		"bright_magenta": BrightMagenta,
		"bright_cyan": BrightCyan,
		"bright_white": BrightWhite,

		"clear": Clear
	}
