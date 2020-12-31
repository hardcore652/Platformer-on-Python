#!/usr/local/bin/python
# coding: utf-8
from pygame import *
import pygame
import os
from time import sleep
pygame.init()
from settings import *
size_multiplier = 1920 / WIN_WIDTH
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
PLATFORM_WIDTH, PLATFORM_HEIGHT = int(64 / size_multiplier), int(64 / size_multiplier)
HERO_WIDTH, HERO_HEIGHT = int(64 / size_multiplier), int(64 / size_multiplier)
script_dir = __file__
script_dir = script_dir.replace('level_editor.py', '')
clock = time.Clock()
screen = pygame.display.set_mode(DISPLAY, DOUBLEBUF)
WIN_CENTER_X = WIN_WIDTH // 2
WIN_CENTER_Y = WIN_HEIGHT // 2
FONT = pygame.font.SysFont('Arial', int(30 / size_multiplier))
SMALL_FONT = pygame.font.SysFont('Arial', int(19 / size_multiplier))
choose = 1
size = None
create_first = 0
edit_first = 0
create_second = 0
edit_second = 0
lvls_list = os.listdir(script_dir + 'Levels/')
for lvl in lvls_list:
	last_lvl = int(lvl.replace('lvl_', '').replace('.txt', ''))
yorb_img = image.load(script_dir+"Sprites/yorb0.png").convert_alpha() # прогружаем картинки спрайтов
player_img = image.load(script_dir+"Sprites/player.png").convert_alpha()
enemy_image = image.load(script_dir+"Sprites/enemy.png").convert_alpha()
brick_img = image.load(script_dir+"Sprites/bricks.png").convert_alpha()
shotgun_img = image.load(script_dir+"Sprites/shotgun.png").convert_alpha()
firegun_img = image.load(script_dir+"Sprites/flamethrower.png").convert_alpha()
pistol_img = image.load(script_dir+"Sprites/pistol.png").convert_alpha()
falling_block_img = image.load(script_dir+"Sprites/falling_block.png").convert_alpha()
finish_img = image.load(script_dir+"Sprites/finish.png").convert_alpha()
planks_img = image.load(script_dir+"Sprites/planks.png").convert_alpha()
rubber_img = image.load(script_dir+"level_editor_icons/rubber.png").convert_alpha()
toolbar_img = image.load(script_dir+"level_editor_icons/toolbar.png").convert_alpha()
cube_img = Surface((HERO_WIDTH, HERO_HEIGHT)).convert_alpha()
cube_img.fill((100, 100, 100))
button_img = image.load(script_dir+"level_editor_icons/button.png").convert_alpha()
door_img = Surface((HERO_WIDTH, HERO_HEIGHT)).convert_alpha()
door_img.fill((0, 0, 255))
dirt_img = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)).convert_alpha()
dirt_img.fill((168, 74, 43))
grass_img = [Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)).convert_alpha(), Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT // 4)).convert_alpha()]
grass_img[0].fill((168, 74, 43))
grass_img[1].fill((0, 176, 0))
kill_block_img = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT)).convert_alpha()
kill_block_img.fill((200,0,0))
alpha_block_img = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
alpha_block_img.fill((255, 150, 0))
alpha_block_img.set_alpha(65)

first = 1
while first:
	clock.tick(30)
	screen.fill((40, 50, 40))
	text_0 = FONT.render('LEVEL EDITOR ALPHA', 1, (200, 200, 200))
	if choose == 1: text_1 = FONT.render('> CREATE LEVEL', 1, (200, 200, 200))
	else: text_1 = FONT.render('CREATE LEVEL', 1, (200, 200, 200))
	if choose == 2: text_2 = FONT.render('> EDIT LEVEL', 1, (200, 200, 200))
	else: text_2 = FONT.render('EDIT LEVEL', 1, (200, 200, 200))
	text_0_rect = text_0.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - int(120 / size_multiplier)))
	text_1_rect = text_1.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - int(20 / size_multiplier)))
	text_2_rect = text_2.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y + int(80 / size_multiplier)))
	screen.blit(text_0, text_0_rect)
	screen.blit(text_1, text_1_rect)
	screen.blit(text_2, text_2_rect)
	for e in event.get():
		if e.type == QUIT: pygame.quit()
		if e.type == KEYDOWN and e.key == K_UP and choose > 1: choose -= 1
		if e.type == KEYDOWN and e.key == K_DOWN and choose < 2: choose += 1
		if e.type == KEYDOWN and e.key == K_RETURN:
			if choose == 1: create_first = 1
			else: edit_first = 1
			choose = 1
			first = 0
	display.update()

