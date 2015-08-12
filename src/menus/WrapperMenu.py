import pygame

from src.constants import *
from src.Util import *
from src.menus.GraphMenu import GraphMenu
from src.menus.HiringMenu import HiringMenu
from src.menus.OrderMenu import OrderMenu
from src.menus.ScoreMenu import ScoreMenu


MENU_LEFT = 50
MENU_TOP = 50

MENU_WIDTH = GAME_WIDTH - MENU_LEFT * 2
MENU_HEIGHT = GAME_HEIGHT - MENU_TOP * 2

class WrapperMenu:
	def __init__(self, bg, model):
		self.next = None
		self.bg = bg
		self.model = model
		self.score_menu = ScoreMenu(self, model)
		self.graph_menu = GraphMenu(self, model)
		self.hiring_menu = HiringMenu(self, model)
		self.order_menu = OrderMenu(self, model)
		self.ordered = [
			self.score_menu,
			self.order_menu,
			self.hiring_menu,
			self.graph_menu
			]
		self.mouse_xy = (0, 0)
		
		self.active_menu = self.score_menu
	
	def update(self, events, mouse_xy):
		self.mouse_xy = mouse_xy
		for event in events:
			if event.mousedown:
				x = event.x - MENU_LEFT
				y = event.y - MENU_TOP
				for element in self.active_menu.get_ui_elements():
					if element.type == 'BUTTON' and element.is_enabled():
						if x >= element.left and x < element.right and y >= element.top and y < element.bottom:
							element.action()
							break
	
	def render(self, screen, rc):
		self.bg.render(screen, rc)
		
		draw_alpha_rectangle(screen, MENU_LEFT, MENU_TOP, MENU_WIDTH, MENU_HEIGHT, 40, 40, 40, 210)
		
		elements = self.active_menu.get_ui_elements()
		for element in elements:
			element.render(screen, MENU_LEFT, MENU_TOP, self.mouse_xy, rc)
		