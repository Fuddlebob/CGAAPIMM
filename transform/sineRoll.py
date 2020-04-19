from . import abstractTransform
import cv2
import numpy as np
import random
import numpy as np
import matplotlib.pyplot as plt

class sineTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Sine Roll"
	
	def description():
		#return a brief description of what the transform does
		return "Rolls the image in a sin wave pattern."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		h, w, c = image.shape
		amplitude = h/random.uniform(0.5, 5.0)
		period = random.uniform(1.0, 5.0)
		offset = random.randint(0, w)
		shift = lambda x: amplitude * np.sin(2.0*np.pi* x * (period / w))

		for i in range(w):
			
			image[:,i] = np.roll(image[:,i], int(shift(i + w)), axis = 0)
		return image