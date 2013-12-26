import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
from OpenGL.GL.shaders import *
from math import *
import time, sys
program = None

import PIL.Image
import numpy
import time
import sys


from shaders import *
from textures import *



####################### PARAMS ############################
visField = 85                                               # visField =
screenW, screenH = 960, 960
lightColor = numpy.array([0.9,0.9,0.9,1], numpy.float32)
lightPosn = numpy.array([0.5, 0.5, -1, 0], numpy.float32)
skyR, skyG, skyB, skyA = 0.5, 0.7, 0.9, 0.0   # RGBA Color of the sky
field = 100.0                                  # (-10, -10) to (10, 10) square
platform =0.5                                 # (-0.5, -0.5) to (0.5, 0.5)
ground_level = 0.2                            # z is down
zoom = 0.0
max_zoom, min_zoom = 0.0, 0.0
shiftZ = 0.0                                  # this is because the helicopter starts at (0,0,0) somewhere in the sky ... different for different files too
grass_width = 2.0

camera_degrees = 45
helicopterTime = 0
wingsAngle = 0
file = None
camera_mode = "stationary"
x, y, z, qx, qy, qz, qw, t = 0, 0, 0, 0, 0, 0, 0, 0
time_adj, time_adj_flag = 0, False
speed = 2
pause = False
stationary_camera_autolock = True

SCALE_CONSTANT = 1
##############################################################

####################### TEXTURES #############################
grassTex = None
platformTex = None
##############################################################
  
