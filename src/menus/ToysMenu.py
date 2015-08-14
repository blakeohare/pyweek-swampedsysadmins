from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text
from src.menus.UiElement import create_ui_image
from src.menus.UiElement import create_ui_image_list

from src.ImageLibrary import IMAGES

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

			col1 = 10
			col2 = 200
			col3 = 400
			
			row1 = 10
			row2 = 150
			row3 = row2 * 2 - row1
			
			elements.append(create_ui_image_list([
				IMAGES.get('furniture/lava_lamp0.png'),
				IMAGES.get('furniture/lava_lamp1.png'),
				IMAGES.get('furniture/lava_lamp2.png'),
				IMAGES.get('furniture/lava_lamp3.png')], col1, row1))
			
			elements.append(create_ui_image(IMAGES.get('furniture/the_doll.png'), col2, row1))
			
			elements.append(create_ui_image(IMAGES.get('furniture/potted_flower.png'), col3, row1))
			
			elements.append(create_ui_image(IMAGES.get('furniture/bean_bag.png'), col1, row2))
			
			elements.append(create_ui_image(IMAGES.get('furniture/foosball.png'), col2, row2))
				
			
			self.elements = elements
		return self.elements
	