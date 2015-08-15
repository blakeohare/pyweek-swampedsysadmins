from src.menus.UiElement import create_ui_button
from src.menus.UiElement import create_ui_text
from src.menus.UiElement import create_ui_image_list

class HiringMenu:
	def __init__(self, wrapper_menu, model):
		self.model = model
		self.elements = None
		self.parent = wrapper_menu
		self.tab = 'HR'
		self.color = (40, 60, 100)
		
		
	
	def get_ui_elements(self):
		if self.elements == None:
			from src.Staff import Staff
			staff_id = len(self.model.staff)
			person = Staff(staff_id)
			person.direction = 's'
			person.moving = True
			images = []
			images.append(person.get_current_image(0))
			images.append(person.get_current_image(3))
			images.append(person.get_current_image(6))
			images.append(person.get_current_image(9))
			
			elements = []
			
			elements.append(create_ui_text('Hire new employee', 'white', 20, 20))
			
			elements.append(create_ui_image_list(images, 100, 60))
			
			y = 150
			col0 = 20
			col1 = 200
			elements.append(create_ui_text('Asking Salary:', 'white', col0, y))
			elements.append(create_ui_text('$100 / game', 'green', col1, y))
			
			y += 30
			elements.append(create_ui_text('Current Payroll:', 'white', col0, y))
			elements.append(create_ui_text('-$' + str(staff_id * 100), 'red', col1, y))
			
			self.elements = elements
		return self.elements
	