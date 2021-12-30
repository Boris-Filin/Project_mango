import math


class Angle:
	def __init__(self, angle=0, in_rads=False, clamp=True):
		self.clamp = clamp
		if not in_rads:
			self.deg = angle
		else:
			self.deg = angle / math.pi * 180

	@property
	def deg(self):
		return self._deg

	@deg.setter
	def deg(self, new_deg):
		if not self.clamp:
			self._deg = new_deg
		self._deg = new_deg % 360
		if self._deg > 180:
			self._deg -= 360

	@property
	def rad(self):
		return self.deg * math.pi / 180

	@staticmethod
	def rads_to_degrees(rad):
		return rad / math.pi * 180

	def __add__(self, val):
		try:
			return Angle(self.deg + val.deg)
		except AttributeError:
			return Angle(self.deg + val)

	def __iadd__(self, val):
		try:
			self.deg += val.deg
		except AttributeError:
			self.deg += val
		return self

	def __sub__(self, val):
		try:
			return Angle(self.deg - val.deg)
		except AttributeError:
			return Angle(self.deg - val)

	def __isub__(self, val):
		try:
			self.deg -= val.deg
		except AttributeError:
			self.deg -= val
		return self

	def __mul__(self, val):
		return Angle(self.deg * val)

	def __imul__(self, val):
		self.deg *= val
		return self

	def __div__(self, val):
		if val == 0:
			raise ZeroDivisionError
		return Angle(self.deg / val)

	def __idiv__(self, val):
		if val == 0:
			raise ZeroDivisionError
		self.deg /= val
		return self

	def __str__(self):
		return "{}° ({} rad)".format(self.deg, self.rad)