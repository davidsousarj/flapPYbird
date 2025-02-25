#! /usr/bin/python3
import os
import pygame
from math import ceil
from random import randint

#TODO: implement background parallax
#TODO: draw better obstacles, ground, backgrounds
#TODO: main menu, high score, etc.

pygame.init()

# Screen parameters
sizex = 854
sizey = 480
tick = 30

# Color nicknames
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (100,100,255)
yellow = (255,255,0)
teal = (0,255,255)
purple = (255,0,255)
black=(0,0,0)
white = (255,255,255)
grey = (100,100,100)

# Background parameters
ground1=(88,42,10)
ground2=(42,14,3)

# Ground parameters
gsize = 10
vx = 1

# Physics parameters
g,vxx,vyy = 1,10,10 #1,10,10 #4,5,20
dt = 1

# Window / Screen 
screen = pygame.display.set_mode((sizex,sizey))
pygame.display.set_caption("A FlapPY Bird Clone by DavidSousaRJ")

# Set up asset folders
game_dir = os.path.dirname(__file__)
font_dir = os.path.join(game_dir, 'font')
sound_dir = os.path.join(game_dir, 'sound')
img_dir = os.path.join(game_dir, 'image')

# Fonts
scorefont = pygame.font.Font(os.path.join(font_dir, "Playmegames.ttf"), 64)
textfont = pygame.font.Font(os.path.join(font_dir, "Playmegames.ttf"), 32)

# Sound effects
sound_fall = pygame.mixer.Sound(os.path.join(sound_dir, 'sound-fall.wav'))
sound_score = pygame.mixer.Sound(os.path.join(sound_dir, 'sound-score.wav'))
sound_lose = pygame.mixer.Sound(os.path.join(sound_dir, 'sound-trap.wav'))
sound_flap = pygame.mixer.Sound(os.path.join(sound_dir, 'sound-wing-flap.wav'))
sound_step = pygame.mixer.Sound(os.path.join(sound_dir, 'sound-step.wav'))

# Sprites
img_bird1 = pygame.image.load(os.path.join(img_dir, 'bird1.png')).convert()
img_bird2 = pygame.image.load(os.path.join(img_dir, 'bird2.png')).convert()
img_bird3 = pygame.image.load(os.path.join(img_dir, 'bird3.png')).convert()
img_bird4 = pygame.image.load(os.path.join(img_dir, 'bird4.png')).convert()
img_bird5 = pygame.image.load(os.path.join(img_dir, 'bird5.png')).convert()

# Detect high score
hs_file = os.path.join(game_dir, '.high_score')
if os.path.isfile(hs_file):
	high_score = int.from_bytes(open(hs_file, 'rb').read())
else:
	high_score = 0

# Bird parameters
class Bird(pygame.sprite.Sprite):
	# The class Sprite has the advantage of being able to use
	# Sprite.rect.x, y, top, topright, left, center, bottom, etc.
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.width = 40
		self.height = 40

		self.image = img_bird1

		self.rect = self.image.get_rect()

		self.rect.x = 50
		self.rect.y = sizey - gsize

		self.vy = 0
		self.air = False
		self.flap = True
		self.ground = True

	def fall(self):
		#Newton Laws
		self.vy += +g*dt	
		self.rect.y  += self.vy*dt 
		self.image = img_bird1

	def walk(self):
		# Walking animation
		if self.image == img_bird3:
			self.image = img_bird4
		elif self.image == img_bird4:
			self.image = img_bird3
		else:
			self.image = img_bird3

	def check_collision(self):
		# Ground collision	
		if self.rect.y >= sizey - gsize - self.height:
			self.rect.y = sizey - gsize - self.height
			self.air = False
			if not bird.ground:
				bird.ground == True
				sound_step.play()

	def jump(self):
		bird.ground = False
		# jump (flap)
		self.vy = -vyy
		self.air = True
		# flap animation
		if self.flap == True:
			self.image = img_bird2
		else:
			self.image = img_bird1
		self.flap = not self.flap #toggle		

