import pygame
import numpy as np
from Entities import *

def file_to_array(file_path):
	"""
	Returns a file's contents as a string array. 
	"""
	lines = []
	with open(file_path, "r") as f:
		lines = f.readlines()
	lines = [x.strip() for x in lines] 
	return lines

def string_array_to_entity_array(str_arr, size=32):
	"""
	Returns the array of entities that are in the string array. 
	Currently does not have specific entities. Only entity classes. 

	Params:
		str_arr[list of strings]:
			This is the string array that will be read and checked for entities.
		size [int]:
			This is the size of each entity. 

	Returns:
		ent_arr[list of entities]:
			This is the list of the entities on the map. 

	Key Code:
	P = Player
	B = Blank
	- = Horizontal wall
	| = Vertical wall
	E = Enemy

	"""
	ent_arr = []
	for i in range(len(str_arr)):
		for j in range(len(str_arr[i])):
			a = str_arr[i][j]
			if a == "P":
				ent_arr.append(Player(x=i*size, y=j*size))
			elif a == "-":
				ent_arr.append(Wall(x=i*size, y=j*size))
			elif a == "|":
				ent_arr.append(Wall(x=i*size, y=j*size))
			elif a != "B":
				ent_arr.append(Entity(x=i*size, y=j*size))


	return ent_arr

def dialogue_to_text_box(dialogue):
	"""
	This returns a TextBox object which has the specified dialogue in it. 

	Params:
		dialogue[str]:
			The dialogue that you want to make into a text box.

	Returns:
		tb [TextBox]:
			The text box object with the dialogue in it. 

	"""
	return TextBox(dialogue)