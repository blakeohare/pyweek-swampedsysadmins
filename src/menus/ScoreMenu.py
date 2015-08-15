from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text

class ScoreMenu:
	def __init__(self, wrapper_menu, model):
		self.model = model
		self.elements = None
		self.parent = wrapper_menu
		self.tab = 'Report'
		self.color = (40, 40, 40)
	
	def get_ui_elements(self):
		if self.elements == None:
			session = self.model.session
			
			elements = []
			
			#elements.append(create_ui_text('Howdy - ScoreMenu', 'red', 5, 5))
			
			col0 = 5
			col1 = 200
			col2 = 320
			col3 = 430
			
			row0 = 15
			row1 = 50
			row2 = 90
			row3 = 130
			
			row4 = 190
			row5 = 230
			
			elements.append(create_ui_text('Fixed', 'white', col0, row1))
			elements.append(create_ui_text('Replaced', 'white', col0, row2))
			elements.append(create_ui_text('Special Order', 'white', col0, row3))
			
			elements.append(create_ui_text('Laptops', 'white', col1, row0))
			elements.append(create_ui_text('Phones', 'white', col2, row0))
			elements.append(create_ui_text('Tablets', 'white', col3, row0))
			
			counts = {}
			for device in session.devices:
				key = device.device_type + 's_' + device.resolution
				counts[key] = counts.get(key, 0) + 1
			
			col1 = 230
			
			elements.append(self.create_grid_element(counts.get('laptops_treated', 0), col1, row1, 'green'))
			elements.append(self.create_grid_element(counts.get('phones_treated', 0), col2, row1, 'green'))
			elements.append(self.create_grid_element(counts.get('tablets_treated', 0), col3, row1, 'green'))
			
			elements.append(self.create_grid_element(counts.get('laptops_replaced', 0), col1, row2, 'orange'))
			elements.append(self.create_grid_element(counts.get('phones_replaced', 0), col2, row2, 'orange'))
			elements.append(self.create_grid_element(counts.get('tablets_replaced', 0), col3, row2, 'orange'))
			
			elements.append(self.create_grid_element(counts.get('laptops_ordered', 0), col1, row3, 'red'))
			elements.append(self.create_grid_element(counts.get('phones_ordered', 0), col2, row3, 'red'))
			elements.append(self.create_grid_element(counts.get('tablets_ordered', 0), col3, row3, 'red'))
			
			elements.append(create_ui_text('Next Budget Allowance:', 'white', col0, row4))
			b = self.model.reward.calculate_next_budget()
			elements.append(create_ui_text('$' + str(b), 'green' if b > 0 else 'red', col2, row4))
			
			elements.append(create_ui_text('Average Turnaround:', 'white', col0, row5))
			t = self.model.reward.get_avg_turnaround()
			elements.append(create_ui_text('{0:.2g}'.format(t) + ' second' + ('' if t == 1 else 's'), 'gray', col2, row5))
			
			self.elements = elements
		return self.elements
	
	def create_grid_element(self, num, x, y, value_color):
		color = 'gray'
		if num > 0: color = value_color
		return create_ui_text(num, color, x, y)