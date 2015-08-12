from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text

class HiringMenu:
	def __init__(self, wrapper_menu, model):
		self.model = model
		self.elements = None
		self.parent = wrapper_menu
	
	def get_ui_elements(self):
		if self.elements == None:
			elements = []
			
			elements.append(create_ui_text('Howdy - HiringMenu', 'purple', 0, 0))
			
			self.elements = elements
		return self.elements
	