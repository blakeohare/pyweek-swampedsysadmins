
class Event:
	def __init__(self, type, x, y, left_button):
		self.mousedown = type == 'mousedown'
		self.mouseup = type == 'mouseup'
		self.mousemove = type == 'mousemove'
		self.x = x
		self.y = y
		self.left = left_button
		self.right = not left_button
