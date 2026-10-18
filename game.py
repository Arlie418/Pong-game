import pygame, sys, random, math

from scripts.player import Player
from scripts.ball import Ball
class Game:
	def __init__(self):
		self.width = 800
		self.height = 450
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Pong game')

		pygame.init()
		self.paddles = [
		Player(self, [30, self.height / 2 - 20], 10, 60, 4, 'left'),
		Player(self,[770, self.height / 2 - 20], 10, 60, 4, 'right')
		]

		self.score = [0, 0]

		self.movement_paddle = [False, False]

		self.ball = Ball(self, [self.width / 2, self.height / 2], 5, 2, random.uniform(0, math.pi))

		self.active_bot = pygame.USEREVENT		

		self.active = True

		self.active_deplay = 3000

		self.game_time = 0

		self.color_assets = {
		'white': (255, 255, 255),
		'gray': (80, 80, 80),
		'black': (0, 0, 0)
		}

		self.sfx = {
			'pong': pygame.mixer.Sound('data/sfx/pong.wav'),
			'hit_wall': pygame.mixer.Sound('data/sfx/hit_wall.wav'),
			'game_over': pygame.mixer.Sound('data/sfx/gameover.wav')
		}

		self.font = pygame.font.Font('data/font/Y224-2vdae.ttf', 55)



		
	def restart(self):
	
		self.paddles = [
		Player(self, [30, self.height / 2 - 20], 10, 60, 4, 'left'),
		Player(self,[770, self.height / 2 - 20], 10, 60, 4, 'right')
		]

		self.active = True

		self.game_time = 0

		if (self.score[0] < self.score[1]):
			angle = random.uniform(-math.pi / 4, math.pi / 4)
		else:
			angle = random.uniform(-3 * math.pi / 4, 3 * math.pi / 4)

		self.ball = Ball(self, [self.width / 2, self.height / 2], 5, 2, angle)

		self.max_bounce_angle = 5 * math.pi / 12

	def draw_word(self, display):
		display.blit(self.font.render(str(self.score[0]), True, self.color_assets['white']), (self.width / 2 - 150, 50))
		display.blit(self.font.render(str(self.score[1]), True, self.color_assets['white']), (self.width / 2 + 90, 50))



	def run(self):
		while True:
			self.screen.fill(self.color_assets['black'])

			self.game_time += 1
			print(self.game_time,'x 0.0003=',round(self.game_time * 0.0005,3))
			if self.ball.pos[0] > self.width or self.ball.pos[0] < 0:
				self.sfx['game_over'].play()
				if self.ball.pos[0] > self.width:
					self.score[0] += 1
				else:
					self.score[1] += 1
				self.restart()

			#border
			for i in range (25):
				rect = pygame.Rect(self.width / 2 - 5, i * 20, 10, 10)
				pygame.draw.rect(self.screen, self.color_assets['gray'], rect)


			for paddle in self.paddles:
				paddle.update((0,self.movement_paddle[1] - self.movement_paddle[0]))
				paddle.render(self.screen)
				self.ball.handle_collision(paddle)

			self.ball.update()
			self.ball.render(self.screen) 

			self.draw_word(self.screen)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					self.active = False
					pygame.time.set_timer(self.active_bot, self.active_deplay, loops = 1)
					if event.key == pygame.K_w:
						self.movement_paddle[0] = True
					if event.key == pygame.K_s:
						self.movement_paddle[1] = True
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_w:
						self.movement_paddle[0] = False
					if event.key == pygame.K_s:
						self.movement_paddle[1] = False
				if event.type == self.active_bot:
					self.active = True
			
			self.clock.tick(120)
			pygame.display.update()

Game().run()


