from src.Staff import Staff
from src.Session import Session

class Model:
	def __init__(self, starting_level):
		self.staff = [Staff('simon')]
		self.session = Session(starting_level) # 0 for tutorial
		
		self.inventory_ivs = 15
		self.inventory_cucumbers = 5
		self.inventory_towels = 5
		self.inventory_tapes = 5
		self.inventory_jackets = 5
		self.inventory_laptops = 3
		self.inventory_phones = 3
		self.inventory_tablets = 3
		
		
	