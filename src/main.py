from PIL import Image
import matplotlib.pyplot as plt
from valorant import *
import random
import time
from util import get_completion, TTSClass, capt_scr
import sys

game = Game()
last_msg = 0

# death_prompt = "You are watching a player play Valorant. The player has just died. Respond with a snarky remark in one sentence only."
# kill_prompt = "You are watching a player play Valorant. The player has just killed an enemy. Respond with a snarky remark in one sentence only."

death_phrases = [
    "Nice try… if you were aiming at the wall.",
    "Wow, that was fast. Did you blink?",
    "You call that positioning?",
    "They didn't even break a sweat.",
    "Outplayed. Brutally.",
    "And… you're gone.",
    "That's one way to warm up the bench.",
    "I've seen bots survive longer.",
    "You really wanted to test the respawn screen, huh?",
    "Hope your team's enjoying the 4v5."
]

kill_phrases = [
    "Wow… even a broken clock's right twice a day.",
    "Pure luck. Don't kid yourself.",
    "Congrats, you actually hit something.",
    "Even I'm surprised that worked.",
    "Was that skill or just panic?",
    "Beginner's luck strikes again.",
    "You aimed there on purpose… right?",
    "Miracles do happen, apparently.",
    "Mark the date, you landed a shot.",
    "Don't get used to that."
]

def say(msg):
	global last_msg
	if time.time() - last_msg < 3:
		return
	tts = TTSClass()
	tts.start(msg)
	del(tts)
	last_msg = time.time()

def main():
	while True:
		scr = capt_scr()
		if game.is_dead(scr):
			continue # don't pick up events while dead (since we're spectating another player)
		if game.died(scr):
			say(random.choice(death_phrases))
		elif game.kill(scr):
			say(random.choice(kill_phrases))

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