keyHash = {}

def loadKeys():
	keyHash['help'] = 'h'
	keyHash['speed'] = 't'
	keyHash['pause'] = 'p'
	keyHash['left'] = 'a'
	keyHash['right'] = 'd'
	keyHash['zoomout'] = 'z'
	keyHash['zoomin'] = 'x'
	keyHash['quit'] = 'q'


def printHelp():
	print "Key Guide:"
	print "Press '" + keyHash['help'] + "' to print this help message again."
	print "Press '" + keyHash['speed'] + "' to toggle between 0.5x, 1x, 2x, 4x, and 8x speeds."
	print "Press '" + keyHash['pause'] + "' to pause / resume."
	print "Press '" + keyHash['left'] + "' to stride the camera left."
	print "Press '" + keyHash['right'] + "' to stride the camera right."
	print "Press '" + keyHash['zoomout'] + "' to zoom out."
	print "Press '" + keyHash['zoomin'] + "' to zoom in."
	print "Press '" + keyHash['quit'] + "' to quit."
	print ""