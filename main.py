import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from OpenGL.GL.shaders import *
from math import *

import PIL.Image
import numpy
import time
import sys

from shaders import *
from textures import *
from controls import *
from model_helicopter import *
from model_ground import *

# Useful Parameters
program = None
datafile = None
platformTex = None
grassTex = None

# Window Dimensions
screenW = 960
screenH = 960

# Direction + Color of Light
lightColor = numpy.array([0.9,0.9,0.9,1], numpy.float32)
lightPosn = numpy.array([0.5, 0.5, -1, 0], numpy.float32)

# Background Color
skyR, skyG, skyB, skyA = 0.5, 0.7, 0.9, 0.0

# Camera Parameters
visField = 85
min_zoom = 0.5
zoom = 1.0 
max_zoom = 2.0
camera_degrees = 45

# Controls Parameters
speed = 2
pause = False

# Datafile Parameters

shiftZ = 0.0  # Remember, positive Z points down
helicopterTime = 0
x, y, z, qx, qy, qz, qw, t = 0, 0, 0, 0, 0, 0, 0, 0
time_adj, time_adj_flag = 0, False   # For files that have different starting times


  
def initGL(w, h):
	global grassTex, platformTex, program
	glClearColor(skyR, skyG, skyB, skyA)
	glClearDepth(1.0)
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)

	helicopterTime = time.time()
	update_timer = time.time()

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(visField, float(w)/float(h), 0.1, 700.0)
	glMatrixMode(GL_MODELVIEW)
	glEnable(GL_DEPTH_TEST)

	grassTex = loadTexture("images/grass.jpg")
	platformTex = loadTexture("images/helicopter_landing.jpg")

	if not glUseProgram:
		print 'Missing Shader Objects!'
		sys.exit(1)

	program = generateShaders()

def resize(w, h):
	global screenW, screenH
	if h < 400:  h = 400
	if w < 400:  w = 400
	screenW = w
	screenH = h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(visField, float(w)/float(h), 0.1, 700.0)
	glMatrixMode(GL_MODELVIEW)
 
def readData():
	global time_adj, time_adj_flag

	for i in range(0, speed-1):
		line = datafile.readline() # just read some lines to speed things up if necessary.
	line = datafile.readline()

	if len(line) == 0:
		datafile.close()
		print "Flight complete!"
		sys.exit(0)
	else:
		tokens = line.split()
		retList = map(lambda x: float(x), tokens[2:9])
		retList.append(float(tokens[1]))
		if not time_adj_flag:
			time_adj_flag = True
			time_adj = float(tokens[1])
		return retList
 
def glutPrint(x, y, font, text, r, g, b):
	glColor3f(r,g,b)
	glRasterPos2f(x,y)
	for ch in text:
		glutBitmapCharacter(font, ord(ch))

def convert_standard(camera_degrees):
	if camera_degrees < 0:
		return convert_standard(camera_degrees + 360)
	elif camera_degrees >= 360:
		return convert_standard(camera_degrees - 360)
	else:
		return camera_degrees

