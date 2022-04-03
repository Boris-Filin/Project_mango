from Segment import Segment


class Wall():
	def __init__(self, segment, tags={}):
		self.segment = segment
		self.tags = {} if tags is None else tags

		self.filling = "" if self.tags.get("fill") is None else self.tags["fill"]
		# self.slabbable = True
		self.slabbable = True if self.tags.get("slab") is None else self.tags["slab"].lower() == "true"
		self.is_exit = False if self.tags.get("is_exit") is None else self.tags["is_exit"].lower() == "true"
