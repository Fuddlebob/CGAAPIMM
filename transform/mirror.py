from . import abstractTransform
from helper import *
import cv2
import numpy as np
import random

class mirrorTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Mirror"
	
	def description():
		#return a brief description of what the transform does
		return "Mirrors the image vertically or horizontally."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		flip = random.randint(0, 1)
		mirror = random.randint(0, 1)
		flipimg =  cv2.flip(image, flip)
		h, w = img_size(image)

		if(flip):
			#horizontal flip
			m = int(w/2)
			if(mirror):
				#mirror left to right
				image[0:h, m:w] = flipimg[0:h, m:w] 
			else:
				#mirror right to left
				image[0:h, 0:m] = flipimg[0:h, 0:m] 
		else:
			#vertical flip
			m = int(h/2)
			if(mirror):
				#mirror top to bottom
				image[m:h, 0:w] = flipimg[m:h, 0:w] 
			else:
				#mirror bottom to top
				image[0:m, 0:w] = flipimg[0:m, 0:w] 

		return image