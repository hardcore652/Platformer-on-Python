from pygame import *
from subprocess import call
import pygame
init()
from settings import *
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
script_dir = __file__
script_dir = script_dir.replace('starter.py', '')
clock = time.Clock()
screen = pygame.display.set_mode(DISPLAY)
display.set_caption('HOW TO PLAY')
with open(script_dir+"lvl.txt", "r") as f:
	lvl = f.readline()
while 1:
	clock.tick(30)
	for e in event.get():
		if e.type == QUIT: pygame.quit()
	screen.fill((255, 255, 255))
	text_1 = font.render('WASD - MOVE', 1, (0, 0, 0))
	text_2 = font.render('LMB - SHOOT', 1, (0, 0, 0))
	text_3 = font.render('IF YOU TOUCH THE RED BLOCK YOU WILL DIE', 1, (0, 0, 0))
	text_4 = font.render('IF YOU APPROACH A WEAPON YOU WILL PICK IT UP', 1, (0, 0, 0))
	text_5 = font.render("IF THE ENEMY SEES YOU THEY'LL START SHOOTING", 1, (0, 0, 0))
	text_6 = font.render('IN THE LOWER LEFT CORNER YOU CAN SEE INFORMATION ABOUT COOLDOWN, HEALTH AND AMMO', 1, (0, 0, 0))
	text_8 = font.render('YOU CAN JUMP WHEN YOU PASS THROUGH THE YELLOW ORB', 1, (0, 0, 0))
	text_9 = font.render('PRESS ENTER TO START', 1, (0, 0, 0))
	screen.blit(text_1, (5, 10))
	screen.blit(text_2, (5, 50))
	screen.blit(text_3, (5, 90))
	screen.blit(text_4, (5, 130))
	screen.blit(text_5, (5, 170))
	screen.blit(text_6, (5, 210))
	screen.blit(text_8, (5, 250))
	screen.blit(text_9, (5, 350))
	keys = key.get_pressed()
	if keys[K_RETURN]:
		pygame.quit()
		call(['python', script_dir + 'lvl_'+lvl+'.py'])
		break
	display.update()