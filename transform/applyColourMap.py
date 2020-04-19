from . import abstractTransform
from helper import *
import cv2
import numpy as np
import random


class applyColourMapTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Apply Colour Map"
	
	def description():
		#return a brief description of what the transform does
		return "Colours the image according to a random colour map."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		image = refreshImage(image)
		return cv2.applyColorMap(image, random.randint(0, 11))