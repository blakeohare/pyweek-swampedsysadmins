class Reward:
	def __init__(self, model, session):
		self.model = model
		self.session = session
		self.avg_turnaround = None
		self.overtime = None
		self.next_budget = None
	
	def get_avg_turnaround(self):
		output = self.avg_turnaround
		if output == None:
			output = 0
			for device in self.session.devices:
				output += device.response_time
			output = 1.0 * output / len(self.session.devices)
		
			output = output / 30.0
			self.avg_turnaround = output
		return output
	
	def calculate_next_budget(self):
		output = self.next_budget
		if output == None:
			value = 1000
			
			turnaround = self.get_avg_turnaround()
			
			tbonus = 10 - turnaround
			
			value += tbonus * 100
			
			output = int(value)
			if output < 0: output = 0
			self.next_budget = output
		return output