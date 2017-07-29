#import basic pygame modules
import pygame
from pygame.locals import *

class Entity():
	def __init__(self,current_world, x=0, y=0):
		self.x = 0
		self.y = 0
		self.current_world = current_world

	def move(self,x,y):
		self.x += x
		self.y += y
		self.rect = Rect(self.x,self.y,32,32)

	def update(self, current_input):
		pass


	def get_collision_box(self,vcollision_object):
		pass

	def draw(self, screen):
		pass


class Shape():
	def __init__():
