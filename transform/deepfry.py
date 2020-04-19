from . import abstractTransform
from helper import *
import cv2
import numpy as np
import os

tempfile = "temp.jpeg"

class deepFryTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Deep Fry"
	
	def description():
		#return a brief description of what the transform does
		return "Deep fries the image using Deep Fry Bot's algorithm."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		image = refreshImage(image)
		image = badPosterize(image)
		cv2.imwrite(tempfile, image, [int(cv2.IMWRITE_JPEG_QUALITY), 0])
		image = cv2.imread(tempfile)
		os.remove(tempfile)
		return image

	
	
def addColour(imageNormal):
	return cv2.applyColorMap(imageNormal, cv2.COLORMAP_AUTUMN)

def badPosterize(imageNormal):
	"""
	Posterize the image through a color list, diving it and making a pallete.
	Finally, applying to the image and returning the image with a the new pallete
	:param imageNormal: CV opened image | imageNormal | The normal image opened with OpenCV
	"""
	colorList = np.arange(0, 256)
	colorDivider = np.linspace(0, 255,3)[1]
	colorQuantization = np.int0(np.linspace(0, 255, 2))
	colorLevels = np.clip(np.int0(colorList/colorDivider), 0, 1)
	colorPalette = colorQuantization[colorLevels]
	return colorPalette[imageNormal]