import pygame # импортируем библиотеки
from pygame import *
from time import sleep
from subprocess import call
from random import randint
from settings import *

init() # инициализируем pygame

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

script_dir = __file__ # узнаём расположение скрипта
script_dir = script_dir.replace('lvl_1.py', '')

PLATFORM_WIDTH, PLATFORM_HEIGHT = 64, 64 # ставим ширину и высоту платформ

HERO_WIDTH, HERO_HEIGHT = 64, 64 # ставим ширину и высоту персонажа

all_sprites = sprite.Group() # создаём группу спрайтов

finish_trigger = sprite.Group()

orbs_list = [] # создаём список для подкидывающих шаров

shell_size = 24 # устанавливаем размер для пуль

dead = False

yorb = [image.load(script_dir+"Sprites/yorb0.png"), image.load(script_dir+"Sprites/yorb1.png")] # прогружаем картинки спрайтов
player = [image.load(script_dir+"Sprites/player.png"), image.load(script_dir+"Sprites/player_move.png")]
player_pop = image.load(script_dir+"Sprites/player_pop.png")
bullet_image = [image.load(script_dir+"Sprites/circle.png"), image.load(script_dir+"Sprites/circle_pop.png")]
enemy_image = image.load(script_dir+"Sprites/enemy.png")
brick_img = image.load(script_dir+"Sprites/bricks.png")
shotgun_img = [image.load(script_dir+"Sprites/shotgun.png"), image.load(script_dir+"Sprites/shotgun_fire.png")]
firegun_img = image.load(script_dir+"Sprites/flamethrower.png")
heart_img = image.load(script_dir+"Sprites/heart.png")
pistol_img = image.load(script_dir+"Sprites/pistol.png")
shield_img = image.load(script_dir+"Sprites/shield.png")
falling_block_img = [image.load(script_dir+"Sprites/falling_block.png"), image.load(script_dir+"Sprites/falling_block_break.png")]
finish_img = image.load(script_dir+"Sprites/finish.png")
planks_img = image.load(script_dir+"Sprites/planks.png")

# d-земля, g-трава, b-кирпичи, k-смертельный блок, 
# e-враг смотрит вправо, E-враг смотрит влево, .-подкидывающий шарик, 
# s-дробовик, f-огнемёт, p-пистолет,
# a-прозрачный блок, F-блок падающий от прикосновения,
# P-выход из уровня, w-дерево
level = [
"ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"d                                                         d",
"dgggggggggggggggggggggggggggggggggggggggggggggggggggggggggd"]

def next_level():
	with open(script_dir+"lvl.txt", "w") as f:
		f.write("2")
	sleep(1)
	pygame.quit()
	call(["python", script_dir+"lvl_2.py"])		

class Enemy_trigger(sprite.Sprite): # конструктор врагов
	def __init__(self, x, y, facing):
		sprite.Sprite.__init__(self)
		if facing: self.rect = Rect(x, y, -enemy_view, HERO_HEIGHT)
		else: self.rect = Rect(x + HERO_WIDTH, y, enemy_view, HERO_HEIGHT)
