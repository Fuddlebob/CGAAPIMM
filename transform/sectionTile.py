from . import abstractTransform
from helper import *
import cv2
import numpy as np
from PIL import Image
import math
import random
import os

class sectionTileTransform(abstractTransform.abstractTransformClass):
	def name():
		#short form name for the transform
		return "Section Tile"
	
	def description():
		#return a brief description of what the transform does
		return "Creates a new image, split into sections, tiled by various sections of the original image."
		
	def transform(image):
		#take in an openCV image and transform it, returning the new image
		h, w = img_size(image)
		size = random.randint(16, min(128, int(min(w, h)/4)))
		tileset_width = math.floor(w/size) - 1
		tileset_height = math.floor(h/size) - 1
		width = random.randint(30, 60)
		height = random.randint(30, 60)			
		tilearr = make_arr(width, height)
		divs = div_arr(tilearr)
		divs = random_merge(divs)
		
		for i, d in enumerate(divs):
			contents = random.randint(0, tileset_width * tileset_height)
			tilearr = fill_div(tilearr, d, contents)
		image = make_image(tilearr, size, image)
		return image
		
		

def get_tile(tilenum, size, image):
	h,w = img_size(image)
	tileset_width = math.floor(w/size) - 1
	tileset_height = math.floor(h/size) - 1
	row = int(tilenum / tileset_width)
	col = tilenum - (row * tileset_width)
	if(row >= tileset_width or col >= tileset_height):
		return get_tile(0, size, image)
	left = col * size
	upper = row * size
	new = image[upper:upper+size,left:left+size]

	return new
	
	
def div_arr(arr):
	width = len(arr)
	height = len(arr[0])
	div_lefts = []
	curr_left = 0
	while(curr_left < width):
		div_lefts.append(curr_left)
		w = random.randint(6, 10)
		curr_left = curr_left + w
		if(curr_left > width - 6):
			curr_left = width
	
	div_uppers = []
	curr_upper = 0
	while(curr_upper < height):
		div_uppers.append(curr_upper)
		h = random.randint(6, 10)
		curr_upper = curr_upper + h
		if(curr_upper > height - 6):
			curr_upper = height
	divs = []
	for j, u in enumerate(div_uppers):
		for i, l in enumerate(div_lefts):
			if(i == len(div_lefts) -1):
				w = width - l
			else:
				w = div_lefts[i + 1] - l
				
			if(j == len(div_uppers) - 1):
				h = height - u
			else:
				h = div_uppers[j + 1] - u
			div = Div(l, u, w, h)
			divs.append(div)
	return divs
	
'''
given the x and y of a tile, returns which div it is in
'''
def find_div(divs, x, y):
	for i, d in enumerate(divs):
		if(d.in_div(x, y)):
			return i
	return -1	
	
'''
given a div and a pair of coordinates, tells you if the 
'''
	
def random_merge(divs):
	i = 0
	mr_chance = .75
	md_chance = .75
	while(i < len(divs)):
		temp_mr = mr_chance
		temp_md = md_chance
		while(random.random() < temp_mr):
			divs = merge_right(divs, i)
			temp_mr = pow(temp_mr, 3)
		while(random.random() < temp_md):
			divs = merge_down(divs, i)
			temp_md = pow(temp_mr, 3)
		i = i + 1

	return divs
	
'''
Given a 2D array of divs, merges a given one with any directly to its right
does nothing if the set of divs directly to the right are not uniform in width
'''
def merge_right(divs, num):
	div = divs[num]
	upper = div.upper
	lower = div.upper + div.height
	x = div.left + div.width
	merge_list = []
	for y in range(upper, lower):
		if(find_div(merge_list, x, y) != -1):
			continue
		
		dn = find_div(divs, x, y)
		if(dn == -1):
			continue
		merge_list.append(divs[dn])
	if(divs[num].merge_divs(merge_list)):
		for b in merge_list:
			divs.remove(b)
	return divs

'''
Given a 2D array of divs, merges a given one with any directly below it
does nothing if the set of divs directly below it are not uniform in height
'''
def merge_down(divs, num):
	div = divs[num]
	left = div.x
	right = div.x + div.w
	y = div.y + div.h
	merge_list = []
	for x in range(left, right):
		if(find_div(merge_list, x, y) != -1):
			continue
		dn = find_div(divs, x, y)
		if(dn == -1):
			continue
		merge_list.append(divs[dn])
	if(divs[num].merge_divs(merge_list)):
		for b in merge_list:
			divs.remove(b)
	return divs	
	
	
	
class Div:
	def __init__(self, l=0, u=0, w=0, h=0):
		self.left = l
		self.upper = u
		self.x = l
		self.y = u
		self.width = w
		self.w = w
		self.height = h
		self.h = h
		
	def in_div(self, x, y):
		if((self.left <= x < self.left + self.width) and (self.upper <= y < self.upper + self.height)):
			return True
		return False
	
	def merge_divs(self, divs):	
		if not divs:
			return True	
		can_merge = True
		merge_dir = -1
		check = divs[0]
		if(check.left == self.left + self.width):
			merge_dir = 0
		elif(check.upper == self.upper + self.height):
			merge_dir = 1
		if(merge_dir == -1):
			return False
		if(merge_dir == 0):
			#merge right
			width = check.width
			heightsum = 0
			for d in divs:
				heightsum = heightsum + d.height
				if(width != d.width or d.left != self.left + self.width):
					can_merge = False
			if(heightsum != self.height):
				can_merge = False
			if(can_merge):
				self.width = self.width + width
		if(merge_dir == 1):
			#merge down
			height = check.height
			widthsum = 0
			for d in divs:
				widthsum = widthsum + d.width
				if(height != d.height or d.upper != self.upper + self.height):
					can_merge = False
			if(widthsum != self.width):
				can_merge = False
			if(can_merge):
				self.height = self.height + height
		
		self.x = self.left
		self.y = self.upper		
		self.h = self.height
		self.w = self.width
		
		return can_merge
		
def fill_div(arr, box, num):
	left = box.x
	upper = box.y
	width = box.w
	height = box.h
	for i in range(width):
		for j in range(height):
			arr[left + i][upper + j] = num
	return arr

def make_image(tilearr, size, image):
	width = len(tilearr)
	height = len(tilearr[0])
	newImage = np.zeros((height*size,width*size,3), np.uint8)
	for i in range(width):
		for j in range(height):
			y = size * j
			x = size * i
			tile = get_tile(tilearr[i][j], size, image)
			newImage[y:y+size, x:x+size] = tile
	
	return newImage

def make_arr(width, height):
	arr = []
	for i in range(width):
		arr.append([])
		for j in range(height):
			arr[i].append(0)
	return arr