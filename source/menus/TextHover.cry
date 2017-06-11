from src.Util import *
from src.FontEngine import TEXT

class TextHover:
	def __init__(self, pages, bg):
		from src.menus.UiElement import create_ui_button
		self.pages = pages
		self.next = None
		self.bg = bg
		self.mouse_xy = (0, 0)
		self.button = create_ui_button('Okidoke', self.press_okidoke, 300, 400, 150, 24, lambda:True)
	
	def update(self, events, mouse_xy):
		
		self.mouse_xy = mouse_xy
		for event in events:
			if event.mousedown:
				x = event.x
				y = event.y
				element = self.button
				if x >= element.left and x < element.right and y >= element.top and y < element.bottom:
					element.action()
				

	def press_okidoke(self):
		if len(self.pages) == 1:
			self.next = self.bg
		else:
			self.pages = self.pages[1:]

	def render(self, screen, rc):
		self.bg.render(screen, rc)
		if len(self.pages) > 0:
			draw_alpha_rectangle(screen, 50, 50, 540, 380, 40, 40, 40, 180)

			self.button.render(screen, 0, 0, self.mouse_xy, rc)
			
			lines = self.pages[0].split('\n')
			x = 60
			y = 60
			for line in lines:
				TEXT.render(screen, line, 'white', x, y)
				y += 24
				
		