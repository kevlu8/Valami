from collections import deque
from PIL import Image
import matplotlib.pyplot as plt
from valorant import *
import random
import time
from util import get_completion, TTSClass, capt_scr
import sys
import os

game = Game()
last_msg = 0

death_prompt = "You are watching a player play Valorant. The player has just died. Give 5 snarky and sarcastic remarks that you would say."
kill_prompt = "You are watching a player play Valorant. The player has just killed an enemy. Give 5 snarky and sarcastic remarks that you would say."

death_files = deque()
kill_files = deque()

tts = TTSClass()

def recompute_deaths():
	new_msgs = get_completion(death_prompt)
	for msg in new_msgs.split("\n"):
		idx = random.randint(0, 1000000)
		death_files.append(f"death_{idx}.wav")
		tts.into_file(msg, death_files[-1])

def recompute_kills():
	new_msgs = get_completion(kill_prompt)
	for msg in new_msgs.split("\n"):
		idx = random.randint(0, 1000000)
		kill_files.append(f"kill_{idx}.wav")
		tts.into_file(msg, kill_files[-1])

def say(fidx):
	tts.play_file(fidx)
	os.remove(fidx)

def main():
	while True:
		if len(death_files) < 2:
			recompute_deaths()
		if len(kill_files) < 2:
			recompute_kills()

		scr = capt_scr()
		if game.is_dead(scr):
			continue # don't pick up events while dead (since we're spectating another player)
		if game.died(scr):
			say(death_files.popleft())
		elif game.kill(scr):
			say(kill_files.popleft())

		time.sleep(0.05)

def debug():
	img = Image.open("nokill2.png")
	print(game.died(img))
	sys.exit(0)

if __name__ == "__main__":
	# debug()
	
	print("switch to the game, fast!")
	time.sleep(5)
	main()