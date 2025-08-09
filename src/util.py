import numpy as np
from PIL import ImageGrab
import pyttsx3
import cv2
import matplotlib.pyplot as plt
import requests

def capt_scr():
	scr = ImageGrab.grab()
	return scr

def screen_sat(scr):
	# scr = image of the entire screen, type = PIL.Image.Image
	# 1. crop to middle only - center 80% of image
	w = scr.width
	h = scr.height
	crop = scr.crop((w * 0.1, h * 0.1, w * 0.9, h * 0.9))
	# 2. get average grayscale color of that crop
	avg = np.array(crop.convert("L")).mean() / 255.0
	return avg

def exists_circles(scr):
	# 1. convert to numpy array and grayscale
	img = cv2.cvtColor(np.array(scr), cv2.COLOR_RGB2BGR)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# 2. blur
	gray = cv2.medianBlur(gray, 5)
	# 3. detect circles
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
		param1=80, param2=55, minRadius=30, maxRadius=100)
	if circles is None:
		return 0
	# draw out circles
	# circles = np.uint16(np.around(circles))
	# for i in circles[0, :]:
	# 	# draw the outer circle
	# 	cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
	# 	# draw the center of the circle
	# 	cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
	# plt.imshow(img)
	# plt.show()
	# print(circles.shape[1])
	return circles.shape[1]

def get_completion(msg):
	headers = {
		"Content-Type": "application/json"
	}
	data = {
		"messages": [
			{
				"role": "system",
				"content": "You are a snarky Valorant coach whose job is to provide sarcastic commentary on a player's performance. Do not use special characters in your responses. The commentary you provide will be given to the player in real-time, so keep it short."
			},
			{
				"role": "user",
				"content": msg
			}
		],
		"model": " meta-llama/llama-4-maverick-17b-128e-instruct",
		"include_reasoning": False,
	}
	response = requests.post("https://ai.hackclub.com/chat/completions", headers=headers, json=data)
	if response.status_code == 200:
		return response.json()["choices"][0]["message"]["content"]
	return "Error"

class TTSClass:
	engine = None
	def __init__(self):
		self.engine = pyttsx3.init()
	def start(self, msg):
		self.engine.say(msg)
		self.engine.runAndWait()