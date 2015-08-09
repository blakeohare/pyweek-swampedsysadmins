class DragDescriptor:
	def __init__(self, member):
		self.member = member
		self.points = [(member.x, member.y)] # points the user dragged out
		self.distance = [0] # distance from the previous point
		self.current_distance = 0.0
		self.total_distance = 0.0
		self.traversed_distance = 0.0 # how much has the player traversed since the user started drawing
		self.is_active = False
		self.done = False
	
	def add_point(self, x, y, playboard):
		# TODO; trace the line segment to see if there is any overlap with unpassable blocks
		
		prev_x, prev_y = self.points[-1]
		self.points.append((x, y))
		
		dx = prev_x - x
		dy = prev_y - y
		dist = (dx ** 2 + dy ** 2) ** .5
		self.distance.append(dist)
		self.total_distance += dist
	
	def do_update(self, chop_off_amount, first_recurse=True):
		player = self.member
		
		if len(self.points) == 1:
			player.x, player.y = self.points[0]
			if not self.is_active:
				self.done = True
			self.total_distance = 0
			return 
		
		x, y = self.points[1]
		dx = x - player.x
		dy = y - player.y
		dist = (dx ** 2 + dy ** 2) ** .5
		
		if dist == chop_off_amount:
			self.points = self.points[1:]
			self.total_distance -= dist
			if len(self.points) == 1:
				if not self.is_active:
					self.done = True
			player.x, player.y = x, y
			self.traversed_distance += dist
			return 
		elif dist < chop_off_amount:
			self.points = self.points[1:]
			self.total_distance -= dist
			player.x, player.y = x, y
			self.traversed_distance += dist
			return self.do_update(chop_off_amount - dist)
		else: # point is further than the velocity. update the first point
			self.points[0] = (self.points[0][0] + dx * chop_off_amount / dist, 
							  self.points[0][1] + dy * chop_off_amount / dist)
			player.x, player.y = self.points[0]
			self.total_distance -= chop_off_amount
			self.traversed_distance += chop_off_amount
			return
		
	
	def get_marker_list(self, rc):
		
		interval = 8
		
		if self.total_distance < interval:
			if self.total_distance == 0:
				return [self.points[0]]
			output = [self.points[0], self.points[-1]]
			return output
		
		
		output = []
		offset = -self.traversed_distance + rc * 1.0 # scale this to make it move faster or slower
		dist = ((offset % interval) + interval) % interval
		index = 0
		points = self.points
		distance_covered = interval - dist
		prev_x, prev_y = points[0]
		index = 1
		while index < len(points):
			dx = points[index][0] - prev_x
			dy = points[index][1] - prev_y
			dist = (dx ** 2 + dy ** 2) ** .5
			# this point is before the next interval, step forward
			if distance_covered + dist < interval:
				distance_covered += dist
				prev_x, prev_y = points[index]
				index += 1
			elif distance_covered + dist == interval: # the next point is the next step
				output.append(points[index])
				distance_covered = 0.0
				prev_x, prev_y = points[index]
				index += 1
			else: # the next point is beyond the next step. Add a point to the output and update prev_x, prev_y to it, and set distance covered to 0
				remaining = interval - distance_covered
				if dx == 0: # avoid negative slopes
					px = prev_x
					py = prev_y
					if dy > 0:
						py += remaining
					else:
						py -= remaining
					
					output.append((px, py))
					prev_y = py
				else:
					m = 1.0 * dy / dx # slope
					px = prev_x + dx * remaining / dist
					py = prev_y + dy * remaining / dist
					output.append((px, py))
					prev_x, prev_y = px, py
				distance_covered = 0.0

		return output

			
		
		
		
		