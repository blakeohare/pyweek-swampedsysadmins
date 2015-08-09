class DragDescriptor:
	def __init__(self, member, x, y):
		self.member = member
		self.points = [(x, y)] # points the user dragged out
		self.distance = [0] # distance from the previous point
		self.current_distance = 0.0
		self.total_distance = 0.0
		self.traversed_distance = 0.0 # how much has the player traversed since the user started drawing
	
	def add_point(self, x, y, playboard):
		# TODO; trace the line segment to see if there is any overlap with unpassable blocks
		
		prev_x, prev_y = self.points[-1]
		self.points.append((x, y))
		
		dx = prev_x - x
		dy = prev_y - y
		dist = (dx ** 2 + dy ** 2) ** .5
		self.distance.append(dist)
		self.total_distance += dist
	
	def get_marker_list(self, rc):
		
		interval = 8
		
		if self.total_distance < interval:
			if self.total_distance == 0:
				#print 'A', [self.points[0]]
				return [self.points[0]]
			output = [self.points[0], self.points[-1]]
			#print 'B', output
			return output
		
		
		output = []
		offset = self.traversed_distance + rc * 1.0 # scale this to make it move faster or slower
		dist = (offset % interval)
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
		#print output
		return output

			
		
		
		
		