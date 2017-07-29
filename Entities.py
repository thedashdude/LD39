#import basic pygame modules
import pygame
from pygame.locals import *

class Entity():
	def __init__(self, x=0, y=0, length = 32, width = 32):
		self.rect = Rect(x,y,length,width)

		self.new_entities = []
		

	def update(self, keystate, mouse_position, mouse_press, collided_entites):
		pass

	def get_new_entities(self):
		x = self.new_entities
		self.new_entities = []
		return x

	def get_collision_box(self):
		return self.rect

	def draw(self, screen):
		pass

class Test(Entity):
	def __init__(self,x=0,y=0):
		super().__init__(x,y)
	def update(self, keystate, mouse_position, mouse_press, collided_entites):
		self.rect.top = self.rect.top + 1
		if keystate[K_UP]:
			self.rect.top = self.rect.top - 2
	def draw(self, screen):
		pygame.draw.rect(screen, (200,200,200), self.rect)
