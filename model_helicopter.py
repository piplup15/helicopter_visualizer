import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
from OpenGL.GL.shaders import *
from math import *
import numpy

def createHelicopter(program, data, wingsAngle):

	x,y,z,qx,qy,qz,qw = data

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