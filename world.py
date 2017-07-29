import numpy as np

class World():
    def __init__(self,EntityList,screen):
        self.entities = EntityList
        self.screen = screen
    def draw_all(self):
        for k in self.entities:
            k.draw(self.screen)

    def update(self,keystate,mousePos,mousePressed):
        boxes = []
        ents = []
        for k in self.entities:
            k.update(keystate,mousePos,mousePressed)
            box.append(k.rect)
            ents.append(k)
        ents = np.array(ents)
        for k in self.entities:
            k.collide( ents[k.rect.collidelistall(boxes)] )
            for entity in k.get_new_entities():
                self.entities.append(entity)
    def cont(self):
        return True