def initGL(w, h):
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


    # load all textures:
    global grassTex
    grassTex = loadTexture("images/grass.jpg")
    global platformTex
    platformTex = loadTexture("images/helicopter_landing.jpg")
 
    if not glUseProgram:
        print 'Missing Shader Objects!'
        sys.exit(1)
 
    global program
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
		line = file.readline() # just read some lines to speed things up if necessary.
	line = file.readline()

	if len(line) == 0:
		file.close()
		print "Flight complete!"
		exit(0)
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

	global program, x, y, z, qx, qy, qz, qw, t, camera_degrees, stationary_camera_autolock

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Printing vital text to the screen...

	camera_degrees = convert_standard(camera_degrees)

	if not pause:
		x, y, z, qx, qy, qz, qw, t = readData()

		x *= SCALE_CONSTANT
		y *= SCALE_CONSTANT
		z *= SCALE_CONSTANT

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
	glLoadIdentity()

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glLoadIdentity()

	########################### Camera ###########################
	if camera_mode == "follow":
		gluLookAt(-5*zoom*cos(radians(camera_degrees)) + x, 5*zoom*sin(radians(camera_degrees)) + y, -2*zoom + z, x, y, z, 0, 0, -1)
	elif camera_mode == "stationary":
		if stationary_camera_autolock:
			magnitude = sqrt(x**2 + y**2)
			cos_meas = x * 1.0 / magnitude if magnitude != 0 else 1.0
			sin_meas = y * 1.0 / magnitude if magnitude != 0 else 0.0
			camera_degrees = degrees(acos(cos_meas)) if sin_meas > 0.0 else -degrees(acos(cos_meas))
			if magnitude != 0:
				gluLookAt(0, 0, SCALE_CONSTANT*shiftZ, x * 1.0 / magnitude , y * 1.0 / magnitude, SCALE_CONSTANT*shiftZ-.8, 0, 0, -1)
			else:
				gluLookAt(0, 0, SCALE_CONSTANT*shiftZ, 0, 0, -1, 0, 0, -1)
			stationary_camera_autolock = False
		else:
			gluLookAt(0, 0, SCALE_CONSTANT*shiftZ, cos(radians(camera_degrees)), sin(radians(camera_degrees)), SCALE_CONSTANT*shiftZ-.8, 0, 0, -1)

	########################### Lights ###########################
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


	########################### Ground ##########################

	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) ; 
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) ; 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) ;
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) ;
	glBindTexture(GL_TEXTURE_2D, grassTex)

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, field); glVertex3f(-field, -field, SCALE_CONSTANT*shiftZ + ground_level);
	glTexCoord2f(field, field); glVertex3f(-field, field, SCALE_CONSTANT*shiftZ + ground_level);
	glTexCoord2f(field, 0.0); glVertex3f(field, field, SCALE_CONSTANT*shiftZ + ground_level);
	glTexCoord2f(0.0, 0.0); glVertex3f(field, -field, SCALE_CONSTANT*shiftZ + ground_level);
	glEnd();

	glDisable(GL_TEXTURE_2D)

	########################## Platform #########################
	glPushMatrix()
	glRotatef(-90, 0, 0, 1)
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) ; 
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) ; 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) ;
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) ;
	glBindTexture(GL_TEXTURE_2D, platformTex)

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, 1.0); glVertex3f(-platform, -platform, SCALE_CONSTANT*shiftZ + ground_level - 0.01);
	glTexCoord2f(1.0, 1.0); glVertex3f(-platform, platform, SCALE_CONSTANT*shiftZ + ground_level - 0.01);
	glTexCoord2f(1.0, 0.0); glVertex3f(platform, platform, SCALE_CONSTANT*shiftZ + ground_level - 0.01);
	glTexCoord2f(0.0, 0.0); glVertex3f(platform, -platform, SCALE_CONSTANT*shiftZ + ground_level - 0.01);
	glEnd();

	glDisable(GL_TEXTURE_2D)
	glPopMatrix()

	glUniform1i(isTex, 0)

	######################### Simple Helicopter #################

	ambient = glGetUniformLocation(program, "ambient")
	diffuse = glGetUniformLocation(program, "diffuse")
	specular = glGetUniformLocation(program, "specular")
	emission = glGetUniformLocation(program, "emission")
	shininess = glGetUniformLocation(program, "shininess")

	glPushMatrix()

	# Flying the helicopter
	glTranslatef(x, y, z)

	angle = acos(qw) * 2.0
	axisX = qx / sin (0.5 * angle)
	axisY = qy / sin (0.5 * angle)
	axisZ = qz / sin (0.5 * angle)


	glRotatef(degrees(angle), axisX, axisY, axisZ)


	# Helicopter head
	glPushMatrix()
	glUniform4fv(ambient, 1, numpy.array([0.3, 0.3, 0.4, 1.0], numpy.float32))
	glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 1.0], numpy.float32))
	glUniform4fv(diffuse, 1, numpy.array([0.2, 0.2, 0.5, 1.0], numpy.float32))
	glUniform4fv(specular, 1, numpy.array([0.5, 0.5, 0.5, 1.0], numpy.float32))
	glUniform1f(shininess, 2.0)
	glutSolidSphere(0.15, 30, 30)
	glPopMatrix()
	
	# Back wings
	glPushMatrix()
	glTranslatef(-0.38, .025, 0)
	glRotate(wingsAngle, 0, 1, 0)
	glRotate(45, 0, 1, 0)
	glScalef(.25, .02, .05)
	glutSolidCube(1)
	glPopMatrix()

	glPushMatrix()
	glTranslatef(-0.38, -.025, 0)
	glRotate(wingsAngle, 0, 1, 0)
	glRotate(-45, 0, 1, 0)
	glScalef(.25, .02, .05)
	glutSolidCube(1)
	glPopMatrix()

	# Top wings
	glPushMatrix()
	glTranslatef(0, 0, -0.21)
	glRotate(wingsAngle, 0, 0, -1)
	glRotate(45, 0, 0, -1)
	glScalef(.7, .06, .02)
	glutSolidCube(1)
	glPopMatrix()

	glPushMatrix()
	glTranslatef(0, 0, -0.21)
	glRotate(wingsAngle, 0, 0, -1)
	glRotate(-45, 0, 0, -1)
	glScalef(.7, .06, .02)
	glutSolidCube(1)
	glPopMatrix()

	# Helicopter Legs
	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(0,-0.11,0.16)
	glRotatef(90,0,1,0)
	glTranslatef(0,0,-0.2)
	gluCylinder(quadric, 0.03, 0.03, 0.4, 30, 30)
	quadric = gluNewQuadric()
	gluDisk(quadric, 0, 0.03, 30, 30)
	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(0, 0, 0.4)
	gluDisk(quadric, 0, 0.03, 30, 30)
	glPopMatrix()
	glPopMatrix()

	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(0,0.11,0.16)
	glRotatef(90,0,1,0)
	glTranslatef(0,0,-0.2)
	gluCylinder(quadric, 0.03, 0.03, 0.4, 30, 30)
	quadric = gluNewQuadric()
	gluDisk(quadric, 0, 0.03, 30, 30)
	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(0, 0, 0.4)
	gluDisk(quadric, 0, 0.03, 30, 30)
	glPopMatrix()
	glPopMatrix()


	# Helicopter backbone
	glPushMatrix()
	glUniform4fv(ambient, 1, numpy.array([0.0, 0.0, 0.0, 1.0], numpy.float32))
	glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 1.0], numpy.float32))
	glUniform4fv(diffuse, 1, numpy.array([0.4, 0.4, 0.4, 1.0], numpy.float32))
	glUniform4fv(specular, 1, numpy.array([0.5, 0.5, 0.5, 1.0], numpy.float32))
	glUniform1f(shininess, 2.0)
	glTranslatef(-0.25, 0, 0)
	glScalef(.3, .03, .07)
	glutSolidCube(1)
	glPopMatrix()

	# Helicopter Topbone
	glPushMatrix()
	glTranslatef(0, 0, -0.2)
	quadric = gluNewQuadric()
	gluCylinder(quadric, 0.04, 0.04, 0.115, 30, 30)
	glPopMatrix()

	#Helicopter Legbones
	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(-0.06,-0.05,0.05)
	glRotatef(-30,-1,0,0)
	gluCylinder(quadric, 0.02, 0.02, 0.13, 30, 30)
	glPopMatrix()

	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(0.06,-0.05,0.05)
	glRotatef(-30,-1,0,0)
	gluCylinder(quadric, 0.02, 0.02, 0.13, 30, 30)
	glPopMatrix()

	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(-0.06,0.05,0.05)
	glRotatef(30,-1,0,0)
	gluCylinder(quadric, 0.02, 0.02, 0.13, 30, 30)
	glPopMatrix()

	glPushMatrix()
	quadric = gluNewQuadric()
	glTranslatef(0.06,0.05,0.05)
	glRotatef(30,-1,0,0)
	gluCylinder(quadric, 0.02, 0.02, 0.13, 30, 30)
	glPopMatrix()

	glPopMatrix()

	animateHelicopter()
	glutSwapBuffers()


