from PIL import Image
import matplotlib.pyplot as plt
from valorant import *
import random
import time
from util import get_completion, TTS, capt_scr
import sys

game = Game()
last_msg = 0

death_prompt = "You are watching a player play Valorant. The player has just died. Respond with a snarky remark in one sentence only."
kill_prompt = "You are watching a player play Valorant. The player has just killed an enemy. Respond with a snarky remark in one sentence only."

def say(msg):
	global last_msg
	if time.time() - last_msg < 3:
		return
	tts = TTS()
	tts.start(msg)
	del(tts)
	last_msg = time.time()

def main():
	while True:
		scr = capt_scr()
		if game.is_dead(scr):
			continue # don't pick up events while dead (since we're spectating another player)
		if game.died(scr):
			say(get_completion(death_prompt))
		elif game.kill(scr):
			say(get_completion(kill_prompt))

		time.sleep(0.05)

def debug():
	img = Image.open("kill.png")
	print(game.died(img))
	sys.exit(0)

if __name__ == "__main__":
	# debug()
	
	print("switch to the game, fast!")
	time.sleep(5)
	main()