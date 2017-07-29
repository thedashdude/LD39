import numpy as np

class World():
    def __init__(self,EntityList,screen):
        self.entities = EntityList
        self.screen = screen

        self.collisions_array = list()

    def draw_all(self):
        for k in self.entities:
            k.draw(self.screen)

    def update(self,keystate,mousePos,mousePressed):
        #self.calculate_collisions()

        for index, entity in enumerate(self.entities):
            entity.update(keystate,mousePos,mousePressed, self.entities )

            for new_entity in entity.get_new_entities():
                self.entities.append(new_entity)

    def calculate_collisions(self):
        self.collisions_array = [


        [self.entities[collision_index]  #create list of collided entitites
        

        for collision_index in entity.rect.collidelistall(self.entities[:entity_index] + self.entities[entity_index+1:] )]  #check if an entity collides with all other entities


        for entity_index, entity in enumerate(self.entities)] #get each entity with its index


    def cont(self):
        return True