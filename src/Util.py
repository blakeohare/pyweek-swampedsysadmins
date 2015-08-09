def make_grid(width, height):
	output = []
	
	while width > 0:
		width -= 1
		output.append([None] * height)
	return output

def coerce_range(value, lower, upper):
	if value < lower: return lower
	if value > upper: return upper
	return value


def range255(value):
	if value < 0: return 0
	if value > 255: return 255
	return int(value)
