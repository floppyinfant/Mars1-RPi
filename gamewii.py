#!/usr/bin/env python

# project title:        gamewii.py
# by author:            Totman
# web:                  http://www.floppyinfant.com/
# version, date:        0.1, 2015-01-14
# license:
# Copyright (C) 2015, all rights reserved

__author__ = "Totman"
__copyright__ = "Copyright (C) 2015 Totman"
__license__ = "Public Domain"
__version__ = "0.1"

"""
Wiimote Controller for Pygame

@see https://www.python.org/
@see http://www.pygame.org/docs/
@see PYTHON_HOME/lib/site-packages/pygame/examples/sound.py | midi.py
@see http://inventwithpython.com/pygame/downloads/gemgem.py

@see https://pypi.python.org/pypi/RPi.GPIO
@see https://github.com/WiringPi/WiringPi2-Python
@see cwiid

"""

import sys
import os
import os.path
#import time
#import argparse    #TODO
#import webbrowser

import pygame
from pygame.locals import *
import pygame.midi
#import pygame.mixer_music

#import RPi.GPIO as GPIO
import cwiid

#############################################################
# globals
DEBUG = 3   # debug level

wii = cwiid.Wiimote()

# Raspberry Pi
#GPIO.setmode(GPIO.BCM)

# constants
FPS = 30  # frames per second to update the screen
WINDOWWIDTH = 800  # width of the program's window, in pixels
WINDOWHEIGHT = 300  # height in pixels

#                R    G    B
WHITE        = (255, 255, 255)
DARKGRAY     = ( 40,  40,  40)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
# RED	     = (255, 100, 100)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
# BLUE	     = (  0,   0, 255)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
PURPLE       = (255,   0, 255)
LIGHTBLUE    = (170, 190, 255)
BROWN        = (  85, 65,   0)

# colors
BGCOLOR = WHITE


def print_device_info():
    """ MIDI-Devices present on that machine """

    pygame.midi.init()

    for i in range(pygame.midi.get_count()):
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
    """ Print usage and exit """
    # TODO print usage
    # print("usage: python <progname> --switch_longname [optional_args]")
    print("--list : list available midi devices")


# TODO: Resource Manager
class ResourceManager():
    """ Resource Manager
    keeps all loaded resources in one place
    """
    def __init__(self):
        self.FONTS = {}
        self.IMAGES = {}
        self.SOUNDS = {}

    def add_sound(self, name, filename):
        self.SOUNDS[name] = filename