if edit_first:
	enter = ''
	choosed_lvl = None
while edit_first:
	clock.tick(30)
	screen.fill((40, 50, 40))
	text_0 = FONT.render('ENTER LEVEL NUMBER', 1, (200, 200, 200))
	text_0_rect = text_0.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - int(200 / size_multiplier)))
	screen.blit(text_0, text_0_rect)
	text_1 = FONT.render(enter + '_', 1, (200, 200, 200))
	text_1_rect = text_1.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - int(100 / size_multiplier)))
	screen.blit(text_1, text_1_rect)
	for e in event.get():
		if e.type == QUIT: pygame.quit()
		if e.type == KEYDOWN:
			if e.key == K_1 or e.key == K_KP1:
				enter = enter + '1'
			if e.key == K_2 or e.key == K_KP2:
				enter = enter + '2'
			if e.key == K_3 or e.key == K_KP3:
				enter = enter + '3'
			if e.key == K_4 or e.key == K_KP4:
				enter = enter + '4'
			if e.key == K_5 or e.key == K_KP5:
				enter = enter + '5'
			if e.key == K_6 or e.key == K_KP6:
				enter = enter + '6'
			if e.key == K_7 or e.key == K_KP7:
				enter = enter + '7'
			if e.key == K_8 or e.key == K_KP8:
				enter = enter + '8'
			if e.key == K_9 or e.key == K_KP9:
				enter = enter + '9'
			if e.key == K_0 or e.key == K_KP0:
				enter = enter + '0'
			if e.key == K_BACKSPACE:
				enter = enter[0:-1]
			if e.key == K_RETURN:
				if enter != '':
					choosed_lvl = int(enter)
					edit_second = 1
					edit_first = 0
				else:
					pygame.quit()
					for i in range(10):
						print('INCORRECT LEVEL NAME')
					sleep(10)
	display.update()

while create_first:
	clock.tick(30)
	screen.fill((40, 50, 40))
	text_0 = FONT.render('CHOOSE LVL SIZE', 1, (200, 200, 200))
	if choose == 1: text_1 = FONT.render('> SMALL 40x15', 1, (200, 200, 200))
	else: text_1 = FONT.render('SMALL 40x15', 1, (200, 200, 200))
	if choose == 2: text_2 = FONT.render('> MEDIUM 60x20', 1, (200, 200, 200))
	else: text_2 = FONT.render('MEDIUM 60x20', 1, (200, 200, 200))
	if choose == 3: text_3 = FONT.render('> LARGE 90x35', 1, (200, 200, 200))
	else: text_3 = FONT.render('LARGE 90x35', 1, (200, 200, 200))
	text_0_rect = text_0.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - int(200 / size_multiplier)))
	text_1_rect = text_1.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y - int(80 / size_multiplier)))
	text_2_rect = text_2.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y + int(20 / size_multiplier)))
	text_3_rect = text_3.get_rect(center=(WIN_CENTER_X, WIN_CENTER_Y + int(120 / size_multiplier)))
	screen.blit(text_0, text_0_rect)
	screen.blit(text_1, text_1_rect)
	screen.blit(text_2, text_2_rect)
	screen.blit(text_3, text_3_rect)
	for e in event.get():
		if e.type == QUIT: pygame.quit()
		if e.type == KEYDOWN and e.key == K_UP and choose > 1: choose -= 1
		if e.type == KEYDOWN and e.key == K_DOWN and choose < 3: choose += 1
		if e.type == KEYDOWN and e.key == K_RETURN:
			size = choose
			choose = 1
			create_first = 0
			create_second = 1
	display.update()


mouse_x = mouse_y = 0
if size == 1: size_x, size_y, block_size = 40, 15, int(48 / size_multiplier)
if size == 2: size_x, size_y, block_size = 60, 20, int(32 / size_multiplier)
if size == 3: size_x, size_y, block_size = 90, 35, int(21 / size_multiplier)
if create_second:
	working_level = last_lvl + 1
	with open(script_dir + "Levels/lvl_"+str(working_level)+".txt", "w+") as f:
		for i in range(size_y):
			f.write(' '*size_x + '\n')
	choosed_x = 0
	choosed_y = 0
	choosed_number_x = None
	choosed_number_y = None
