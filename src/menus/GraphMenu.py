from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text

class GraphMenu:
	def __init__(self, wrapper_menu, model):
		self.model = model
		self.elements = None
		self.parent = wrapper_menu
	
	def get_ui_elements(self):
		if self.elements == None:
			elements = []
			
			elements.append(create_ui_text('Howdy - GraphMenu', 'yellow', 0, 0))
			
			self.elements = elements
		return self.elements
	