def main():
    global FPSCLOCK, DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    # set up the window
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Drum Kit Kit')

    #############################################################
    # initialize resources
    # get path
    main_dir = os.path.split(os.path.abspath(__file__))[0]

    # load images
    # set absolute path to file
    file_path_image = os.path.join(main_dir, 'data', 'img', 'cat.png')
    try:
        img = pygame.image.load(file_path_image)
    except pygame.error:
        raise SystemExit('Could not load file "%s" %s' % (file_path_image, pygame.get_error()))

    # load fonts
    file_path_font = os.path.join(main_dir, 'data', 'fnt', 'lcd.ttf')
    try:
        BASICFONT = pygame.font.Font(file_path_font, 36)
    except pygame.error:
        raise SystemExit('Could not load file "%s" %s' % (file_path_font, pygame.get_error()))

    # load sounds
    # choose a desired audio format
    # TODO
    pygame.mixer.init(11025)

    # constants
    BD = 'Bassdrum'
    SD = 'Snare'
    HHC = 'Closed_Hi_Hat'
    HHO = 'Open_Hi_Hat'

    # set absolute path to sample
    # select sound sample files
    file_path_bd = os.path.join(main_dir, 'data', 'snd', 'BBox', 'Tr-808', 'Bassdrum', 'Bdrum1.wav')
    file_path_sd = os.path.join(main_dir, 'data', 'snd', 'BBox', 'Tr-909', 'Snares', 'Snare1.wav')
    file_path_hhc = os.path.join(main_dir, 'data', 'snd', 'BBox', 'Tr-909', 'Cymbals', 'Hhclose1.wav')
    file_path_hho = os.path.join(main_dir, 'data', 'snd', 'BBox', 'Tr-909', 'Cymbals', 'Hhopen1.wav')
    # load sound files
    SOUNDS = {}
    try:
        SOUNDS[BD] = pygame.mixer.Sound(file_path_bd)
    except pygame.error:
        raise SystemExit('Could not load file "%s" %s' % (file_path_bd, pygame.get_error()))
    try:
        SOUNDS[SD] = pygame.mixer.Sound(file_path_sd)
    except pygame.error:
        raise SystemExit('Could not load file "%s" %s' % (file_path_sd, pygame.get_error()))
    try:
        SOUNDS[HHC] = pygame.mixer.Sound(file_path_hhc)
    except pygame.error:
        raise SystemExit('Could not load file "%s" %s' % (file_path_hhc, pygame.get_error()))
    try:
        SOUNDS[HHO] = pygame.mixer.Sound(file_path_hho)
    except pygame.error:
        raise SystemExit('Could not load file "%s" %s' % (file_path_hho, pygame.get_error()))

    # load background music
    # you can load a .wav, .ogg, (.mp3), .mid
    file_path_music = os.path.join(main_dir, 'data', 'music', 'boratto bd-clk-noi 125.wav')
    #file_path_music = os.path.join(main_dir, 'data', 'mid', 'tetrisb.mid')
    try:
        pygame.mixer.music.load(file_path_music)
        #pygame.mixer.music.play(-1)
    except pygame.error:
        raise SystemExit('Could not load file "%s" %s' % (file_path_music, pygame.get_error()))

    #  MIDI
    pygame.midi.init()
    port = pygame.midi.get_default_output_id()
    MIDI_OUT = pygame.midi.Output(port, 0)      # close MIDI Device in finally statement, when done
    # set instrument
    instrument = 0  # values 0 - 127
    MIDI_OUT.set_instrument(instrument)
    # note on parameter
    tune = 48
    velocity = 120

    #############################################################
    # initialize local variables

    # image
    mouse_x = 0
    mouse_y = 0
    last_mouse_down_x = 0
    last_mouse_down_y = 0

    # music
    is_music_playing = False

    # the main loop
    while True:
        # TODO: fill all - or just the parts that need to be redrawn?!
        DISPLAYSURF.fill(BGCOLOR)

        # draw images
        DISPLAYSURF.blit(img, (mouse_x, mouse_y))

        # draw text
        text = BASICFONT.render('Drum Kit Kit', 1, BLUE)
        text_rect = text.get_rect()
        text_rect.topleft = (WINDOWWIDTH / 2, 10)
        DISPLAYSURF.blit(text, text_rect)

        # event handling loop
        for event in pygame.event.get():
            #################################################################
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #################################################################
            # Keyboard
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    # you could display a confirmation window
                    pygame.quit()
                    sys.exit()
                elif event.key == K_BACKSPACE:
                    # leave function
                    return
                # MIDI note on
                elif event.key == K_z:  # deutsches Layout 'y'
                    note = tune + 0
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_s:
                    note = tune + 1
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_x:
                    note = tune + 2
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_d:
                    note = tune + 3
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_c:
                    note = tune + 4
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_v:
                    note = tune + 5
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_g:
                    note = tune + 6
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_b:
                    note = tune + 7
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_h:
                    note = tune + 8
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_n:
                    note = tune + 9
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_j:
                    note = tune + 10
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_m:
                    note = tune + 11
                    MIDI_OUT.note_off(note, 0)
                elif event.key == K_COMMA:
                    note = tune + 12
                    MIDI_OUT.note_off(note, 0)
            #################################################################
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    if DEBUG >= 2:
                        print "play BD: " + str(SOUNDS[BD])
                    SOUNDS[BD].play()
                elif event.key == K_2:
                    if DEBUG >= 2:
                        print "play SD: " + str(SOUNDS[SD])
                    SOUNDS[SD].play()
                elif event.key == K_3:
                    if DEBUG >= 2:
                        print "play HHC: " + str(SOUNDS[HHC])
                    SOUNDS[HHC].play()
                elif event.key == K_4:
                    if DEBUG >= 2:
                        print "play HHO: " + str(SOUNDS[HHO])
                    SOUNDS[HHO].play()
                elif event.key == K_SPACE:
                    # toggle background music
                    if is_music_playing:
                        is_music_playing = False
                        pygame.mixer.music.fadeout(1000)
                        # pygame.mixer.music.stop()
                    else:
                        is_music_playing = True
                        pygame.mixer.music.play(-1)
                # MIDI note on
                elif event.key == K_z:  # deutsches Layout 'y'
                    note = tune + 0
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_s:
                    note = tune + 1
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_x:
                    note = tune + 2
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_d:
                    note = tune + 3
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_c:
                    note = tune + 4
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_v:
                    note = tune + 5
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_g:
                    note = tune + 6
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_b:
                    note = tune + 7
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_h:
                    note = tune + 8
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_n:
                    note = tune + 9
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_j:
                    note = tune + 10
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_m:
                    note = tune + 11
                    MIDI_OUT.note_on(note, velocity)
                elif event.key == K_COMMA:
                    note = tune + 12
                    MIDI_OUT.note_on(note, velocity)
                # movement in game
                elif event.key == K_w:
                    # move UP
                    if DEBUG >= 2:
                        print "UP"
                elif event.key == K_a:
                    # move LEFT
                    if DEBUG >= 2:
                        print "LEFT"
                elif event.key == K_d:
                    # move RIGHT
                    if DEBUG >= 2:
                        print "RIGHT"
                elif event.key == K_s:
                    # move DOWN
                    if DEBUG >= 2:
                        print "DOWN"
                elif event.key == K_e:
                    # change tool
                    if DEBUG >= 2:
                        print "TOOL SELECT"
            #################################################################
            # Mouse
            elif event.type == MOUSEBUTTONUP:
                if event.pos == (last_mouse_down_x, last_mouse_down_y):
                    # This event is a mouse click, not the end of a mouse drag.
                    mouse_x, mouse_y = event.pos
                    # check for clicks on display-buttons
                    if pygame.Rect(74, 16, 111, 30).collidepoint(mouse_x, mouse_y):
                        # do something
                        pass
                else:
                    # this is the end of a mouse drag
                    pass
            elif event.type == MOUSEBUTTONDOWN:
                # this is the start of a mouse click or mouse drag
                last_mouse_down_x, last_mouse_down_y = event.pos
            elif event.type == MOUSEMOTION:
                # ???
                pass
            #################################################################
            # MIDI events
            elif event.type == pygame.midi.MIDIIN:
                # @see pygame.midi.midis2events()
                pass
            #
            #################################################################

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    # finally close MIDI Device
    del MIDI_OUT
    pygame.midi.quit()

if __name__ == '__main__':

    try:
        # parse args
        if "--help" in sys.argv or "-h" in sys.argv:
            usage()
        elif "--list" in sys.argv or "-l" in sys.argv:
            print_device_info()
        else:
            # usage()
            try:
                main()
            except KeyboardInterrupt:
                print "Aborting by user request."

        # or check for optional args
        """
        if len(sys.argv) > 1:
            main(sys.argv[1])
        else:
            main()
        """

        # or use module argparse

        # or use module getopt (C style)

    except KeyboardInterrupt:
        pass

""" NOTES

# play a sound
channel = sound.play()
# poll until finished
while channel.get_busy():  # still playing
    pygame.time.wait(10)   # poll interval


# MIDI

MIDI_OUT.note_on(note, velocity)
pygame.time.wait(400)
MIDI_OUT.note_off(note, 0)


webbrowser.open('http://inventwithpython.com')

# scaling
if img.get_size() != (IMAGESIZE, IMAGESIZE):
    img = pygame.transform.smoothscale(img, (IMAGESIZE, IMAGESIZE))

"""
