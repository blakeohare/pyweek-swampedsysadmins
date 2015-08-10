from src.Staff import Staff
from src.Session import Session

class Model:
	def __init__(self, starting_level):
		self.staff = [Staff('simon')]
		self.session = Session(starting_level) # 0 for tutorial
	