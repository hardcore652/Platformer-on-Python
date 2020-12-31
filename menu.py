#!/usr/local/bin/python
# coding: utf-8
from pygame import *
import pygame
pygame.init()
from settings import *
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
script_dir = __file__
script_dir = script_dir.replace('menu.py', '')
clock = time.Clock()
screen = pygame.display.set_mode(DISPLAY)
display.set_caption('MAIN MENU')
FONT = pygame.font.SysFont('Arial', 30)
WIN_CENTER_X = WIN_WIDTH // 2
WIN_CENTER_Y = WIN_HEIGHT // 2
Help = False
selected = 1
with open(script_dir+"current_lvl.txt", "r") as f:
	lvl = f.readline()
def help_draw():
	text_1 = FONT.render('WASD - MOVE', 1, (200, 200, 200))
	text_2 = FONT.render('LMB - SHOOT', 1, (200, 200, 200))
	text_3 = FONT.render('IF YOU TOUCH THE RED BLOCK YOU WILL DIE', 1, (200, 200, 200))
	text_4 = FONT.render('YOU CAN PICK UP WEAPON AND GREY BLOCKS', 1, (200, 200, 200))
	text_5 = FONT.render("IF THE ENEMY SEES YOU THEY'LL START SHOOTING", 1, (200, 200, 200))
	text_7 = FONT.render('E - PICK UP, DROP', 1, (200, 200, 200))
	text_6 = FONT.render('IN THE LOWER LEFT CORNER YOU CAN SEE INFORMATION ABOUT COOLDOWN, HEALTH AND AMMO', 1, (200, 200, 200))
	text_8 = FONT.render('YOU CAN JUMP WHEN YOU PASS THROUGH THE YELLOW ORB', 1, (200, 200, 200))
	text_9 = FONT.render('ENTER - GO TO MAIN MENU', 1, (200, 200, 200))
	text_10 = FONT.render('IF YOU PUT THE GREY BLOCK ON THE BUTTON, THE DOOR WILL OPEN', 1, (200, 200, 200))
	screen.blit(text_1, (5, 10))
	screen.blit(text_2, (5, 50))
	screen.blit(text_7, (5, 90))
	screen.blit(text_3, (5, 130))
	screen.blit(text_10, (5, 170))
	screen.blit(text_4, (5, 210))
	screen.blit(text_5, (5, 250))
	screen.blit(text_6, (5, 290))
	screen.blit(text_8, (5, 330))
	screen.blit(text_9, (5, 380))
def main_menu():
	text_0 = FONT.render('^  or  v  to move and  ENTER  to select', 1, (200, 200, 200))
	if int(lvl) > 0:
		if selected == 1: text_1 = FONT.render('> CONTINUE GAME', 1, (200, 200, 200))
		else: text_1 = FONT.render('CONTINUE GAME', 1, (200, 200, 200))
	else:
		if selected == 1: text_1 = FONT.render('> START GAME', 1, (200, 200, 200))
		else: text_1 = FONT.render('START GAME', 1, (200, 200, 200))
	if selected == 2: text_2 = FONT.render('> HELP', 1, (200, 200, 200))
	else: text_2 = FONT.render('HELP', 1, (200, 200, 200))
	if selected == 3: text_3 = FONT.render('> LEVEL EDITOR', 1, (200, 200, 200))
	else: text_3 = FONT.render('LEVEL EDITOR', 1, (200, 200, 200))
	text_0_rect = text_0.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - 150))
	text_1_rect = text_1.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - 50))
	text_2_rect = text_2.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y + 50))
	text_3_rect = text_3.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y + 150))
	screen.blit(text_0, text_0_rect)
	screen.blit(text_1, text_1_rect)
	screen.blit(text_2, text_2_rect)
	screen.blit(text_3, text_3_rect)

while 1:
	clock.tick(30)
	for e in event.get():
		if e.type == QUIT: pygame.quit()
		if not Help:
			if e.type == KEYDOWN and e.key == K_RETURN:
				if selected == 1:
					pygame.quit()
					import game
				if selected == 2:
					Help = True
				if selected == 3:
					pygame.quit()
					import level_editor
			if e.type == KEYDOWN and e.key == K_UP and selected > 1: selected -= 1
			if e.type == KEYDOWN and e.key == K_DOWN and selected < 3: selected += 1
		else:
			if e.type == KEYDOWN and e.key == K_RETURN:
				Help = False
	screen.fill((40, 50, 40))
	if Help: help_draw()
	else: main_menu()
	display.update()