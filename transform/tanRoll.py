from . import abstractTransform
import cv2
import numpy as np
import random
import numpy as np
import matplotlib.pyplot as plt

class tanRollTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Tan Roll"
	
	def description():
		#return a brief description of what the transform does
		return "Rolls the image in a tan wave pattern. This one can get pretty screwy."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		h, w, c = image.shape
		amplitude = h/random.uniform(0.5, 5.0)
		period = random.uniform(0.25, 1.25)
		vert = random.randint(0, 1)
		if(vert):
			#vertical roll
			offset = random.randint(0, w)

			shift = lambda x: amplitude * np.tan(2.0*np.pi* x * (period / w))

			for i in range(w):
				s = int(shift(i + offset)) % h
				image[:,i] = np.roll(image[:,i], s, axis = 0)
		else:
			#horizontal roll
			offset = random.randint(0, h)

			shift = lambda x: amplitude * np.tan(2.0*np.pi* x * (period / h))

			for i in range(h):
				s = int(shift(i + offset)) % w
				image[i,:] = np.roll(image[i,:], s, axis = 0)
		return image