def display():
	global program, x, y, z, qx, qy, qz, qw, t, camera_degrees
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	camera_degrees = convert_standard(camera_degrees)

	if not pause:
		x, y, z, qx, qy, qz, qw, t = readData()

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0.0, screenW, 0.0, screenH)
	glutPrint(15, screenH - 40, GLUT_BITMAP_HELVETICA_18, "Time Elapsed: " + str(round(t - time_adj, 1)) + " s", 0, 0, 0)
	glutPrint(15, screenH - 80, GLUT_BITMAP_HELVETICA_18, "Position: ", 0, 0, 0)
	glutPrint(40, screenH - 110, GLUT_BITMAP_HELVETICA_18, "x: " + str(round(x,2)), 0, 0, 0)
	glutPrint(40, screenH - 140, GLUT_BITMAP_HELVETICA_18, "y: " + str(round(y,2)), 0, 0, 0)
	glutPrint(40, screenH - 170, GLUT_BITMAP_HELVETICA_18, "z: " + str(round(z,2)), 0, 0, 0)
	glutPrint(15, screenH - 210, GLUT_BITMAP_HELVETICA_18, "Quaternion: ", 0, 0, 0)
	glutPrint(40, screenH - 240, GLUT_BITMAP_HELVETICA_18, "x: " + str(round(qx,2)), 0, 0, 0)
	glutPrint(40, screenH - 270, GLUT_BITMAP_HELVETICA_18, "y: " + str(round(qy,2)), 0, 0, 0)
	glutPrint(40, screenH - 300, GLUT_BITMAP_HELVETICA_18, "z: " + str(round(qz,2)), 0, 0, 0)
	glutPrint(40, screenH - 330, GLUT_BITMAP_HELVETICA_18, "w: " + str(round(qw,2)), 0, 0, 0)
	glutPrint(screenW - 188, screenH - 40, GLUT_BITMAP_HELVETICA_18, "Camera Angle: " + str(round(camera_degrees, 0)), 0, 0, 0)
	glutPrint(screenW - 128, screenH - 80, GLUT_BITMAP_HELVETICA_18, "Speed: " + str(speed * 0.5), 0, 0, 0)
	glPopMatrix()

	glMatrixMode(GL_MODELVIEW)

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glLoadIdentity()

	gluLookAt(-5*zoom*cos(radians(camera_degrees)) + x, 5*zoom*sin(radians(camera_degrees)) + y, -2*zoom + z, x, y, z, 0, 0, -1)
	
	enablelighting = glGetUniformLocation(program, "enablelighting")
	glUniform1f(enablelighting, 1)
	numused = glGetUniformLocation(program, "numused")
	glUniform1i(numused, 1)
	lightposn = glGetUniformLocation(program, "lightposn")
	glUniform4fv(lightposn, 1, lightPosn)
	lightcol = glGetUniformLocation(program, "lightcolor")
	glUniform4fv(lightcol, 1, lightColor)

	isTex = glGetUniformLocation(program, "isTex")
	glUniform1i(isTex, 1)
	createGround(grassTex, shiftZ)
	createPlatform(platformTex, shiftZ)
	glUniform1i(isTex, 0)

	data = [x, y, z, qx, qy, qz, qw]
	createHelicopter(program, data)
	animateHelicopter(helicopterTime, pause)
	glutSwapBuffers()

#keyHash is a parameter in controls.py
def keyPressed(*args):
	global camera_degrees, zoom, speed, pause
	if args[0].lower() == keyHash['quit']:
		sys.exit()
	if args[0].lower() == keyHash['left']:
		camera_degrees -= 3
	if args[0].lower() == keyHash['right']:
		camera_degrees += 3
	if args[0].lower() == keyHash['zoomout']:
		zoom += 0.02
		if zoom > max_zoom: zoom = max_zoom
	if args[0].lower() == keyHash['zoomin']:
		zoom -= 0.02
		if zoom < min_zoom: zoom = min_zoom
	if args[0].lower() == keyHash['speed']:
		speed = (2*speed) % 31
	if args[0].lower() == keyHash['help']:
		printHelp()
	if args[0].lower() == keyHash['pause']:
		pause = not pause

def idleFunc():
	glutPostRedisplay()

def main():
	global datafile, zoom, max_zoom, min_zoom, shiftZ

	glutInit(sys.argv[0:1])

	if len(sys.argv) == 1:
		print "You must specify a file as input data for the visualizer. The command is: python helicopter_vis.py -f <filename>."
		exit(1)

	i = 1
	while i < len(sys.argv):
		if sys.argv[i] == "-f" :
			try:
				datafile = open(sys.argv[i+1])
			except IndexError:
				print "You must specify a file as input data for the visualizer. The command is: python helicopter_vis.py -f <filename> [-z <vertical_shift_amount>]."
				exit(1)
			except IOError:
				print "Unable to open file: " + sys.argv[i+1] + "."
				exit(1)
		elif sys.argv[i] == "-z" :
			try:
				shiftZ = float(sys.argv[i+1])
			except (ValueError, IndexError):
				print "You must specify a numerical floating point value for the shift amount (positiveZ = down)."
				exit(1)
		else:
			print "Illegal flag option; only -f <filename> and -z <vertical_shift_amount> allowed."
			exit(1)
		i += 2

	loadKeys()
	printHelp()

	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(screenW, screenH)
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("Helicopter Visualization")

	glutDisplayFunc(display)
	glutIdleFunc(idleFunc)
	glutReshapeFunc(resize)
	glutKeyboardFunc(keyPressed)
	initGL(screenW, screenH)
	glUseProgram(program)  
	glutMainLoop()

if __name__ == "__main__":
	main()