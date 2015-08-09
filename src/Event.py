from src.constants import *

class Event:
	def __init__(self, type, x, y, left_button):
		self.mousedown = type == 'mousedown'
		self.mouseup = type == 'mouseup'
		self.mousemove = type == 'mousemove'
		
		self.x = GAME_WIDTH * x // SCREEN_SIZE[0]
		self.y = GAME_HEIGHT * y // SCREEN_SIZE[1]
		
		self.left = left_button
		self.right = not left_button
