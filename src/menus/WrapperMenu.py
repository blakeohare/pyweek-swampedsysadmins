import pygame

from src.constants import *
from src.Util import *
from src.menus.GraphMenu import GraphMenu
from src.menus.HiringMenu import HiringMenu
from src.menus.OrderMenu import OrderMenu
from src.menus.ScoreMenu import ScoreMenu
from src.menus.ToysMenu import ToysMenu
from src.menus.UiElement import *

MENU_LEFT = 50
MENU_TOP = 50

MENU_WIDTH = GAME_WIDTH - MENU_LEFT * 2
MENU_HEIGHT = GAME_HEIGHT - MENU_TOP * 2

class WrapperMenu:
	def __init__(self, bg, model):
		self.next = None
		self.bg = bg
		self.model = model
		self.session = model.session
		self.devices = model.session.devices
		self.score_menu = ScoreMenu(self, model)
		self.graph_menu = GraphMenu(self, model)
		self.hiring_menu = HiringMenu(self, model)
		self.order_menu = OrderMenu(self, model)
		self.toys_menu = ToysMenu(self, model)
		self.ordered = [
			self.score_menu,
			self.order_menu,
			self.toys_menu,
			self.hiring_menu,
			self.graph_menu,
			]
		self.mouse_xy = (0, 0)
		self.tab_regions = [None] * len(self.ordered)
		
		self.active_menu = self.score_menu
		self.elements = None
	
	def update(self, events, mouse_xy):
		self.mouse_xy = mouse_xy
		for event in events:
			if event.mousedown:
				x = event.x - MENU_LEFT
				y = event.y - MENU_TOP
				for element in self.get_ui_elements():
					if element.type == 'BUTTON' and element.is_enabled():
						if x >= element.left and x < element.right and y >= element.top and y < element.bottom:
							element.action()
							break
				
				mx, my = self.mouse_xy
				for i in range(len(self.tab_regions)):
					region = self.tab_regions[i]
					if region != None:
						if mx >= region[0] and mx < region[2] and my >= region[1] and my < region[3]:
							self.active_menu = self.ordered[i]
							self.elements = None
							break
							
	def get_ui_elements(self):
		if self.elements == None:
			elements = self.active_menu.get_ui_elements()
			elements.append(create_ui_button('Okidoke', self.okidoke, MENU_WIDTH - 170, MENU_HEIGHT - 52, 150, 32, lambda:True))
			self.elements = elements
		return self.elements
	
	def render(self, screen, rc):
		self.bg.render(screen, rc)
		x, y = self.mouse_xy
		px = MENU_LEFT + 8
		py = MENU_TOP - 32
		
		alpha = 230
		
		for i in range(len(self.ordered)):
			tab = self.ordered[i]
			width = len(tab.tab) * 16 + 16
			draw_alpha_rectangle(screen, px, py, width, 32, tab.color[0], tab.color[1], tab.color[2], alpha)
			TEXT.render(screen, tab.tab, 'white', px + 14, py + 8)
			
			left = px
			right = px + width
			top = py
			bottom = py + 32
			
			self.tab_regions[i] = (left, top, right, bottom)
			
			px += width + 6
		
		rgb = self.active_menu.color
		
		draw_alpha_rectangle(screen, MENU_LEFT, MENU_TOP, MENU_WIDTH, MENU_HEIGHT, rgb[0], rgb[1], rgb[2], alpha)
		
		for element in self.get_ui_elements():
			element.render(screen, MENU_LEFT, MENU_TOP, self.mouse_xy, rc)
	
	def okidoke(self):
		from src.PlayScene import PlayScene
		self.model.increment_level()
		self.next = PlayScene(None, self.model)