# Obstacle parameters
class Obstacle:
	def __init__(self):
		self.width = 40
		self.x = sizex + self.width
		self.height = 150
		self.yc = randint(self.height//2,
						  sizey - gsize - self.height//2)
		self.y1 = self.yc - self.height//2
		self.y2 = self.yc + self.height//2

	def move(self):
		self.x -= vx*vxx

	def draw(self):
		pygame.draw.rect(screen, purple, (self.x, 0,
										  self.width, self.y1))
		pygame.draw.rect(screen, purple, (self.x, self.y2, 
										  self.width,
										  sizey - gsize - self.y2))

	def detect_restart(self):
		if self.x <= -self.width:
			self.x = space*4
			self.yc = randint(self.height//2,
							  sizey - gsize - self.height//2)
			self.y1 = self.yc - self.height//2
			self.y2 = self.yc + self.height//2

def get_x(Obstacle):
	# Depends on bird.x = 50 and probably on Obstacle.width and vx
	if Obstacle.x < 40: # but... works!
		return 1000
	else:
		return Obstacle.x

def game_over(score, high_score):
	global white, all_sprites, scorefont, textfont, screen, hs_file

	if high_score == 0 or score > high_score:
		high_score = score

	with open(hs_file, 'wb') as f:
		f.write(high_score.to_bytes(8))

	all_sprites.update()
	all_sprites.draw(screen)

	gameover = scorefont.render("GAME OVER", 1, white)
	score = textfont.render(f"SCORE: {score}", 1, white)
	highscore = textfont.render(f"HIGH SCORE: {high_score}", 1, white)
	presskey  = textfont.render("Press Enter to quit game", 1, white)

	screen.blit(gameover, (270, 200))
	screen.blit(score, (350, 250))
	screen.blit(highscore, (350, 300))
	screen.blit(presskey, (220, 350))
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RETURN] or event.type == pygame.QUIT:
				pygame.quit()

########################################################################
# Sprite and Screen Elements Initialization
bird = Bird()

o1=Obstacle()
o2=Obstacle()
o3=Obstacle()
o4=Obstacle()
space = 325
o2.x += space
o3.x += space*2
o4.x += space*3

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_sprites.add(bird)

score = 0
step = 0
run = True

# Main Loop
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	# Move Bird
	if bird.air:
		bird.fall()
	else:
		bird.walk()
	bird.check_collision()

	# Detect Pressed Keys
	keys = pygame.key.get_pressed()
	if keys[pygame.K_SPACE]:
		sound_flap.play()
		bird.jump()
	
	if keys[pygame.K_F10]: # shortcut to gameover
		game_over(score, high_score)

	# Draw Background		
	screen.fill(cyan)

	# Draw obstacles
	for o in (o1,o2,o3,o4):
		o.move()
		o.draw()
		o.detect_restart()

	# Draw ground
	for i in range(ceil( sizex / gsize / 2.0)+1):
		pygame.draw.rect(screen, ground1, (2*i*gsize - step*vx,
										   sizey - gsize, gsize, gsize))
		pygame.draw.rect(screen, ground2, ((2*i+1)*gsize - step*vx,
										   sizey - gsize, gsize, gsize))
	step +=1	
	if step == 2*gsize: step = 0

	# Detect next obstacle
	next_o = min(o1, o2, o3, o4, key=get_x)

 	# Detect bird collision
	if ( bird.rect.x < next_o.x + next_o.width and\
		 bird.rect.x + bird.width > next_o.x   and\
		 bird.rect.y < 0 + next_o.y1           and\
		 bird.rect.y + bird.height > 0         ) or\
	   ( bird.rect.x < next_o.x + next_o.width and\
		 bird.rect.x + bird.width > next_o.x   and\
		 bird.rect.y < next_o.y2 + sizey - gsize and\
		 bird.rect.y + bird.height > next_o.y2 ):
		sound_lose.play()
		bird.image = img_bird5
		bird.image.set_colorkey(red)
		game_over(score, high_score)

	# Detect score
	if next_o.x < bird.rect.x:
		score += 1
		sound_score.play()
	label = scorefont.render(f"{score}", 1, white)
	screen.blit(label, (sizex//2, 10))

	bird.image.set_colorkey(red)
	all_sprites.update()
	all_sprites.draw(screen)

	pygame.display.update()
	clock.tick(tick)

pygame.quit()
