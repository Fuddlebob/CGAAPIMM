from . import abstractTransform
from helper import *
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import requests

class putTextTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Put Text"
	
	def description():
		#return a brief description of what the transform does
		return "Writes some text somewhere on the image. Impact font, baby."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		text = randomText()
		#save the image and use PIL instead because cv2 sucks for text stuff
		cv2.imwrite("temp.png", image)
		pim = Image.open("temp.png").convert("RGBA")
		fontsize = random.randint(16, 400)
		font = ImageFont.truetype("transformFiles/impact.ttf", fontsize)
		width, height = pim.size
		x1 = random.randint(0, width)
		x2 = random.randint(0, width)
		if(x2 < x1):
			tmp = x1
			x1 = x2
			x2 = tmp
		y1 = random.randint(0, height)
		y2 = random.randint(0, height)
		if(y2 < y1):
			tmp = y1
			y1 = y2
			y2 = tmp
		pim = text_center(text, font, randomColour(), (x1, y1, x2, y2), pim)
		pim.save("temp.png")
		image = cv2.imread("temp.png")
		os.remove("temp.png")
		return image
		


#stole all this from Blue
def text_center(text, font, fill, bounds, image):
    x1, y1, x2, y2 = bounds
    W, H = (x2 - x1, y2 - y1)
    offset = (3, 3)

    shadow = Image.new("RGBA", image.size)
    canvas = ImageDraw.Draw(shadow)
    w, h = canvas.textsize(text, font=font)
    shadow_fill = (0, 0, 0, 255)
    for i in range(1, -1, -2):
        for j in range(1, -1, -2):
            pos = (x1 + (W - w) / 2 + i * offset[0], 
                y1 + (H - h) / 2 + j * offset[1])
            canvas.multiline_text(pos,
                                text,
                                font=font,
                                fill=shadow_fill,
                                spacing=10,
                                align="center")
    for i in range(5):
        shadow = shadow.filter(ImageFilter.BLUR)
    image = Image.alpha_composite(image, shadow)
    canvas = ImageDraw.Draw(image)
    w, h = canvas.textsize(text, font=font)
    pos = (x1 + (W - w) / 2, y1 + (H - h) / 2)
    canvas.multiline_text(pos,
                          text,
                          font=font,
                          fill=fill,
                          spacing=10,
                          align="center")
    return image
	
		
