import pygame
from src.MagicPotato import MAGIC_POTATO
from src.constants import *
from src.FontEngine import TEXT

class OptionsMenu:
	def __init__(self, background_scene):
		self.next = None
		self.bg = background_scene
		self.buttons = {
			'full_screen': [0] * 4,
			'back': [0] * 4
		}
		self.cursor = (0, 0)
		self.currently_over = None
		
	def update(self, events, mouse_coords):
		self.cursor = mouse_coords
		
		for event in events:
			if event.mousedown:
				if self.currently_over != None:
					self.do_command(self.currently_over)
	
	def do_command(self, id):
		if id == 'full_screen':
			if MAGIC_POTATO.is_full_screen():
				MAGIC_POTATO.set_full_screen(False)
			else: MAGIC_POTATO.set_full_screen(True)
		elif id == 'back':
			pass
			# self.next = 
	
	def render(self, screen, render_counter):
		if self.bg != None:
			self.bg.render(screen, render_counter)
		
		pygame.draw.rect(screen, (40, 40, 40, 100), pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT))
		
		mx, my = self.cursor
		
		y = GAME_HEIGHT // 2
		x = GAME_WIDTH // 3
		
		current = None
		for option in [
			('Full Screen', 'full_screen'),
			('Back', 'back')
			]:
			
			label, id = option
			button = self.buttons[id]
			hover = mx > button[0] and mx < button[2] and my > button[1] and my < button[3]
			
			color = 'gray'
			if id == 'full_screen' and MAGIC_POTATO.is_full_screen(): ## until I figure out checkboxes.
				color = 'blue'
			
			if hover:
				current = id
				color = 'white'
			
			coords = TEXT.render(screen, label, color, x, y)
			self.buttons[id] = (x, y, coords[0], coords[1])
			y += 30 ## what this?
		self.currently_over = current