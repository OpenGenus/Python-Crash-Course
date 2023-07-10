import pygame
import os
import random


from dinosaur import Dinosaur
from cloud import Cloud 
# from obstacle import Obstacle,SmallCactus,LargeCactus,Bird

#initializing pygame
pygame.init()

#constants
SCREEN_WIDTH=1000
SCREEN_HEIGHT=600
SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))




#load images

SMALL_CACTUS=[pygame.image.load(os.path.join('./Assets/Cactus','SmallCactus1.png')), pygame.image.load(os.path.join('./Assets/Cactus','SmallCactus2.png')), pygame.image.load(os.path.join('./Assets/Cactus','SmallCactus3.png')) ]

LARGE_CACTUS=[pygame.image.load(os.path.join('./Assets/Cactus','LargeCactus1.png')), pygame.image.load(os.path.join('./Assets/Cactus','LargeCactus2.png')), pygame.image.load(os.path.join('./Assets/Cactus','LargeCactus3.png')) ]

BIRD=[pygame.image.load(os.path.join('./Assets/Bird','Bird1.png')), pygame.image.load(os.path.join('./Assets/Bird','Bird2.png')) ]



BG=pygame.image.load(os.path.join('./Assets/Other','Track.png'))



class Obstacle:

    def __init__(self,image,type):
        self.image=image
        self.type=type 
        self.rect=self.image[self.type].get_rect()
        self.rect.x=SCREEN_WIDTH 
    def update(self):
        self.rect.x -= gamespeed 
        if(self.rect.x<= - SCREEN_WIDTH):
            self.rect.x= SCREEN_WIDTH
            obstacles.pop()

    def draw(self,SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)



class SmallCactus(Obstacle):
    def __init__(self,image):
        self.image=image 
        self.type=random.randint(0,2)
        super().__init__(self.image,self.type)
        self.rect.y=400

class LargeCactus(Obstacle):
    def __init__(self,image):
        self.image=image 
        self.type=random.randint(0,2)
        super().__init__(self.image,self.type)
        self.rect.y=340

class Bird(Obstacle):
    def __init__(self,image):
        self.image=image 
        self.index=0 
        self.type=0 
        super().__init__(self.image,self.type)
        self.rect.y=random.randint(290,310)
    def draw( self, screen):
        if(self.index>=9):
            self.index=0
        screen.blit( self.image[self.index //5], self.rect)
        self.index+=1




def game_main():

    global gamespeed, x_pos, y_pos, points,obstacles,death_count
    gamespeed=12
    x_pos=0
    y_pos=400
    points=0
    font= pygame.font.SysFont('arial',20)
    obstacles=[]
    death_count=0
  

    def score():
        global points,gamespeed
        points+=1

        if points%100 == 0:
            gamespeed+=1

        text=font.render("Points: "+ str(points), True, (0,0,0))

        text_rect=text.get_rect()
        text_rect.center=(800,90)

        SCREEN.blit( text, text_rect )

    def track():
       global x_pos, y_pos
       image_width=BG.get_width()
       SCREEN.blit(BG, (x_pos, y_pos))
       SCREEN.blit(BG,(image_width+x_pos, y_pos))

       if x_pos<= - image_width:
           
           SCREEN.blit(BG, (image_width+x_pos, y_pos))
           x_pos=0
       
       x_pos -= gamespeed
     
    
    clock=pygame.time.Clock()
    dinosaur=Dinosaur()
    cloud=Cloud(gamespeed,SCREEN_WIDTH)
    

    
    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()

        SCREEN.fill((255,255,255))
        userIn=pygame.key.get_pressed()
        
        dinosaur.draw(SCREEN)
        dinosaur.update(userIn)  

        score()
        track()

        if len(obstacles)==0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0,2) == 1: 
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if dinosaur.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                death_count+=1
                menu(death_count)

        cloud.draw(SCREEN)
        cloud.update()

        clock.tick(30)
       
        pygame.display.update()


def menu(death_count):

    global points

    while True:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.SysFont('aria', 30)

        if death_count == 0:
            text= font.render(' Press any key to start', True, (0,0,0))
        elif death_count>0:
            text= font.render(' Press any key to restart', True, (0,0,0) )
            score= font.render(' Your score: ' + str(points), True, (0,0,0))
            score_rect=score.get_rect()
            score_rect.center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
            SCREEN.blit(score, score_rect)
        text_rect= text.get_rect()
        text_rect.center= (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        SCREEN.blit(text,text_rect)

        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                game_main()

menu(death_count=0)
