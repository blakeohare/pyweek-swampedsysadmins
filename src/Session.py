import random

from src.Device import Device		

class Session:
	def __init__(self, level_id, model = None):
		self.counter = 0
		self.laptops_fixed = 0
		self.phones_fixed = 0
		self.tablets_fixed = 0
		
		IS_DEBUG = False
		
		self.end = 30 * 60 * 1 # 1 minute
		self.device_count_override = None
		self.required_events = []
		
		#self.end = 10 * 30 # 10 seconds
		#self.device_count_override = 3
		
		self.employee_anger = None
		#self.level = 10
		totoro_count = 0
		if model != None:
			for furn in model.furniture:
				if furn[0] == '2':
					totoro_count += 1
		
		totoro_factor = .91 ** totoro_count
		#print 'ttr', totoro_factor
		#level_id = 100
		
		self.devices = []
		self.active_devices = []
		self.level = level_id
		self.events = []
		ailments = ['sick']
		if self.level >= 2:
			ailments.append('sad')
		if self.level >= 3:
			ailments.append('angry')
		if self.level >= 4:
			ailments.append('crazy')
		if self.level >= 5:
			ailments.append('unknown')
		if self.level >= 7:
			ailments *= 3 # reduce the probability that it will be dead on arrival
			ailments.append('dead') 
		
		#print ailments
		self.total_devices = 0
		if self.level > 0:
			total = 5 + 2 * self.level
			
			#total = 100
			
			#if self.device_count_override != None:
			#	total = self.device_count_override
			
			
			#if IS_DEBUG:
			#	total = 1
				
			self.total_devices = total
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
				ail = ailments[0]
				if random.random() > totoro_factor:
					ail = 'sick'
					#print 'totoro replaced'
				self.events.append(('device', t, types[i], ail))
		
		for event in self.required_events:
			devices = 'phone tablet laptop'.split(' ')
			random.shuffle(devices)
			self.events = [('device', 0, devices[0], event)] + self.events
		
		self.events.sort(key = lambda x:x[1])
		self.staff_randomized = False
	
	def induce_device_storm(self):
		self.counter = 5
		self.events = []
		for i in range(12):
			self.events.append(('device', 6 + i, 'phone', random.choice(['sick', 'angry', 'unknown', 'crazy', 'sad'])))
		self.employee_anger = None
	
	def induce_device(self, type, ailment):
		self.counter = 5
		self.events = [('device', 20, type, ailment)]
		self.employee_anger = None
	
	def get_events_for_frame(self):
		if len(self.events) > 0 and self.counter >= self.events[0][1]:
			event = self.events.pop(0)
			return event
		return None
	
	def is_done(self):
		return self.counter >= self.end and len(self.active_devices) == 0
		
	def is_iv_available(self):
		return True
	
	def is_cucumber_available(self):
		return True
	
	def is_tape_available(self):
		return True
	
	def is_jacket_available(self):
		return True
		
	def update(self, playboard):
		
		if not self.staff_randomized:
			for staff in playboard.model.staff:
				x, y = playboard.get_random_open_tile()
				staff.x = x * 32 + 16
				staff.y = y * 32 + 16
			self.staff_randomized = True
		
		event = self.get_events_for_frame()
		
		if event != None:
			type = event[0]
			if type == 'device':
				device_type = event[2]
				ailment = event[3]
				device = Device(playboard, self.counter, device_type, 200, 10, ailment)
				self.devices.append(device)
				self.active_devices.append(device)
		
		
		new_active_devices = []
		for device in self.active_devices:
			device.update()
			if device.state == 'new':
				playboard.animations.append({
					'type': 'device',
					'ttl': 10,
					'mx': device.x,
					'my': device.y,
					'x': device.x,
					'y': device.y,
					'device': device.device_type,
					'overlay': 'check',
					'vx': 0,
					'vy': -3
				})
			elif device.state == 'dead' and device.replaced:
				playboard.animations.append({
					'type': 'device',
					'ttl': 10,
					'mx': device.x,
					'my': device.y,
					'x': device.x,
					'y': device.y,
					'device': device.device_type,
					'overlay': 'dead',
					'vx': 0,
					'vy': -3
				})
				
			else:
				new_active_devices.append(device)
		self.active_devices = new_active_devices
		
		self.counter += 1
	
	def get_current_angry_employee(self):
		if self.employee_anger == None:
			if self.events == None or len(self.events) == 0:
				return None
			employees = []
			events = []
			for event in self.events:
				if event[0] == 'device':
					events.append((random.choice(list('123')), event[1]))
			for i in range(11):
				for event in events:
					emp, t = event
					t1 = t - i
					t2 = t + i
					while len(employees) < t2 + 5:
						employees.append(None)
					
					if employees[t1] == None:
						employees[t1] = emp
					if employees[t2] == None:
						employees[t2] = emp
			self.employee_anger = employees
		
		if self.counter < len(self.employee_anger):
			return self.employee_anger[self.counter]
		return None