if edit_second:
	working_level = choosed_lvl
	choosed_x = 0
	choosed_y = 0
	choosed_number_x = None
	choosed_number_y = None
	create_second = 1
	try:
		with open(script_dir + "Levels/lvl_"+str(working_level)+".txt", "r") as f:
			file_list = f.readlines()
	except:
		pygame.quit()
		for i in range(10):
			print('FILE NOT FOUND!')
		sleep(10)
	size_y = len(file_list)
	size_x = len(file_list[0]) - 1
	if size_x == 90:
		block_size = int(21 / size_multiplier)
		size = 3
	if size_x == 60:
		block_size = int(32 / size_multiplier)
		size = 2
	if size_x == 40:
		block_size = int(48 / size_multiplier)
		size = 1
while create_second:
	clock.tick(30)
	screen.fill((40, 50, 40))
	if choosed_x == 0 and choosed_y == 0: block = 'b'
	if choosed_x == 0 and choosed_y == 1: block = 'd'
	if choosed_x == 1 and choosed_y == 0: block = 'g'
	if choosed_x == 1 and choosed_y == 1: block = 'a'
	if choosed_x == 2 and choosed_y == 0: block = 'S'
	if choosed_x == 2 and choosed_y == 1: block = 'k'
	if choosed_x == 3 and choosed_y == 0: block = 'e'
	if choosed_x == 3 and choosed_y == 1: block = 'E'
	if choosed_x == 4 and choosed_y == 0: block = 'F'
	if choosed_x == 4 and choosed_y == 1: block = 'P'
	if choosed_x == 5 and choosed_y == 0: block = 'w'
	if choosed_x == 5 and choosed_y == 1: block = 'C'
	if choosed_x == 6 and choosed_y == 0:
		if choosed_number_x == None and choosed_number_y == None: block = ' '
		if choosed_number_x == 0 and choosed_number_y == 0: block = 'B1'
		if choosed_number_x == 1 and choosed_number_y == 0: block = 'B2'
		if choosed_number_x == 2 and choosed_number_y == 0: block = 'B3'
		if choosed_number_x == 0 and choosed_number_y == 1: block = 'B4'
		if choosed_number_x == 1 and choosed_number_y == 1: block = 'B5'
		if choosed_number_x == 2 and choosed_number_y == 1: block = 'B6'
		if choosed_number_x == 0 and choosed_number_y == 2: block = 'B7'
		if choosed_number_x == 1 and choosed_number_y == 2: block = 'B8'
		if choosed_number_x == 2 and choosed_number_y == 2: block = 'B9'
		text = 1
		for y in range(3):
			for x in range(3):
				text_img = FONT.render(str(text), 1, (200, 200, 200))
				text_rect = text_img.get_rect(center=(int(1430 / size_multiplier) + x * int(80 / size_multiplier) + int(80 / size_multiplier) // 2, int(840 / size_multiplier) + y * int(80 / size_multiplier) + int(80 / size_multiplier) // 2))
				text += 1
				screen.blit(text_img, text_rect)
				if choosed_number_x == x and choosed_number_y == y:
					pygame.draw.rect(screen, (250, 250, 250), (WIN_WIDTH - int(250 / size_multiplier) - 3 * int(80 / size_multiplier) + x * int(80 / size_multiplier), WIN_HEIGHT - 3 * int(80 / size_multiplier) + y * int(80 / size_multiplier), int(80 / size_multiplier), int(80 / size_multiplier)), 6)
				else:
					pygame.draw.rect(screen, (100, 100, 100), (WIN_WIDTH - int(250 / size_multiplier) - 3 * int(80 / size_multiplier) + x * int(80 / size_multiplier), WIN_HEIGHT - 3 * int(80 / size_multiplier) + y * int(80 / size_multiplier), int(80 / size_multiplier), int(80 / size_multiplier)), 2)
	elif choosed_x == 6 and choosed_y == 1:
		if choosed_number_x == None and choosed_number_y == None: block = ' '
		if choosed_number_x == 0 and choosed_number_y == 0: block = 'D1'
		if choosed_number_x == 1 and choosed_number_y == 0: block = 'D2'
		if choosed_number_x == 2 and choosed_number_y == 0: block = 'D3'
		if choosed_number_x == 0 and choosed_number_y == 1: block = 'D4'
		if choosed_number_x == 1 and choosed_number_y == 1: block = 'D5'
		if choosed_number_x == 2 and choosed_number_y == 1: block = 'D6'
		if choosed_number_x == 0 and choosed_number_y == 2: block = 'D7'
		if choosed_number_x == 1 and choosed_number_y == 2: block = 'D8'
		if choosed_number_x == 2 and choosed_number_y == 2: block = 'D9'
		text = 1
		for y in range(3):
			for x in range(3):
				text_img = FONT.render(str(text), 1, (200, 200, 200))
				text_rect = text_img.get_rect(center=(int(1430 / size_multiplier) + x * int(80 / size_multiplier) + int(80 / size_multiplier) // 2, int(840 / size_multiplier) + y * int(80 / size_multiplier) + int(80 / size_multiplier) // 2))
				text += 1
				screen.blit(text_img, text_rect)
				if choosed_number_x == x and choosed_number_y == y:
					pygame.draw.rect(screen, (250, 250, 250), (WIN_WIDTH - int(250 / size_multiplier) - 3 * int(80 / size_multiplier) + x * int(80 / size_multiplier), WIN_HEIGHT - 3 * int(80 / size_multiplier) + y * int(80 / size_multiplier), int(80 / size_multiplier), int(80 / size_multiplier)), 6)
				else:
					pygame.draw.rect(screen, (100, 100, 100), (WIN_WIDTH - int(250 / size_multiplier) - 3 * int(80 / size_multiplier) + x * int(80 / size_multiplier), WIN_HEIGHT - 3 * int(80 / size_multiplier) + y * int(80 / size_multiplier), int(80 / size_multiplier), int(80 / size_multiplier)), 2)
	else: choosed_number_x, choosed_number_y = None, None
	if choosed_x == 7 and choosed_y == 0: block = 'p'
	if choosed_x == 7 and choosed_y == 1: block = 's'
	if choosed_x == 8 and choosed_y == 0: block = 'f'
	if choosed_x == 8 and choosed_y == 1: block = '.'
	if choosed_x == 9: block = ' '
	working_level_img = FONT.render('LEVEL ' + str(working_level), 1, (200, 200, 200))
	working_level_img_rect = working_level_img.get_rect(center=(WIN_WIDTH - int(100 / size_multiplier), WIN_HEIGHT - int(50 / size_multiplier)))
	start_text_img = FONT.render('PRESS ENTER TO TEST LEVEL', 1, (250, 250, 250))
	screen.blit(start_text_img, (5, (size_y + 1) * block_size))
	for y in range(size_y):
		for x in range(size_x):
			with open(script_dir + "Levels/lvl_"+str(working_level)+".txt", "r") as f:
				file = f.readlines()
			line = list(file[y])
			if line[x] == 'b': screen.blit(transform.scale(brick_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'B':
				screen.blit(transform.scale(button_img, (block_size, int(block_size / (64 / 46)))), (x * block_size, y * block_size + block_size - int(block_size / (64 / 46))))
				if size == 1: font = pygame.font.SysFont('Arial', int(30 / size_multiplier))
				if size == 2: font = pygame.font.SysFont('Arial', int(20 / size_multiplier))
				if size == 3: font = pygame.font.SysFont('Arial', int(10 / size_multiplier))
				text = font.render(line[x + 1], 1, (255, 255, 255))
				text_rect = text.get_rect(center=((x + 1) * block_size + block_size // 2, y * block_size + block_size // 2))
				screen.blit(text, text_rect)
			if line[x] == 'D':
				screen.blit(transform.scale(door_img, (block_size, block_size)), (x * block_size, y * block_size))
				if size == 1: font = pygame.font.SysFont('Arial', int(30 / size_multiplier))
				if size == 2: font = pygame.font.SysFont('Arial', int(20 / size_multiplier))
				if size == 3: font = pygame.font.SysFont('Arial', int(10 / size_multiplier))
				text = font.render(line[x + 1], 1, (255, 255, 255))
				text_rect = text.get_rect(center=((x + 1) * block_size + block_size // 2, y * block_size + block_size // 2))
				screen.blit(text, text_rect)
			if line[x] == 'd': screen.blit(transform.scale(dirt_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'g':
				screen.blit(transform.scale(grass_img[0], (block_size, block_size)), (x * block_size, y * block_size))
				screen.blit(transform.scale(grass_img[1], (block_size, block_size // 4)), (x * block_size, y * block_size))
			if line[x] == 'a': screen.blit(transform.scale(alpha_block_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'S': screen.blit(transform.scale(player_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'k': screen.blit(transform.scale(kill_block_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'e': screen.blit(transform.scale(enemy_image, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'E': screen.blit(transform.scale(transform.flip(enemy_image, True, False), (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'F': screen.blit(transform.scale(falling_block_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'P': screen.blit(transform.scale(finish_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'w': screen.blit(transform.scale(planks_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'C': screen.blit(transform.scale(cube_img, (block_size, block_size)), (x * block_size, y * block_size))
			if line[x] == 'p': screen.blit(transform.scale(pistol_img, (block_size, int(block_size / (13 / 8)))), (x * block_size, y * block_size + int(10 / size_multiplier)))
			if line[x] == 's': screen.blit(transform.scale(shotgun_img, (block_size, int(block_size / (52 / 23)))), (x * block_size, y * block_size + int(10 / size_multiplier)))
			if line[x] == 'f': screen.blit(transform.scale(firegun_img, (block_size, int(block_size / (25 / 13)))), (x * block_size, y * block_size + int(10 / size_multiplier)))
			if line[x] == '.': screen.blit(transform.scale(yorb_img, (block_size, block_size)), (x * block_size, y * block_size))
			pygame.draw.rect(screen, (100, 100, 100), (x * block_size, y * block_size, block_size, block_size), 1)

	for y in range(2):
		for x in range(10):
			screen.blit(transform.scale(toolbar_img, (int(964 / size_multiplier), int(164 / size_multiplier)) ), ( int(18 / size_multiplier), int(898 / size_multiplier )) )
			if choosed_x == x and choosed_y == y:
				pygame.draw.rect(screen, (250, 250, 250), (x * int(100 / size_multiplier), WIN_HEIGHT - 2 * int(100 / size_multiplier) + y * int(100 / size_multiplier), int(100 / size_multiplier), int(100 / size_multiplier)), int(6 / size_multiplier))
			else:
				pygame.draw.rect(screen, (100, 100, 100), (x * int(100 / size_multiplier), WIN_HEIGHT - 2 * int(100 / size_multiplier) + y * int(100 / size_multiplier), int(100 / size_multiplier), int(100 / size_multiplier)), int(2 / size_multiplier))

	for e in event.get():
		if e.type == QUIT: pygame.quit()
		if e.type == KEYDOWN and e.key == K_RETURN:
			with open(script_dir+"editor_lvl.txt", "w+") as f:
				f.write(str(working_level))
			pygame.quit()
			import level_test
		if e.type == pygame.MOUSEMOTION:
			mouse_x, mouse_y = e.pos
		if e.type == MOUSEBUTTONDOWN and e.button == 1:
			x, y = int(mouse_x / block_size), int(mouse_y / block_size)
			if x < size_x and y < size_y:
				if not (x + 1 == size_x and ('B' in block or 'D' in block)):
					if block == 'S':
						with open(script_dir + "Levels/lvl_"+str(working_level)+".txt", "r") as f:
							file = f.readlines()
							f = open(script_dir + "Levels/lvl_"+str(working_level)+".txt", "w+")
							for i in file:
								f.write(i.replace('S', ' '))
							f.close()
					with open(script_dir + "Levels/lvl_"+str(working_level)+".txt", "r") as f:
						file = f.readlines()
					line = list(file[y])
					if line[x] != '1' and line[x] != '2' and line[x] != '3' and line[x] != '4' and line[x] != '5' and line[x] != '6' and line[x] != '7' and line[x] != '8' and line[x] != '9' and line[x+1] != 'D' and line[x+1] != 'B':
						if 'B' in block or 'D' in block:
							block = list(block)
							line[x] = block[0]
							line[x + 1] = block[1]
						elif (line[x] == 'D' or line[x] == 'B') and block == ' ':
							line[x], line[x + 1] = block, block
						else:
							line[x] = block
					file[y] = "".join(line)
					with open(script_dir + "Levels/lvl_"+str(working_level)+".txt", "w+") as f:
						for line in file:
							f.write(line)
			if mouse_x < int(1000 / size_multiplier) and mouse_y > WIN_HEIGHT - 2 * int(100 / size_multiplier):
				choosed_x, choosed_y = int(mouse_x / int(100 / size_multiplier)), int((mouse_y - WIN_HEIGHT + 2 * int(100 / size_multiplier)) / int(100 / size_multiplier))
			if choosed_x == 6:
				if mouse_x > WIN_WIDTH - int(250 / size_multiplier) - 3 * int(80 / size_multiplier) and mouse_x < WIN_WIDTH - int(250 / size_multiplier) and mouse_y > WIN_HEIGHT - 3 * int(80 / size_multiplier):
					choosed_number_x, choosed_number_y = (mouse_x - WIN_WIDTH + 3 * int(80 / size_multiplier) + int(250 / size_multiplier)) // int(80 / size_multiplier), (mouse_y - WIN_HEIGHT + 3 * int(80 / size_multiplier)) // int(80 / size_multiplier)
	screen.blit(working_level_img, working_level_img_rect)
	display.update()