import pygame
from src.MagicPotato import MAGIC_POTATO
from src.constants import *

class OptionsMenu:
	def __init__(self, background_scene):
		self.next = None
		self.bg = background_scene
		MAGIC_POTATO.set_full_screen(True)
	
	def update(self, events, mouse_coords):
		pass
	
	def render(self, screen, render_counter):
		if self.bg != None:
			self.bg.render(screen, render_counter)
		
		pygame.draw.rect(screen, (40, 40, 40, 100), pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT))
		
		# TODO: draw menu
	
	