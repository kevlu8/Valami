from util import *
import matplotlib.pyplot as plt
import cv2
import pytesseract
import math
from PIL import ImageFilter, Image

class Game:
	def __init__(self):
		pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kevlu8\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

	# check if player just died
	def died(self, scr):
		# 1. crop to the health hud
		w = scr.width
		h = scr.height
		crop = scr.crop((w * 0.30, h * 0.92, w * 0.34, h * 0.98))
		# 2. preserve only white -> i.e. r,g,b > 100, range(r,g,b) < 20
		data = crop.getdata()
		new_data = []
		for item in data:
			rgb = item[:-1]
			if max(rgb) - min(rgb) < 8 and min(rgb) > 100:
				new_data.append((255, 255, 255))
			else:
				new_data.append((0, 0, 0))
		crop.putdata(new_data)
		# 3. scale up
		crop = crop.resize((crop.width * 4, crop.height * 4), resample=Image.Resampling.BILINEAR)
		# 4. blur
		crop = crop.filter(ImageFilter.GaussianBlur(radius=3))

		plt.imshow(crop)
		plt.show()
		# 5. OCR
		text = pytesseract.image_to_string(crop)
		print(text)
		# 6. if we're alive, the text should contain a number 1-100
		if any(char.isdigit() for char in text) and 0 <= int(text) <= 100:
			return False
		return True

	# more generally, is true while the player is not alive
	def is_dead(self, scr):
		# 1. get the "spectating" section of the screen
		w = scr.width
		h = scr.height
		crop = scr.crop((w * 0.05, h * 0.78, w * 0.15, h * 0.82))
		# 2. run OCR and check if it says "SWITCH PLAYER"
		text = pytesseract.image_to_string(crop)
		return "switch player" in text.lower()

	# check if player just got a kill
	def kill(self, scr):
		# 1. get the kill icon area
		w = scr.width
		h = scr.height
		crop = scr.crop((w * 0.45, h * 0.72, w * 0.55, h * 0.87))
		# 2. check for circles (since the kill icon is a circle)
		ncircles = exists_circles(crop)
		return ncircles > 0