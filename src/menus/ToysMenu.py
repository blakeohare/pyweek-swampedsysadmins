from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text

class ToysMenu:
	def __init__(self, wrapper_menu, model):
		self.model = model
		self.elements = None
		self.parent = wrapper_menu
		self.tab = 'Toys'
		self.color = (100, 100, 40)
	
	def get_ui_elements(self):
		if self.elements == None:
			elements = []
			
			elements.append(create_ui_text('Howdy - TosyMenu', 'purple', 0, 0))
			
			self.elements = elements
		return self.elements
	