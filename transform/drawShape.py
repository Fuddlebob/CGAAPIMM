from . import abstractTransform
from helper import *
import cv2
import numpy as np
import random
import math

class drawShapeTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Draw Shape"
	
	def description():
		#return a brief description of what the transform does
		return "Draws a circle, rectangle, or triangle somewhere on the image."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		shape_type = random.choice([0,1,2])
		colour = randomColour()
		h, w, c = image.shape
		if(shape_type == 0):
			#draw circle
			center = randomPoint(w, h)
			radius = random.randint(16, int(max(h/2, w/2)))
			cv2.circle(image, center, radius, colour, thickness=-1)
		
		elif(shape_type == 1):
			#draw rectangle
			pt1 = randomPoint(w, h)
			pt2 = randomPoint(w, h)
			cv2.rectangle(image, pt1, pt2, colour, thickness = -1)
			
		else:
			#draw triangle
			pts = np.array([randomPoint(w, h), randomPoint(w, h), randomPoint(w, h)])
			cv2.fillConvexPoly(image, pts, colour)
		
		return image
		
	
