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
		self.staff_member = None
		self.hired = False
		
		
	
	def get_ui_elements(self):
		if self.elements == None:
			from src.Staff import Staff
			staff_id = len(self.model.staff)
			if self.staff_member == None:
				person = Staff(staff_id)
				self.staff_member = person
			else:
				person = self.staff_member
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
			col1 = 300
			elements.append(create_ui_text('Asking Salary:', 'white', col0, y))
			elements.append(create_ui_text('$100 / game', 'green', col1, y))
			
			y += 30
			elements.append(create_ui_text('Current Payroll:', 'white', col0, y))
			elements.append(create_ui_text('-$' + str(staff_id * 100), 'red', col1, y))
			
			y += 50
			elements.append(create_ui_button('Hire', self.hire, 100, y, 100, 24, self.can_hire))
			
			self.elements = elements
		return self.elements
	
	def can_hire(self):
		return not self.hired
	
	def hire(self):
		from src.Staff import Staff
		new_hire = Staff(self.staff_member.id)
		new_hire.x = 32 * 5
		new_hire.y = 32 * 5
		self.model.staff.append(new_hire)
		self.hired = True
		self.elements = None
		self.parent.elements = None