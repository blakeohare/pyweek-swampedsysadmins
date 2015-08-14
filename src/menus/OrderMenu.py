from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text

IV_PRICE = 10
CUCUMBER_PRICE = 10
TAPE_PRICE = 15
JACKET_PRICE = 30
PHONE_PRICE = 200
TABLET_PRICE = 250
LAPTOP_PRICE = 300

class OrderMenu:
	def __init__(self, wrapper_menu, model):
		self.model = model
		self.elements = None
		self.parent = wrapper_menu
		self.tab = 'Stock'
		self.color = (100, 60, 60)
	
	def get_ui_elements(self):
		if self.elements == None:
			elements = []
			col1 = 10
			col2 = 300
			col3 = 400
			
			y = 20
			
			elements.append(create_ui_text("Treatment Gear", 'gray', col1, y))
			y += 30
			
			elements.append(create_ui_text('IV Bags', 'white', col1, y))
			elements.append(create_ui_text(self.model.inventory_ivs, 'white', col2, y))
			elements.append(create_ui_button('$' + str(IV_PRICE), self.buy_iv, col3, y, 100, 24, self.can_afford))
			y += 30
			
			elements.append(create_ui_text('Cucumbers', 'white', col1, y))
			elements.append(create_ui_text(self.model.inventory_cucumbers, 'white', col2, y))
			elements.append(create_ui_button('$' + str(CUCUMBER_PRICE), self.buy_cucumber, col3, y, 100, 24, self.can_afford))
			y += 30
			
			elements.append(create_ui_text('Tapes', 'white', col1, y))
			elements.append(create_ui_text(self.model.inventory_tapes, 'white', col2, y))
			elements.append(create_ui_button('$' + str(TAPE_PRICE), self.buy_tape, col3, y, 100, 24, self.can_afford))
			y += 30
			
			elements.append(create_ui_text('Jackets', 'white', col1, y))
			elements.append(create_ui_text(self.model.inventory_jackets, 'white', col2, y))
			elements.append(create_ui_button('$' + str(JACKET_PRICE), self.buy_jacket, col3, y, 100, 24, self.can_afford))
			y += 30
			
			y += 15
			
			elements.append(create_ui_text("Replacement Equipment", 'gray', col1, y))
			y += 30
			
			elements.append(create_ui_text('Phones', 'white', col1, y))
			elements.append(create_ui_text(self.model.inventory_phones, 'white', col2, y))
			elements.append(create_ui_button('$' + str(PHONE_PRICE), self.buy_phone, col3, y, 100, 24, self.can_afford))
			y += 30
			
			elements.append(create_ui_text('Tablets', 'white', col1, y))
			elements.append(create_ui_text(self.model.inventory_tablets, 'white', col2, y))
			elements.append(create_ui_button('$' + str(TABLET_PRICE), self.buy_tablet, col3, y, 100, 24, self.can_afford))
			y += 30
			
			elements.append(create_ui_text('Laptops', 'white', col1, y))
			elements.append(create_ui_text(self.model.inventory_laptops, 'white', col2, y))
			elements.append(create_ui_button('$'+ str(LAPTOP_PRICE), self.buy_laptop, col3, y, 100, 24, self.can_afford))
			y += 30
			
			self.elements = elements
		return self.elements
	
	def can_afford(self):
		return True
	
	def clear_cache(self):
		self.elements = None
		self.parent.elements = None
	
	def buy_iv(self):
		self.model.inventory_ivs += 1
		self.clear_cache()
	
	def buy_cucumber(self):
		self.model.inventory_cucumbers += 1
		self.clear_cache()
	
	def buy_tape(self):
		self.model.inventory_tapes += 1
		self.clear_cache()
	
	def buy_jacket(self):
		self.model.inventory_jackets += 1
		self.clear_cache()
	
	def buy_laptop(self):
		self.model.inventory_laptops += 1
		self.clear_cache()
	
	def buy_phone(self):
		self.model.inventory_phones += 1
		self.clear_cache()
		
	def buy_tablet(self):
		self.model.inventory_tablets += 1
		self.clear_cache()