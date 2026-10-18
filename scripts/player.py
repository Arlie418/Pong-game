import pygame, math

class Player:
	def __init__(self, game, pos, width, height, speed, side):
		self.game = game
		self.pos = list(pos)
		self.width = width
		self.height = height
		self.speed = speed
		self.side = side
		self.creaction_time = 0.6
		self.distance_reaction = self.game.width / 2

	def update(self, movement = (0, 0)):
		if self.side == 'left':	
			self.pos[1] += movement[1] * self.speed
		
		if (self.game.active):
			if self.side == 'left':
				if (self.game.ball.pos[0] <  self.distance_reaction and self.game.ball.velocity[0] < 0):
					distance_to_ball = self.game.ball.pos[1] - (self.pos[1] + self.height / 2)
					target = distance_to_ball + self.game.ball.velocity[1]  * self.creaction_time
					if abs(target) > self.speed + 5:
						self.pos[1] += max(-self.speed,min(self.speed, target))

		if self.side == 'right':
			if (self.game.ball.pos[0] >=  self.distance_reaction and self.game.ball.velocity[0] >= 0):
				distance_to_ball = self.game.ball.pos[1] - (self.pos[1] + self.height / 2) 
				target = distance_to_ball + self.game.ball.velocity[1]  * self.creaction_time
				if abs(target) > self.speed + 5:
					self.pos[1] += max(-self.speed, min(self.speed,target))
		
		self.pos[1] = min(self.game.height - self.height, max(0, self.pos[1]))	


	def rect(self):
		return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

	def render(self, display):
		pygame.draw.rect(display, self.game.color_assets['white'], self.rect())

