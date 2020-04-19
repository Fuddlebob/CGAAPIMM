from . import abstractTransform
from helper import *
import random
import cv2
import numpy as np

class zoomTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Zoom in"
	
	def description():
		#return a brief description of what the transform does
		return "Zooms in on a random square of the image and resizes it to a 2048x2048 square."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		h, w = img_size(image)
		ma = min(h, w)
		size = max(64, int(random.uniform(0.05, 0.4) * ma))
		w2, h2 = randomPoint(w - size, h - size)
		zoom = image[h2:h2+size, w2:w2+size]
		return cv2.resize(zoom, (2048, 2048))