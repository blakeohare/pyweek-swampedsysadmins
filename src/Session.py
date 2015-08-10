import random

from src.Device import Device		

class Session:
	def __init__(self, level_id):
		self.counter = 0
		self.laptops_fixed = 0
		self.phones_fixed = 0
		self.tablets_fixed = 0
		self.end = 30 * 60 * 2 # 2 minutes
		self.devices = []
		self.active_devices = []
		self.level = level_id
		self.events = []
		ailments = ['sick']
		if self.level >= 2:
			ailments.append('sad')
		elif self.level >= 3:
			ailments.append('angry')
		elif self.level >= 4:
			ailments.append('crazy')
		elif self.level >= 5:
			ailments.append('unknown')
		elif self.level >= 7:
			ailments *= 3 # reduce the probability that it will be dead on arrival
			ailments.append('dead') 
			
		if self.level > 0:
			total = 5 + 5 * self.level
			types = ['laptop']
			if self.level > 2: types.append('tablet')
			if self.level > 4: types.append('phone')
			types *= (int(total / len(types)) + 2)
			types = types[:total]
			random.shuffle(types)
			for i in range(total):
				t = 1.0 * i / total + random.random() * 0.1 - .05
				if t > 1.0: t = 1.0
				if t < 0: t = 0.0
				t = t * .95 + .025
				t = int(self.end * t)
				random.shuffle(ailments)
				self.events.append(('device', t, types[i], ailments[0]))
		self.events.sort(key = lambda x:x[1])
	
	def get_events_for_frame(self):
		if len(self.events) > 0 and self.counter >= self.events[0][1]:
			event = self.events.pop(0)
			return event
		return None
	
	def is_done(self):
		return self.counter >= self.end and len(self.active_devices) == 0
		
	def update(self, playboard):
		
		event = self.get_events_for_frame()
		
		if event != None:
			type = event[0]
			if type == 'device':
				device_type = event[2]
				ailment = event[3]
				device = Device(playboard, self.counter, device_type, 200, 10, ailment)
				self.devices.append(device)
				self.active_devices.append(device)
		
		
		for device in self.active_devices:
			device.update()
		
		self.counter += 1
	