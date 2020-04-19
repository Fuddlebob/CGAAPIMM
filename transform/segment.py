from . import abstractTransform
import cv2
import numpy as np
import random
from PIL import Image, ImageDraw
import math
import os

class segmentTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Segment"
	
	def description():
		#return a brief description of what the transform does
		return "Segments the image into identically sized pieces."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		#save the image and use PIL instead because cv2 sucks for text stuff
		cv2.imwrite("temp.png", image)
		pim = Image.open("temp.png")
		tile_width = random.randint(16, 128)
		tile_height = random.randint(16, 128)
		x_spacing = random.randint(4, 64)
		y_spacing = random.randint(4, 64)
		width, height = pim.size
		set_width = math.ceil(width/tile_width)
		set_height = math.ceil(height/tile_height)
		new_width = width + (x_spacing * set_width)
		new_height = height + (y_spacing * set_height)
		new_set = Image.new("RGBA", (new_width, new_height), color="white")
		
		for x in range(set_width):
			for y in range(set_height):
				left = x * tile_width
				upper = y * tile_height
				box = (left, upper, left + tile_width, upper + tile_height)
				tile = pim.crop(box)
				new_left = (tile_width + x_spacing) * x
				new_upper = (tile_height + y_spacing) * y
				new_set.paste(tile, (new_left, new_upper))
		new_set.save("temp.png", "PNG")
		image = cv2.imread("temp.png")
		os.remove("temp.png")
		return image