import pygame
from sys import exit
from random import randint, choice

def display_score():
	current_time = round((pygame.time.get_ticks() - start_time)/1000)
	score_surf = font.render(f'{current_time}', False, 'Black')
	score_rect = score_surf.get_rect(center = (400, 50))
	screen.blit(score_surf, score_rect)
	return current_time

def collisions_sprites():
	if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
		obstacle_group.empty()
		return False
	return True

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
		player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk1, player_walk2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80, 300))
		self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('sounds/music.wav')
		self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
		self.jump_sound.set_volume(0.1)
	
	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()
	
	def animation_state(self):
		if self.rect.bottom < 300:
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk): self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300: self.rect.bottom = 300
	
	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()
		
		if type == 'fly':
			fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
			fly2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
			self.frames = [fly1, fly2]
			y_pos = 210
		else:
			snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail1, snail2]
			y_pos = 300
		
		self.animation_index = 0		
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

	def animation_state(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]
	
	def destroy(self):
		if self.rect.x < -100: self.kill()
	
	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

if __name__ == '__main__':

	pygame.init()

	start_time = 0
	score = 0
	ground_level = 300
	screen_width = 800
	screen_heigth = 400
	font_size = 50
	game_active = False
	v3MenuText = (111,196,169)
	v3MenuBackgroundColor = (94, 129, 162)
	
	bg_Sound = pygame.mixer.Sound('sounds/music.wav')
	bg_Sound.set_volume(0.1)
	bg_Sound.play(loops= -1)

	pygame.display.set_caption("Mr. Poop Adventure")
	
	screen = pygame.display.set_mode((screen_width, screen_heigth))
	clock = pygame.time.Clock()
	font = pygame.font.Font('font/Pixeltype.ttf', font_size)

	sky_surface = pygame.image.load('graphics/Sky.png').convert()
	ground_surface = pygame.image.load('graphics/ground.png').convert()

	player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
	player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
	player_stand_rect = player_stand.get_rect(center = (400, 200))
	
	# Groups
	player = pygame.sprite.GroupSingle()
	obstacle_group = pygame.sprite.Group()

	player.add(Player())

	# Intro
	game_name = font.render('Pixel runner', False, v3MenuText)
	game_name_rect = game_name.get_rect(center = (400, 80))
	game_message = font.render('Press space to run', False, v3MenuText)
	game_message_rect = game_message.get_rect(center = (400, 320))

	# Timer
	obstacle_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(obstacle_timer, 1400)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			
			if not game_active:	
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
						game_active = True
						start_time = pygame.time.get_ticks()
			
			if game_active:
				if event.type == obstacle_timer:
					obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
				

		if game_active:
			# sky and ground
			screen.blit(sky_surface, (0, 0))
			screen.blit(ground_surface, (0, ground_level))
			
			# score
			score = display_score()

			# draw player
			player.draw(screen)
			player.update()

			# draw obstacles
			obstacle_group.draw(screen)
			obstacle_group.update()

			# Collision
			game_active = collisions_sprites()
		else:
			screen.fill(v3MenuBackgroundColor)
			screen.blit(player_stand, player_stand_rect)
			
			score_message = font.render(f'Your score: {score}', False, v3MenuText)
			score_message_rect = score_message.get_rect(center = (400, 330))

			screen.blit(game_name, game_name_rect)
			if score == 0:
				screen.blit(game_message, game_message_rect)
			else:
				screen.blit(score_message, score_message_rect)

		pygame.display.update()
		clock.tick(60)