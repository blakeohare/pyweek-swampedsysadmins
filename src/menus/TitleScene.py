import pygame
from src.constants import *
from src.ImageLibrary import IMAGES
from src.FontEngine import TEXT

class TitleScene:
	def __init__(self):
		self.next = None
		self.buttons = {
			'new_game': [0] * 4,
			'options': [0] * 4,
			'exit': [0] * 4
		}
		self.cursor = (0, 0)
	
	def update(self, events, mouse_pos):
		self.cursor = mouse_pos
	
	def render(self, screen, rc):
		bg = IMAGES.get('menus/title.png')
		screen.blit(bg, (0, 0))
		
		mx, my = self.cursor
		
		y = GAME_HEIGHT // 2
		x = GAME_WIDTH // 3
		
		for option in [
			('New Game', 'new_game'),
			('Options', 'options'),
			('Exit', 'exit')
			]:
			
			label, id = option
			button = self.buttons[id]
			hover = mx > button[0] and mx < button[2] and my > button[1] and my < button[3]
			
			coords = TEXT.render(screen, label, 'white' if hover else 'gray', x, y)
			self.buttons[id] = (x, y, coords[0], coords[1])
			y += 30
		