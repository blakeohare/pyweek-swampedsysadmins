import pygame
from src.constants import *
from src.ImageLibrary import IMAGES
from src.FontEngine import TEXT
from src.PlayScene import PlayScene
from src.menus.OptionsMenu import OptionsMenu
from src.Sound import SND

class TitleScene:
	def __init__(self):
		self.next = None
		self.buttons = {
			'new_game': [0] * 4,
			'tutorial': [0] * 4,
			'options': [0] * 4,
			'exit': [0] * 4
		}
		self.cursor = (0, 0)
		self.currently_over = None
		self.first = True
	
	def update(self, events, mouse_pos):
		self.cursor = mouse_pos
		
		if self.first:
			self.first = False
			SND.music_title()
		
		for event in events:
			if event.mousedown:
				if self.currently_over != None:
					self.do_command(self.currently_over)
			elif event.keydown:
				if event.key == 'enter':
					self.do_command('new_game')
				elif event.key == 't':
					self.do_command('tutorial')
				elif event.key == 'o':
					self.do_command('options')
	
	def do_command(self, id):
		if id == 'new_game':
			self.next = PlayScene(1)
		
		elif id == 'tutorial':
			self.next = PlayScene(0)
		
		elif id == 'options':
			self.next = OptionsMenu(None)
		
		elif id == 'exit':
			self.next = 'exit'
	
	def render(self, screen, rc):
		bg = IMAGES.get('menus/title.png')
		screen.blit(bg, (0, 0))
		
		mx, my = self.cursor
		
		y = GAME_HEIGHT // 2
		x = GAME_WIDTH // 5
		
		current = None
		for option in [
			('New Game', 'new_game'),
			('Tutorial', 'tutorial'),
			('Options', 'options'),
			('Exit', 'exit')
			]:
			
			label, id = option
			button = self.buttons[id]
			hover = mx > button[0] and mx < button[2] and my > button[1] and my < button[3]
			
			if hover:
				current = id
			
			coords = TEXT.render(screen, label, 'yellow' if hover else 'white', x, y)
			self.buttons[id] = (x, y, coords[0], coords[1])
			y += 30
		self.currently_over = current