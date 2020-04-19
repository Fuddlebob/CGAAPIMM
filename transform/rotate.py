from . import abstractTransform
import cv2
import numpy as np
import imutils
import random

class rotateTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Rotate"
	
	def description():
		#return a brief description of what the transform does
		return "Rotates the image by a random angle."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		return imutils.rotate(image, random.randint(30, 330))