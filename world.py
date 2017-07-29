import numpy as np

class World():
    def __init__(self,EntityList, tb, screen):
        self.entities = EntityList
        self.text = tb
        self.screen = screen
        self.paused = False
        self.collisions_array = list()

    def draw_all(self):
        for k in self.entities:
            k.draw(self.screen)

    def update(self,keystate,mousePos,mousePressed):
        #self.calculate_collisions()
        if not self.paused:
            for index, entity in enumerate(self.entities):
                entity.update(keystate,mousePos,mousePressed, self.entities )

                for new_entity in entity.get_new_entities():
                    self.entities.append(new_entity)
        else:
            self.text.update(mousePressed)

    def cont(self):
        return True