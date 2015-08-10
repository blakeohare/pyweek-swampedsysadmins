import pygame
from src.constants import *

_KEYS = {
	pygame.K_RETURN: 'enter',
	pygame.K_SPACE: 'space',
}
for i in range(26):
	_KEYS[pygame.K_a + i] = chr(ord('a') + i) 
for i in range(1, 12):
	_KEYS[pygame.K_F1 + i - 1] = 'f' + str(i)


class Event:
	def __init__(self, type, x, y, left_button):
		self.mousedown = type == 'mousedown'
		self.mouseup = type == 'mouseup'
		self.mousemove = type == 'mousemove'
		self.keydown = type == 'keydown'
		
		if self.keydown:
			self.key = _KEYS.get(x, 'unknown')
			self.x = 0
			self.y = 0
		else:
			self.key = None
			self.x = GAME_WIDTH * x // SCREEN_SIZE[0]
			self.y = GAME_HEIGHT * y // SCREEN_SIZE[1]
			
			
		
		self.left = left_button
		self.right = not left_button