def animateHelicopter():
	global wingsAngle, helicopterTime
	if (time.time() - helicopterTime) >= 0.02:         #10 ms == 100 fps
		if not pause:
			wingsAngle += 45
		helicopterTime = time.time()


def keyPressed(*args):
	global camera_degrees, zoom, speed, pause, stationary_camera_autolock
	if ord(args[0]) == 27: # Escape character
		sys.exit()
	if args[0].lower() == 'a':
		camera_degrees -= 3
	if args[0].lower() == 'd':
		camera_degrees += 3
	if args[0].lower() == 'z':
		zoom += 0.02
		if zoom > max_zoom: zoom = max_zoom
	if args[0].lower() == 'x':
		zoom -= 0.02
		if zoom < min_zoom: zoom = min_zoom
	if args[0].lower() == 't':
		speed = (2*speed) % 31
	if args[0].lower() == 'h':
		printHelp()
	if args[0].lower() == 'p':
		pause = not pause
	if args[0].lower() == 'g' and camera_mode == "stationary":
		stationary_camera_autolock = True



def printHelp():
	print "Key Guide:"
	print "Press 'h' to print this help message again."
	print "Press 't' to toggle between 0.5x, 1x, 2x, 4x, and 8x speeds."
	print "Press 'p' to pause / resume."
	print "Press 'a' to stride the camera left."
	print "Press 'd' to stride the camera right."

	if camera_mode == "follow":
		print "Press 'z' to zoom out."
		print "Press 'x' to zoom in."
	else:
		print "Press 'g' to autolock onto the helicopter."

	print "Press 'ESC' to quit."
	print ""

def idleFunc():
	glutPostRedisplay()

def main():

	global file, camera_mode, zoom, max_zoom, min_zoom, shiftZ

	glutInit(sys.argv[0:1]) # dunno what this does...

	if len(sys.argv) == 1:
		print "You must specify a file as input data for the visualizer. The command is: python helicopter_vis.py -f <filename> [-c <camera_mode>]."
		exit(1)

	i = 1
	while i < len(sys.argv):
		if sys.argv[i] == "-f" :
			try:
				file = open(sys.argv[i+1])
			except IndexError:
				print "You must specify a file as input data for the visualizer. The command is: python helicopter_vis.py -f <filename> [-c <camera_mode>] [-z <vertical_shift_amount>]."
				exit(1)
			except IOError:
				print "Unable to open file: " + sys.argv[i+1] + "."
				exit(1)

		elif sys.argv[i] == "-c" :
			try:
				if sys.argv[i+1] not in ["stationary", "follow"]:
					print "Illegal camera option: must choose either 'stationary' or 'follow'."
					exit(1)
				else:
					camera_mode = sys.argv[i+1]
					zoom, max_zoom, min_zoom = 0.5, 2.0, 0.5
			except IndexError:
				print "You must specify a camera option: either 'stationary' or 'follow'."
				exit(1)

		elif sys.argv[i] == "-z" :
			try:
				shiftZ = float(sys.argv[i+1])
			except (ValueError, IndexError):
				print "You must specify a numerical floating point value for the shift amount (positiveZ = down)."
				exit(1)

		else:
			print "Illegal flag option; only -f <filename>, -c <camera_mode>, and -z <vertical_shift_amount> allowed."
			exit(1)
		i += 2


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