class Enemy_hitbox(sprite.Sprite):
	def __init__(self, x, y, facing):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, HERO_WIDTH, HERO_HEIGHT)
		self.trigger = Enemy_trigger(x, y, facing)
		self.Type = 'enemy'
		self.facing = facing
		self.health = 40
		self.timer = 33
		self.health_bar = Enemy_health_bar(x - 20, y - 25, self.health)
		if facing: self.image = transform.flip(transform.scale(enemy_image, (HERO_WIDTH, HERO_HEIGHT)), True, False)
		else: self.image = transform.scale(enemy_image, (HERO_WIDTH, HERO_HEIGHT))
	def update(self):
		self.health_bar.health = self.health
		self.health_bar.update()
		if self.health < 1: self.kill()
		if sprite.collide_rect(self.trigger, hero): self.timer += 1
		else: self.timer = 33
		if self.timer > 59:
			if self.facing: sh = Shell(self.trigger.rect.x + HERO_WIDTH // 2 - shell_size // 2, self.trigger.rect.y + HERO_HEIGHT // 2 - shell_size // 2, -15, 'enemy')
			else: sh = Shell(self.trigger.rect.x - HERO_WIDTH + HERO_WIDTH // 2 - shell_size // 2, self.trigger.rect.y + HERO_HEIGHT // 2 - shell_size // 2, +15, 'enemy')
			all_sprites.add(sh)
			self.timer = 0
class Enemy_health_bar(sprite.Sprite):
	def __init__(self, x, y, health):
		sprite.Sprite.__init__(self)
		self.health = health
		self.rect = Rect(x, y, 100, 15)
		self.image = [Surface((100, 15)), Surface((0, 15))]
	def update(self):
		if self.health > 0: self.image = [Surface((100, 15)), Surface((self.health * 2.5, 15))]
		else: self.image = [Surface((100, 15)), Surface((0, 15))]
		self.image[0].fill((255, 0, 0))
		self.image[1].fill((0, 255, 0))

class Platform(sprite.Sprite): # конструктор блоков
	def __init__(self, x, y, type):
		sprite.Sprite.__init__(self)
		self.type = type
		self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
		self.Type = 'platform'
		if type == "b":
			self.image = transform.scale(brick_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
		if type == "d":
			self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
			self.image.fill((105, 54, 54))
		if type == "g":
			self.image = [Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)), Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT // 4))]
			self.image[0].fill((105, 54, 54))
			self.image[1].fill((0, 176, 0))
		if type == "kb":
			self.image = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
			self.image.fill((200,0,0))
			self.rect = Rect(x, y + 1, PLATFORM_WIDTH, PLATFORM_HEIGHT - 1)
		if type == "a":
			self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
			self.image.fill((255, 150, 0))
			self.image.set_alpha(70)
		if type == "F":
			self.yvel = 0
			self.gravity = 0.90
			self.health = 2
			self.fall = False
			self.image = transform.scale(falling_block_img[0], (PLATFORM_WIDTH, PLATFORM_HEIGHT))
			self.onGround = False
			self.timer = 0
		if type == 'finish':
			self.image = transform.scale(finish_img,(PLATFORM_WIDTH, PLATFORM_HEIGHT))
		if type == 'planks':
			self.image = transform.scale(planks_img,(PLATFORM_WIDTH, PLATFORM_HEIGHT))
			self.health = 20
	def update(self):
		if not self.onGround: self.yvel += self.gravity
		self.onGround = False
		self.rect.y += self.yvel
		for e in all_sprites:
			if (e.Type == 'platform' and e != self and e.type != 'a' and sprite.collide_rect(self, e)) or (e.Type == 'enemy' and sprite.collide_rect(self, e)):
				if self.yvel > 0: self.rect.bottom, self.onGround, self.yvel = e.rect.top, True, 0
				if self.yvel < 0: self.rect.top,self.yvel = e.rect.bottom, 0
		if self.timer > 0: self.timer -= 1
		if self.timer == 0 and self.health == 0:
			self.kill()

class yOrb(sprite.Sprite): # конструктор жёлтого подкидывающего кружка
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = transform.scale(yorb[0], (42, 42))
		self.rect = Rect(x, y, 42, 42)

class weapon_trigger(sprite.Sprite): # класс триггера для оружий
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, 2, 2)

class shotgun(sprite.Sprite): # класс дробовика
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.trigger = weapon_trigger(x + PLATFORM_WIDTH // 2 - 1, y + PLATFORM_HEIGHT // 2 - 1)
		self.image = transform.scale(shotgun_img[0], (101, 45))
		self.rect = Rect(x - 6, y + 5, 101, 45)
		self.Type = 'weapon'
		self.type = 'sg'
		self.moveUp = False
		self.ammo = 5
		self.picked_up = False
		self.fire = False
	def update(self):
		if not self.picked_up:
			for pl in all_sprites:
				if pl.Type == 'platform' and not self.picked_up and sprite.collide_rect(self.trigger, pl):
					self.rect.y -= PLATFORM_HEIGHT
					self.trigger.rect.y -= PLATFORM_HEIGHT
			if sprite.collide_rect(self, hero) and hero.weapon == None and not self.picked_up:
					self.picked_up = True
					hero.weapon = 'shotgun'
		if self.picked_up:
			if self.ammo < 1:
				hero.weapon = None
				self.kill()
			if self.fire and cooldown > 10: self.fire = False
			if self.fire:
				if last_right: self.image = transform.scale(shotgun_img[1], (101, 45))
				else: self.image = transform.flip(transform.scale(shotgun_img[1], (101, 45)), True, False)
			else:
				if last_right: self.image = transform.scale(shotgun_img[0], (101, 45))
				else: self.image = transform.flip(transform.scale(shotgun_img[0], (101, 45)), True, False)
			if last_right: self.rect.x, self.rect.y = hero.rect.x + 3, hero.rect.y + 15
			else: self.rect.x, self.rect.y = hero.rect.x - 40, hero.rect.y + 15

class pistol(sprite.Sprite): # класс пистолета
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.trigger = weapon_trigger(x + PLATFORM_WIDTH // 2 - 1, y + PLATFORM_HEIGHT // 2 - 1)
		self.image = transform.scale(pistol_img, (45, 28))
		self.rect = Rect(x + 7, y + 18, 25, 15)
		self.type = 'p'
		self.Type = 'weapon'
		self.moveUp = False
		self.ammo = 12
		self.picked_up = False
	def update(self):
		if not self.picked_up:
			if sprite.collide_rect(self, hero) and hero.weapon == None:
				self.picked_up = True
				hero.weapon = 'pistol'
			for pl in all_sprites:
				if pl.Type == 'platform' and sprite.collide_rect(self.trigger, pl):
					self.rect.y -= PLATFORM_HEIGHT
					self.trigger.rect.y -= PLATFORM_HEIGHT
		else:
			if self.ammo < 1:
				hero.weapon = None
				self.kill()
			if last_right:
				self.image = transform.scale(pistol_img, (45, 28))
				self.rect.x, self.rect.y = hero.rect.x + 22, hero.rect.y + 32
			else:
				self.image = transform.flip(transform.scale(pistol_img, (45, 28)), True, False)
				self.rect.x, self.rect.y = hero.rect.x - 6, hero.rect.y + 32

class firegun(sprite.Sprite): # класс огненной пушки
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.trigger = weapon_trigger(x + PLATFORM_WIDTH // 2 - 1, y + PLATFORM_HEIGHT // 2 - 1)
		self.image = transform.scale(firegun_img, (77, 40))
		self.rect = Rect(x - 8, y + 10, 77, 40)
		self.type = 'fg'
		self.Type = 'weapon'
		self.moveUp = False
		self.ammo = 350
		self.picked_up = False
		self.shoot = 0
	def fire(self):
		if last_right: fa = flame_ammo(hero.rect.x + HERO_WIDTH // 2 - 5 // 2, hero.rect.y + HERO_HEIGHT // 2 - 3 // 2, 10)
		else: fa = flame_ammo(hero.rect.x + HERO_WIDTH // 2 - 5 // 2, hero.rect.y + HERO_HEIGHT // 2 - 3 // 2, -10)
		all_sprites.add(fa)
		self.ammo -= 1
	def update(self):
		if not self.picked_up:
			if sprite.collide_rect(self, hero) and hero.weapon == None:
				self.picked_up = True
				hero.weapon = 'firegun'
			for pl in all_sprites:
				if pl.Type == 'platform' and sprite.collide_rect(self.trigger, pl):
					self.rect.y -= PLATFORM_HEIGHT
					self.trigger.rect.y -= PLATFORM_HEIGHT
		else:
			if self.ammo < 1:
				hero.weapon = None
				self.kill()
			if last_right:
				self.image = transform.scale(firegun_img, (77, 40))
				self.rect.x, self.rect.y = hero.rect.x + 5, hero.rect.y + 25
			else: 
				self.image = transform.flip(transform.scale(firegun_img, (77, 40)), True, False)
				self.rect.x, self.rect.y = hero.rect.x - 17, hero.rect.y + 25

def level_draw(): # отрисовка карты
	pf_x=pf_y=0
	for row in level:
		for col in row:
			if col == "b": # добавление платформ на уровень
				pf = Platform(pf_x, pf_y, "b")
				all_sprites.add(pf)
			if col == "d": # добавление платформ на уровень
				pf = Platform(pf_x, pf_y, "d")
				all_sprites.add(pf)
			if col == "g": # добавление платформ на уровень
				pf = Platform(pf_x, pf_y, "g")
				all_sprites.add(pf)
			if col == "e": # добавление врагов на уровень
				enemy_hitbox = Enemy_hitbox(pf_x, pf_y, False)
				all_sprites.add(enemy_hitbox)
			if col == "E":
				enemy_hitbox = Enemy_hitbox(pf_x, pf_y, True)
				all_sprites.add(enemy_hitbox)
			if col == ".": # добавление жёлтых орбов на уровень
				orb = yOrb(pf_x + (PLATFORM_WIDTH - 42) // 2, pf_y + (PLATFORM_HEIGHT - 42) // 2)
				orbs_list.append(orb)
			if col == "k": # добавление смертельных блоков на уровень
				pf = Platform(pf_x, pf_y, "kb")
				all_sprites.add(pf)
			if col == "f": # добавление огнемётов на уровень
				fg = firegun(pf_x, pf_y)
				all_sprites.add(fg)
			if col == "s": # добавление дробовиков на уровень
				sg = shotgun(pf_x, pf_y)
				all_sprites.add(sg)
			if col == "p": # добавление пистолетов на уровень
				pist = pistol(pf_x, pf_y)
				all_sprites.add(pist)
			if col == "a": # добавление прозрачных блоков на уровень
				pf = Platform(pf_x, pf_y, "a")
				all_sprites.add(pf)
			if col == "F": # добавление падающих блоков на уровень
				pf = Platform(pf_x, pf_y, "F")
				all_sprites.add(pf)
			if col == "P": # добавление финиша на уровень
				pf = Platform(pf_x, pf_y, "finish")
				finish_trigger.add(pf)
			if col == 'w':
				pf = Platform(pf_x, pf_y, "planks")
				all_sprites.add(pf)
			pf_x += PLATFORM_WIDTH
		pf_y += PLATFORM_HEIGHT
		pf_x = 0
total_level_width,total_level_height = len(level[0])*PLATFORM_WIDTH,len(level)*PLATFORM_HEIGHT # общие ширина и высота уровня в пикселях
level_draw()

class flame_ammo(sprite.Sprite): # конструктор огненных зарядов
	def __init__(self, x, y, xvel):
		sprite.Sprite.__init__(self)
		self.yvel = randint(-3, 2)
		self.xvel = xvel
		self.image = Surface((12, 10))
		self.image.fill((230, 100, 0))
		self.rect = Rect(x, y, 12, 10)
		self.distance = 35
		self.Type = 'projectile'
	def update(self):
		self.distance -= 1
		if self.distance == 0:
			self.kill()
		self.rect.x += self.xvel
		self.rect.y += self.yvel
		for e in all_sprites:
			if e.Type == 'enemy' and sprite.collide_rect(self, e): # проверка заряда на попадение в врага
				e.health -= 1
				self.kill()
			if e.Type == 'platform':
				if e.type != 'a' and sprite.collide_rect(self, e):
					self.kill()
				if e.type == 'F' and sprite.collide_rect(self, e):
					if e.fall and e.timer < 1:
						e.image = transform.scale(falling_block_img[1], (PLATFORM_WIDTH, PLATFORM_HEIGHT))
						e.timer = 35
						e.health = 0
					if not e.fall:
						e.fall = True
						e.timer = 60
						e.health = 1
				if e.type == 'planks' and sprite.collide_rect(self, e):
					e.health -= 1

class Shell(sprite.Sprite): # конструктор пуль
	def __init__(self, x, y, xvel, type):
		sprite.Sprite.__init__(self)
		self.xvel = xvel
		self.yvel = 0
		self.image = transform.scale(bullet_image[0], (shell_size, shell_size))
		self.rect = Rect(x, y, shell_size, shell_size)
		self.timer = 0
		self.Type = 'projectile'
		self.type = type
		self.collide = False
		self.distance = 70
		self.damage = 10
		if 'player_sg_' in self.type:
			self.distance = 40
			self.damage = 15
		if 'player_sg_' in self.type:
			self.image = transform.scale(bullet_image[0],(int(shell_size / 1.5), int(shell_size / 1.5)))
			self.rect = Rect(x, y, int(shell_size / 1.5), int(shell_size / 1.5))
	def remove(self):
		self.collide = True
		self.xvel, self.yvel, self.image = 0, 0, transform.scale(bullet_image[1], (shell_size, shell_size)) # смена картинки на осколки
	def update(self):
		self.distance -= 1
		if self.distance < 1: self.kill() # проверка дистанции полёта пули
		self.rect.x += self.xvel
		if self.collide: self.timer += 1
		self.rect.y += self.yvel
		for e in all_sprites:
			if e.Type == 'platform' and e.type == 'F' and sprite.collide_rect(self, e):
					if e.fall and e.timer < 1:
						e.image = transform.scale(falling_block_img[1], (PLATFORM_WIDTH, PLATFORM_HEIGHT))
						e.timer = 35
						e.health = 0
					if not e.fall:
						e.fall = True
						e.timer = 60
						e.health = 1
			if e.Type == 'platform' and e.type != 'a' and sprite.collide_rect(self, e): self.remove() # проверка пули на попадение в стену
		if 'player' in self.type:
			for e in all_sprites:
				if e.Type == 'enemy' and sprite.collide_rect(self, e): # проверка пули на попадение в врага
					if not self.collide: e.health -= self.damage
					self.xvel, self.yvel = 0, 0
					self.remove()
					if self.timer > 20:
						self.kill()
						self.timer = 0
		if self.type == 'player_sg_0':
			self.type = 'player'
			sh_1 = Shell(hero.rect.x + HERO_WIDTH // 2 - shell_size // 2, hero.rect.y + HERO_HEIGHT // 2 - shell_size // 2, xvel, 'player_sg_1')
			sh_2 = Shell(hero.rect.x + HERO_WIDTH // 2 - shell_size // 2, hero.rect.y + HERO_HEIGHT // 2 - shell_size // 2, xvel, 'player_sg_2')
			all_sprites.add(sh_1)
			all_sprites.add(sh_2)
		if self.type == 'player_sg_1':
			self.type = 'player'
			self.yvel = 3
		if self.type == 'player_sg_2':
			self.type = 'player'
			self.yvel = -3
		if self.type == 'enemy':
			if sprite.collide_rect(self, hero) and hero.invulnerability == 0: # проверка пули на попадение в игрока
				if hero.lives < 2: hero.dead()
				else:
					if not self.collide: hero.removelive()
					self.remove()
		if self.timer > 20: self.kill()

class Player(sprite.Sprite): # класс игрока
	def __init__(self, x, y): # инициализация основных параметров
		sprite.Sprite.__init__(self)
		self.startX, self.startY = x, y
		self.xvel, self.yvel = 0, 0
		self.onGround = False
		self.jump_power, self.speed, self.gravity = 15, 10, 0.98
		self.image = transform.scale(player[0], (HERO_WIDTH, HERO_HEIGHT))
		self.rect = Rect(x, y, HERO_WIDTH, HERO_HEIGHT)
		self.weapon = None
		self.lives = 3
		self.invulnerability = 0
	def removelive(self):
		self.lives -= 1
		self.xvel, self.yvel = 0, 0
		self.invulnerability = 180
	def dead(self):
		self.image = transform.scale(player_pop, (HERO_WIDTH, HERO_HEIGHT))
		global dead
		dead = True
	def update(self, left, right, up): # обновление игрока
		global invisible
		if self.invulnerability > 0:
			if self.invulnerability%20 == 0:
				if invisible: invisible = 0
				else: invisible = 1
			self.invulnerability -= 1
		else:
			invisible = False
		if self.rect.x > total_level_width or self.rect.x < 0 or self.rect.y > total_level_height or self.rect.y < 0:
			self.dead() # при выходе за уровень убить игрока
		if up and self.onGround: self.yvel = -self.jump_power # прыгаем если есть опора
		if left:
			self.xvel = -self.speed # идём влево
			self.image = transform.flip(transform.scale(player[1], (HERO_WIDTH + 6, HERO_HEIGHT)), True, False)
		if right:
			self.xvel = self.speed # идём вправо
			self.image = transform.scale(player[1], (HERO_WIDTH + 6, HERO_HEIGHT))
		if not(left or right):
			self.xvel = 0 # никуда не идём, стоим
			self.image = transform.scale(player[0], (HERO_WIDTH, HERO_HEIGHT))
		if not self.onGround:self.yvel +=  self.gravity # падаем
		self.onGround = False
		self.rect.y += self.yvel # обновление координаты по высоте
		self.collide(0, self.yvel) # проверяем коллизию
		self.rect.x += self.xvel # обновление координаты по длине
		self.collide(self.xvel, 0)
	def collide(self, xvel, yvel):
		for f in finish_trigger:
			if sprite.collide_rect(self, f):
				next_level()
		for e in all_sprites:
			if e.Type == 'platform' and e.type == 'F' and not e.fall and sprite.collide_rect(self, e):
				e.fall = True
				e.health = 1
				e.timer = 50
			if e.Type == 'platform' and e.type == 'kb' and sprite.collide_rect(self, e) and self.invulnerability == 0:
				if self.lives > 1: self.removelive()
				else: self.dead()
		for orb in orbs_list:
			if sprite.collide_rect(self, orb): # проверка столк. с орбом
				keys = pygame.key.get_pressed()
				if keys[K_w]:
					self.yvel = -self.jump_power
		for e in all_sprites:
			if (e.Type == 'platform' and e.type != 'a' and sprite.collide_rect(self, e)) or (e.Type == 'enemy' and sprite.collide_rect(self, e)): # проверка столк. с платформ.
				if xvel > 0: self.rect.right = e.rect.left
				if xvel < 0: self.rect.left = e.rect.right
				if yvel > 0: self.rect.bottom, self.onGround, self.yvel = e.rect.top, True, 0
				if yvel < 0: self.rect.top,self.yvel = e.rect.bottom, 0

class shield(sprite.Sprite): # иконка щита
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = transform.scale(shield_img, (HERO_WIDTH, HERO_HEIGHT))
		self.rect = Rect(x, y, HERO_WIDTH, HERO_HEIGHT)

class Camera(object): # хз как работает, но это класс камеры
	def __init__(self, camera_func, width, height):
		self.camera_func, self.state = camera_func, Rect(0, 0, width, height)
	def apply(self, target):
		return target.rect.move(self.state.topleft)
	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)
def camera_configure(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2
	l = min(0, l)
	l,t = max(-(camera.width-WIN_WIDTH), l),max(-(camera.height-WIN_HEIGHT), t)
	t = min(0, t)
	return Rect(l, t, w, h)


START_X,START_Y = 72, total_level_height - PLATFORM_HEIGHT - 10 # стартовая позиция игрока
hero = Player(START_X,START_Y)

camera = Camera(camera_configure,total_level_width,total_level_height)

screen = pygame.display.set_mode(DISPLAY, DOUBLEBUF)

screen.set_alpha(None)

left,right,up = False,False,False # переменные движения игрока

clock = time.Clock()

tick = 0

last_right = True

cooldown = 0

reload_time = 60

invisible = 0

shield_icon = shield(hero.rect.x + 2, hero.rect.y - 40)

while 1:
	clock.tick(60)

	if hero.weapon == 'pistol':
		reload_time = 30
		if cooldown > reload_time: cooldown = reload_time
	else: reload_time = 60
	if cooldown < reload_time:
		cooldown += 1

	for i in event.get(): # управление игроком
		if i.type == QUIT: pygame.quit()
		if i.type == KEYDOWN and i.key == K_w: up = True
		if i.type == KEYDOWN and i.key == K_a: left, last_right = True, False
		if i.type == KEYDOWN and i.key == K_d: right, last_right = True, True
		if i.type == MOUSEBUTTONDOWN and i.button == 1:
			if cooldown > reload_time - 1:
				if last_right: xvel = 18
				else: xvel = -18
				for e in all_sprites:
					if e.Type == 'weapon' and e.type == 'sg' and e.picked_up:
						sh = Shell(hero.rect.x + HERO_WIDTH // 2 - shell_size // 2, hero.rect.y + HERO_HEIGHT // 2 - shell_size // 2, xvel, 'player_sg_0')
						all_sprites.add(sh)
						e.fire = True
						e.ammo -= 1
						cooldown = 0
					if e.Type == 'weapon' and e.type == 'p' and e.picked_up:
						sh = Shell(hero.rect.x + HERO_WIDTH // 2 - shell_size // 2, hero.rect.y + HERO_HEIGHT // 2 - shell_size // 2, xvel, 'player')
						all_sprites.add(sh)
						e.ammo -= 1
						cooldown = 0
		if i.type == KEYUP and i.key == K_w: up = False
		if i.type == KEYUP and i.key == K_a: left = False
		if i.type == KEYUP and i.key == K_d: right = False

	click = mouse.get_pressed()

	tick += 1 # счётчик текущего игрового тика
	if tick > 59:
		tick = 0

	screen.fill((255,255,255))
	camera.update(hero)
	hero.update(left, right, up)

	for orb in orbs_list:
		if not(orb.rect.x + orb.rect.width < -camera.state.x or orb.rect.x > -camera.state.x + WIN_WIDTH):
			if tick == 29: # анимация орбов
				orb.image = transform.scale(yorb[0], (42, 42))
			if tick == 59:
				orb.image = transform.scale(yorb[1], (42, 42))
			screen.blit(orb.image, camera.apply(orb))
	for e in all_sprites:
		if not(e.rect.x + e.rect.width < -camera.state.x or e.rect.x > -camera.state.x + WIN_WIDTH):
			if e.Type == 'enemy':
				screen.blit(e.health_bar.image[0], camera.apply(e.health_bar))
				screen.blit(e.health_bar.image[1], camera.apply(e.health_bar))
				screen.blit(e.image, camera.apply(e))
			if e.Type == 'platform' and e.type != 'a':
				if e.type == 'planks' and e.health < 1:
					e.kill()
				if e.type == "g":
					screen.blit(e.image[0], camera.apply(e))
					screen.blit(e.image[1], camera.apply(e))
				else: screen.blit(e.image, camera.apply(e))
			if e.Type == 'projectile':
				screen.blit(e.image, camera.apply(e))
		if (e.Type == 'platform' and e.type == 'F' and e.fall) or e.Type == 'enemy' or e.Type == 'projectile':
			e.update()
	if not invisible: screen.blit(hero.image, camera.apply(hero))

	for e in all_sprites:
		if e.Type == 'weapon':
			if not e.picked_up:
				if tick == 59:
					if e.moveUp: e.moveUp = False
					else: e.moveUp = True
				if tick%8 == 0 and e.moveUp: e.rect.y -= 1
				if tick%8 == 0 and not(e.moveUp): e.rect.y += 1
			else:
				if click[0] and e.type == 'fg':
					e.fire()
				ammo_text = font.render('Ammo: ' + str(e.ammo), 1, (255, 255, 255))
				screen.blit(ammo_text, (400, WIN_HEIGHT - 35))
			if not(e.rect.x + e.rect.width < -camera.state.x or e.rect.x > -camera.state.x + WIN_WIDTH):
				screen.blit(e.image, camera.apply(e))
				e.update()
	for f in finish_trigger:
		if not(f.rect.x + f.rect.width < -camera.state.x or f.rect.x > -camera.state.x + WIN_WIDTH):
			screen.blit(f.image, camera.apply(f))
	for e in all_sprites:
		if e.Type == 'platform' and e.type == 'a': screen.blit(e.image, camera.apply(e))
	cd_bar_text = font.render('Cooldown: ', 1, (255, 255, 255))
	if reload_time == 60:
		cd_bar_image = [Surface((120, 30)), Surface((cooldown * 2, 30))]
		cd_bar_image[1].fill((0, 255, 0))
		cd_bar_image[0].fill((255, 0, 0))
	if reload_time == 30:
		cd_bar_image = [Surface((120, 30)), Surface((cooldown * 4, 30))]
		cd_bar_image[1].fill((0, 255, 0))
		cd_bar_image[0].fill((255, 0, 0))
	for i in range(hero.lives):
		screen.blit(heart_img, (5 + 37 * i, WIN_HEIGHT - 37))
	if hero.invulnerability > 0:
		shield_icon.rect.x, shield_icon.rect.y = hero.rect.x, hero.rect.y - HERO_HEIGHT - 10
		screen.blit(shield_icon.image, camera.apply(shield_icon))

	fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (0, 255, 0))
	screen.blit(fps, (5, 5))

	if not hero.weapon == None:
		screen.blit(cd_bar_image[0], (270, WIN_HEIGHT - 35))
		screen.blit(cd_bar_image[1], (270, WIN_HEIGHT - 35))
		screen.blit(cd_bar_text, (115, WIN_HEIGHT - 35))

	display.update() # обновление экрана
	if dead:
		sc_dir = __file__
		sleep(1)
		pygame.quit()
		call(["python", sc_dir])