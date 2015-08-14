from src.Staff import Staff
from src.Session import Session

from src.menus.OrderMenu import PHONE_PRICE
from src.menus.OrderMenu import TABLET_PRICE
from src.menus.OrderMenu import LAPTOP_PRICE

class Model:
	def __init__(self, starting_level):
		self.staff = [Staff('man0'), Staff('woman0')]
		self.session = Session(starting_level) # 0 for tutorial
		
		self.budget = 1000
		self.inventory_ivs = 15
		self.inventory_cucumbers = 5
		self.inventory_tapes = 5
		self.inventory_jackets = 5
		self.inventory_laptops = 3
		self.inventory_phones = 3
		self.inventory_tablets = 3
		
		
	def increment_level(self):
		level_id = self.session.level + 1
		self.session = Session(level_id)
	
	def special_order_laptop(self):
		self.budget -= LAPTOP_PRICE
	
	def special_order_phone(self):
		self.budget -= PHONE_PRICE
	
	def special_order_tablet(self):
		self.budget -= TABLET_PRICE