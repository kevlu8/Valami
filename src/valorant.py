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
		crop = scr.crop((w * 0.30, h * 0.93, w * 0.34, h * 0.97))
		# 2. preserve only white -> i.e. r,g,b > 160, range(r,g,b) < 20
		data = crop.getdata()
		new_data = []
		for item in data:
			rgb = item[:-1]
			if max(rgb) - min(rgb) < 8 and min(rgb) > 160:
				new_data.append((255, 255, 255))
			else:
				new_data.append((0, 0, 0))
		crop.putdata(new_data)
		# 3. scale up
		crop = crop.resize((crop.width * 4, crop.height * 4), resample=Image.Resampling.BILINEAR)
		# 4. blur
		crop = crop.filter(ImageFilter.GaussianBlur(radius=3))
		# 5. OCR
		text = pytesseract.image_to_string(crop)
		# 6. if we're alive, the text should contain a number 1-100
		healthVerdict = any(char.isdigit() for char in text)
		# 7. crop to the ammo hud (in case the user is on left-handed mode; the health hud detection will be imprecise)
		crop = scr.crop((w * 0.66, h * 0.93, w * 0.72, h * 0.97))
		# 8. run the previous steps again
		data = crop.getdata()
		new_data = []
		for item in data:
			rgb = item[:-1]
			if max(rgb) - min(rgb) < 8 and min(rgb) > 160:
				new_data.append((255, 255, 255))
			else:
				new_data.append((0, 0, 0))
		crop.putdata(new_data)
		crop = crop.resize((crop.width * 4, crop.height * 4), resample=Image.Resampling.BILINEAR)
		crop = crop.filter(ImageFilter.GaussianBlur(radius=3))
		plt.imshow(crop)
		plt.show()
		# 9. OCR
		text = pytesseract.image_to_string(crop)
		print(text)
		# 10. if we're alive, the text should contain a number 1-100
		ammoVerdict = any(char.isdigit() for char in text)
		return not healthVerdict and not ammoVerdict # if both are false, we're (probably) dead

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