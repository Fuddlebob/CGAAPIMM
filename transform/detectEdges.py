from . import abstractTransform
from helper import *
import cv2
import numpy as np

class detectEdgesTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Detect Edges"
	
	def description():
		#return a brief description of what the transform does
		return "Create a black and white image, detailing the edges of the original."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		image = refreshImage(image)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (3, 3), 0)
		edged = cv2.Canny(gray, 20, 100)
		edged = cv2.merge([edged,edged,edged])
		return edged