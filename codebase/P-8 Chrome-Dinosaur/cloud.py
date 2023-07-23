import pygame 
import os
import random 

CLOUDS=pygame.image.load(os.path.join('./Assets/Other','Cloud.png'))

class Cloud:

    def __init__(self,gamespeed,screen_width) :
        self.gamespeed=gamespeed 
        self.image= CLOUDS       
        self.rect = self.image.get_rect()
        self.screen_width=screen_width 
        self.x=self.screen_width+random.randint(300,1000)
        self.y=random.randint(150,250)
        
    
    def update(self):
        
        self.x-=self.gamespeed
        if(self.x < self.rect.x):
             self.x=self.screen_width+random.randint(300,1000)
             self.y=random.randint(150,250)
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
