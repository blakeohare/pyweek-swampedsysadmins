from src.constants import *

class Event:
	def __init__(self, type, x, y, left_button):
		self.mousedown = type == 'mousedown'
		self.mouseup = type == 'mouseup'
		self.mousemove = type == 'mousemove'
		
		self.x = GAME_WIDTH * x // SCREEN_WIDTH
		self.y = GAME_HEIGHT * y // SCREEN_HEIGHT
		
		self.left = left_button
		self.right = not left_button
