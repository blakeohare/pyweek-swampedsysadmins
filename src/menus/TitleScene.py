import pygame

from src.ImageLibrary import IMAGES

class TitleScene:
	def __init__(self):
		self.next = None
	
	def update(self, events, mouse_pos):
		pass
	
	def render(self, screen, rc):
		bg = IMAGES.get('menus/title.png')
		screen.blit(bg, (0, 0))