from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text

class OrderMenu:
	def __init__(self, wrapper_menu, model):
		self.model = model
		self.elements = None
		self.parent = wrapper_menu
		self.tab = 'Stock'
		self.color = (140, 40, 40)
	
	def get_ui_elements(self):
		if self.elements == None:
			elements = []
			
			elements.append(create_ui_text('Howdy - OrderMenu', 'green', 0, 0))
			
			self.elements = elements
		return self.elements
	