import pygame
import os
class Unit(pygame.sprite.Sprite):
    def __init__(self, type, x, y, width, height):
        self.type = type
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", type+'.png')), (32, 32))
        self.mask = pygame.mask.from_surface(self.image)
        self.hunted = 0
    
    def up(self):
        self.rect.y -= 2
        
    def down(self):
        self.rect.y += 2
    
    def right(self):
        self.rect.x += 2

    def left(self):
        self.rect.x -= 2

    def draw(self, WN, score_label):
        WN.blit(score_label, (self.rect.x, self.rect.y-15))

        WN.blit(self.image ,(self.rect.x, self.rect.y))

    def near_unit(self,units):
        distances = []
        near_objects = []
        for i in units:
            
            distance = ((self.rect.x - i.rect.x)**2 + (self.rect.y-i.rect.y)**2)**0.5
            distances.append(distance)
            near_objects.append(i)
        return near_objects[distances.index(min(distances))] ,min(distances)
