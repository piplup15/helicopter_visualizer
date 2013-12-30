import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
from OpenGL.GL.shaders import *
from math import *
import time
import numpy

fieldLen = 100.0
platform = 0.5
groundLevel = 0.2 

def createGround(grassTex, shiftZ):
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) 
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glBindTexture(GL_TEXTURE_2D, grassTex)

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, fieldLen)
	glVertex3f(-fieldLen, -fieldLen, shiftZ + groundLevel)
	glTexCoord2f(fieldLen, fieldLen)
	glVertex3f(-fieldLen, fieldLen, shiftZ + groundLevel)
	glTexCoord2f(fieldLen, 0.0)
	glVertex3f(fieldLen, fieldLen, shiftZ + groundLevel)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(fieldLen, -fieldLen, shiftZ + groundLevel)
	glEnd()

	glDisable(GL_TEXTURE_2D)

def createPlatform(platformTex, shiftZ):
	glPushMatrix()
	glRotatef(-90, 0, 0, 1)
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glBindTexture(GL_TEXTURE_2D, platformTex)

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-platform, -platform, shiftZ + groundLevel - 0.01)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(-platform, platform, shiftZ + groundLevel - 0.01)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(platform, platform, shiftZ + groundLevel - 0.01)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(platform, -platform, shiftZ + groundLevel - 0.01)
	glEnd()

	glDisable(GL_TEXTURE_2D)
	glPopMatrix()

