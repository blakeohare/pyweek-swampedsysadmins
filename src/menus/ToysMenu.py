from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text
from src.menus.UiElement import create_ui_image
from src.menus.UiElement import create_ui_image_list
from src.menus.UiElement import create_ui_hover_region

from src.menus.PlaceFurniture import PlaceFurnitureMenu

from src.ImageLibrary import IMAGES

LAVA_PRICE = 50
PLUSH_PRICE = 75
PLANT_PRICE = 100
BEAN_BAG_PRICE = 200
FOOSBALL_PRICE = 500


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

			col1 = 25
			col2 = 230
			col3 = 400
			
			row1 = 10
			row2 = 150
			row3 = row2 * 2 - row1
			
			lava_lamp_image = create_ui_image_list([
				IMAGES.get('furniture/lava_lamp0.png'),
				IMAGES.get('furniture/lava_lamp1.png'),
				IMAGES.get('furniture/lava_lamp2.png'),
				IMAGES.get('furniture/lava_lamp3.png')], col1 + 32, row1)
			elements.append(lava_lamp_image)
			elements.append(create_ui_button('$' + str(LAVA_PRICE), self.buy_lava, col1, row1 + 70, 100, 24, lambda:self.can_afford(LAVA_PRICE)))
			
			plush_image = create_ui_image(IMAGES.get('furniture/the_doll.png'), col2 + 12, row1)
			elements.append(plush_image)
			elements.append(create_ui_button('$' + str(PLUSH_PRICE), self.buy_plush, col2, row1 + 70, 100, 24, lambda:self.can_afford(PLUSH_PRICE)))
			
			plant_image = create_ui_image(IMAGES.get('furniture/potted_flower.png'), col3 + 32, row1)
			elements.append(plant_image)
			elements.append(create_ui_button('$' + str(PLANT_PRICE), self.buy_plant, col3, row1 + 70, 100, 24, lambda:self.can_afford(PLANT_PRICE)))
			
			bean_bag_image = create_ui_image(IMAGES.get('furniture/bean_bag.png'), col1 + 16, row2)
			elements.append(bean_bag_image)
			elements.append(create_ui_button('$' + str(BEAN_BAG_PRICE), self.buy_bean_bag, col1, row2 + 70, 100, 24, lambda:self.can_afford(BEAN_BAG_PRICE)))
			
			foosball_image = create_ui_image(IMAGES.get('furniture/foosball.png'), col2, row2)
			elements.append(foosball_image)
			elements.append(create_ui_button('$' + str(FOOSBALL_PRICE), self.buy_foosball, col2, row2 + 70, 100, 24, lambda:self.can_afford(FOOSBALL_PRICE)))
			
			description = create_ui_text('Mouse over item for description.', 'white', col1, row3 - 32)
			elements.append(description)
			
			
			descriptions = [
				(lava_lamp_image, "Lava lamp:\n+2% productivity, small radius."),
				(plush_image, "Giant plush:\n-10% chance of sad/angry/crazy\ndevices."),
				(plant_image, "Famous flower:\n+10% productivity, small radius."),
				(bean_bag_image, "Bean Bag:\n+3% productivity everywhere."),
				(foosball_image, "Miniature Sportsball:\n-5% productivity, devices don't\nland near it. Limit 1"),
			]
			
			for t in descriptions:
				img, text = t
				elements.append(create_ui_hover_region(description, img.left, img.top, img.right, img.bottom, text))
			
			
			self.elements = elements
		return self.elements
	
	def buy_lava(self):
		self.parent.next = PlaceFurnitureMenu(self.model, self.parent, '1')
	
	def buy_plush(self):
		self.parent.next = PlaceFurnitureMenu(self.model, self.parent, '2')
	
	def buy_plant(self):
		self.parent.next = PlaceFurnitureMenu(self.model, self.parent, '3')
	
	def buy_bean_bag(self):
		self.parent.next = PlaceFurnitureMenu(self.model, self.parent, '4')
	
	def buy_foosball(self):
		self.parent.next = PlaceFurnitureMenu(self.model, self.parent, '5')
	
	def can_afford(self, price):
		return self.model.budget >= price