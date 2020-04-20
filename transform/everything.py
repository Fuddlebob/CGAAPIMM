from . import abstractTransform
from helper import *
import random
import cv2
import numpy as np
import sys

class everythingTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Everything"
	
	def description():
		#return a brief description of what the transform does
		return "Performs every other transform on the image, in a random order. Warning: The resulting image will probably be completely unrecognisable."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		alltransforms = abstractTransform.abstractTransformClass.__subclasses__()
		random.shuffle(alltransforms)
		for t in alltransforms:
			if(not t.name() == "Everything"):
				image = t.transform(image)
				image = resizeImage(image, 1024)
		return image