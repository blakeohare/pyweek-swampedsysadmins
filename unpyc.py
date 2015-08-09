import os

def unpycify(path):
	for file in os.listdir(path):
		fullpath = path + os.sep + file
		if os.path.isdir(fullpath):
			unpycify(fullpath)
		elif file.endswith('.pyc'):
			os.remove(fullpath)

unpycify('.')