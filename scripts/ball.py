import pygame, math

class Ball:
	def __init__(self, game, pos, radius, speed, angle):
		self.game = game
		self.pos = list(pos)
		self.radius = radius
		self.speed = speed	
		self.angle = angle
		self.velocity = [0, 0]
		self.max_bounce_angle = 5 * math.pi / 12
		self.extra_speed = 0

	def handle_collision(self, paddle):
		if self.rect().colliderect(paddle) :
			self.game.sfx['pong'].play()
			relative_intersect = paddle.pos[1] + (paddle.height / 2) - self.pos[1]
			normalized = relative_intersect / (paddle.height / 2)
			normalized = max(-1, min(1, normalized))
			bounce_angle = normalized * self.max_bounce_angle
			self.extra_speed = 3
			if paddle.side == 'left':
				self.pos[0] = max(paddle.rect().right + self.radius, self.pos[0])
				self.angle = bounce_angle
			else:
				self.pos[0] = min(paddle.rect().left - self.radius, self.pos[0])
				self.angle = bounce_angle - math.pi

	def update(self):
		self.velocity = [(self.speed + round(self.game.game_time * 0.0005,3) + self.extra_speed)  * math.cos(self.angle) , (self.speed + round(self.game.game_time * 0.0005,3) + self.extra_speed) * math.sin(self.angle) ]
		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]

		self.extra_speed = min(3, max(0, self.extra_speed - 0.02))

		if (self.pos[1] - self.radius) <= 0 or (self.pos[1] + self.radius) >= self.game.height:
			self.game.sfx['hit_wall'].play()
			self.angle = -self.angle

		self.pos[1] = min(self.game.height - self.radius, max(self.radius, self.pos[1])	)
	

	def rect(self):
		return pygame.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2)


	def render(self, display):
		pygame.draw.circle(display, self.game.color_assets['white'], (round(self.pos[0]), round(self.pos[1])), self.radius)
