from . import abstractTransform
from helper import *
import cv2
import numpy as np
import random

class superimposeTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Superimpose"
	
	def description():
		#return a brief description of what the transform does
		return "Superimposes a random image on top of this one."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		image = refreshImage(image)
		h, w, c = image.shape
		newImage = randomImage()
		newImage = cv2.resize(newImage, (w, h))
		image = cv2.addWeighted(image,1,newImage,random.uniform(0.2, 0.75),0)
		return image