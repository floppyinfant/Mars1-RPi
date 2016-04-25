#!/usr/bin/env python

# project title
# by author
# web
# version, date
# license

"""
@see http://www.pygame.org/docs/
@see PYTHON_HOME/lib/site-packages/pygame/examples
sound.py
midi.py
@see http://inventwithpython.com/pygame/downloads/
gemgem.py
"""

import pygame
from pygame.locals import *
import pygame.midi
# other libraries
import sys
import os
import os.path

# globals

# constants
FPS = 30 # frames per second to update the screen
WINDOWWIDTH = 600  # width of the program's window, in pixels
WINDOWHEIGHT = 600 # height in pixels

#			 R	G	B
WHITE		= (255, 255, 255)
DARKGRAY	 = ( 40,  40,  40)
BLACK		= (  0,   0,   0)

BRIGHTRED	= (255,   0,   0)
RED		  = (155,   0,   0)		# RED	   = (255, 100, 100)
BRIGHTGREEN  = (  0, 255,   0)
GREEN		= (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE		 = (  0,   0, 155)		# BLUE	  = (  0,   0, 255)
BRIGHTYELLOW = (255, 255,   0)
YELLOW	   = (155, 155,   0)

PURPLE	= (255,   0, 255)
LIGHTBLUE = (170, 190, 255)
BROWN	 = ( 85,  65,   0)

# colors
BGCOLOR = WHITE


def print_device_info():
	"""MIDI-Devices present on that machine"""

	pygame.midi.init()

	for i in range( pygame.midi.get_count() ):
		r = pygame.midi.get_device_info(i)
		(interf, name, input, output, opened) = r

		in_out = ""
		if input:
			in_out = "(input)"
		if output:
			in_out = "(output)"

		print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" % (i, interf, name, opened, in_out))

	pygame.midi.quit()


def usage():
	"""Print usage and exit"""
	#print("usage: python <progname> --switch_longname [optional_args]")
	print("--list : list available midi devices")


def main():
	global FPSCLOCK, DISPLAYSURF

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	# set up the window
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('PyGame')


	# load images
	img = pygame.image.load('cat.png')
	#if img.get_size() != (IMAGESIZE, IMAGESIZE):
	#	img = pygame.transform.smoothscale(img, (IMAGESIZE, IMAGESIZE))


	# load fonts
	BASICFONT = pygame.font.Font('freesansbold.ttf', 36)


	# load sounds
	# choose a desired audio format
	pygame.mixer.init(11025)
	# get path
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	# set absolute path to sample
	file_path = os.path.join(main_dir, 'res', 'bdrum.wav')
	# load sound file
	snd = pygame.mixer.Sound(file_path)
	#
	# using a collection
	#SOUNDS = {}
	#SOUNDS['bad swap'] = pygame.mixer.Sound('badswap.wav')
	#SOUNDS['match'] = []
	#for i in range(NUMSOUNDS):
	#	SOUNDS['match'].append(pygame.mixer.Sound('match%s.wav' % i))


	# MIDI
	pygame.midi.init()
	port = pygame.midi.get_default_output_id()
	midi_out = pygame.midi.Output(port, 0)

	# put all MIDI stuff in try - finally statement
	try:
		instrument = 0  # values 0 - 127
		midi_out.set_instrument(instrument)
		note = 60
		velocity = 120
		midi_out.note_on(note, velocity)
		pygame.time.wait(2000)
		midi_out.note_off(note, 0)
	finally:
		del midi_out
		pygame.midi.quit()


	# the main game loop
	while True:
		DISPLAYSURF.fill(BGCOLOR)

		# draw images
		x = 0
		y = 0
		DISPLAYSURF.blit(img, (x, y))


		# draw text
		scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = (WINDOWWIDTH - 100, 10)
		DISPLAYSURF.blit(scoreSurf, scoreRect)


		# play a sound
		print('Playing Sound...')
		channel = sound.play()
		#poll until finished
		while channel.get_busy(): #still playing
			print("...")
			time.wait(1000)
		print("...Finished!")


		# event handling loop
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					# you could display a confirmation window
					pygame.quit()
					sys.exit()
				elif event.key == K_BACKSPACE:
					# leave function
					return
			elif event.type == KEYDOWN:
				if event.key == K_w:
					# move UP
				elif event.key == K_a:
					# move LEFT
				elif event.key == K_d:
					# move RIGHT
				elif event.key == K_s:
					# move DOWN
				elif event.key == K_e:
					# change tool				
			elif event.type == MOUSEBUTTONUP:
				if event.pos == (lastMouseDownX, lastMouseDownY):
					# This event is a mouse click, not the end of a mouse drag.
					x, y = event.pos
					# check for clicks on buttons
					if pygame.Rect(74, 16, 111, 30).collidepoint(x, y):
						# play sound
						snd.play()
				else:
					# this is the end of a mouse drag
					
			elif event.type == MOUSEBUTTONDOWN:
				# this is the start of a mouse click or mouse drag
				lastMouseDownX, lastMouseDownY = event.pos
			elif event.type == pygame.midi.MIDIIN:
				# @see pygame.midi.midis2events()

		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':

	# parse args
	if "" in sys.argv:

	elif "--list" in sys.argv or "-l" in sys.argv:
		print_device_info()
	else:
		usage()

	# or check for optional args
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()

	# or just run main()
	main()

pygame.midi.quit()

#####################################################################
# others
# pygame.time.wait(2000) # pause so the player can bask in victory
# webbrowser.open('http://inventwithpython.com')
#####################################################################
