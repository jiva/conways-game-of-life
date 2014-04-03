#!/usr/bin/env python

# Conway's Game of Life in python + curses
# by jiva

import curses
import time
import random
import sys

try:
	# Return the number of neighbors (8 surrounding cells) that are alive
	# -1,-1    0,-1     +1,-1
	# -1,0     0,0      +1,0
	# -1,+1    0,+1     +1,+1 
	def getLiveNeighbors(_cells, _x, _y, _maxheight, _maxwidth):
		numlive = 0
		
		# top left
		if _x-1 > 0 and _y-1 > 0:
			if _cells[_x-1,_y-1]: numlive += 1
		# top middle
		if _y-1 > 0:
			if _cells[_x,_y-1]: numlive += 1
		# top right
		if _x+1 < _maxwidth and _y-1 > 0:
			if _cells[_x+1,_y-1]: numlive += 1
		# left
		if _x-1 > 0:
			if _cells[_x-1,_y]: numlive += 1
		# right
		if _x+1 < _maxwidth:
			if _cells[_x+1,_y]: numlive += 1
		# bottom left
		if _x-1 > 0 and _y+1 < _maxheight:
			if _cells[_x-1,_y+1]: numlive += 1
		# bottom middle
		if _y+1 < _maxheight:
			if _cells[_x,_y+1]: numlive += 1
		# bottom right
		if _x+1 < _maxwidth and _y+1 < _maxheight:
			if _cells[_x+1,_y+1]: numlive += 1
		return numlive

	# Window which represents the entire screen, will be the board
	board = curses.initscr()

	# Don't echo keyboard input onto the screen
	curses.noecho()

	# Get height and width
	height,width = board.getmaxyx()
	width -= 1 # hack

	# Keep track of cells
	cells = {}

	# Print intro
	board.addstr(height/2, width/2-20, 'Conway\'s Game of Life by jiva\n')
	board.refresh()
	time.sleep(2)

	# Populate cells with a random initial configuration
	# Also print initial board
	for y in xrange(height):
		for x in xrange(width):
			cells[x,y] = random.choice([True,False])
			board.addstr(y, x, '.' if cells[x,y] else ' ')
			board.refresh()

	# Start (inefficient) generational loop
	while True:
		time.sleep(.1)
		ncells = {} # next generation of cells
		for y in xrange(height):
			for x in xrange(width):
				liveneighbors = getLiveNeighbors(cells, x, y, height, width)
				if liveneighbors < 2:
					ncells[x,y] = False
				if liveneighbors == 2 or liveneighbors == 3:
					ncells[x,y] = cells[x,y]
				if liveneighbors > 3:
					ncells[x,y] = False
				if not cells[x,y] and liveneighbors == 3:
					ncells[x,y] = True

		# Print board (and update with new generation)
		for y in xrange(height):
			for x in xrange(width):
				cells[x,y] = ncells[x,y]
				board.addstr(y, x, '.' if cells[x,y] else ' ')
		board.refresh()

except:
	e = sys.exc_info()[0]
	# Cleanly exit
	time.sleep(1)
	curses.echo()
	curses.endwin()
	print e