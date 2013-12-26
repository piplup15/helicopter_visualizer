import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import PIL.Image
import numpy


def loadTexture(name):

	im = PIL.Image.open(name)
	try:
		ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
	except SystemError:
		ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)

	pix = im.load()
	lst = []
	for i in range(im.size[0]):
		lst.append([])
		for j in range(im.size[1]):
			lst[i].append([])
			for k in range(3):
				lst[i][j].append(0)

	for i in range(im.size[0]):
		for j in range(im.size[1]):
			for k in range(3):
				lst[i][j][k] = pix[(i, im.size[1] - 1 - j)][k]

	image = numpy.array(lst, 'B')


	id = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, id)
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
	return id
