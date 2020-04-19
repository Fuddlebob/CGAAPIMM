from . import abstractTransform
import cv2
import numpy as np
import random

class diagonalRollTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Diagonal Roll"
	
	def description():
		#return a brief description of what the transform does
		return "Rolls the image along a diagonal."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		h, w, c = image.shape
		mul = random.choice([-1, 1])
		for i in range(w):
			image[:,i] = np.roll(image[:,i], int(i * h/w) * mul, axis = 0)
		return image