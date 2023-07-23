import pygame
import time


pygame.init()

width = 900
height = 650

dark = (109, 104, 117)

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("MAZE Game")


maze=[[1,3,1,0,1,0,1,0,0,0,0,1,1,0,0],
[1,0,1,0,1,0,1,0,1,0,0,1,0,0,0],
[1,0,0,0,1,0,0,0,1,0,0,0,0,1,0],
[1,0,1,0,1,1,0,1,1,1,1,1,0,1,0],
[1,0,1,0,1,0,0,1,0,0,1,0,0,1,0],
[1,1,1,0,1,0,0,0,0,0,1,0,0,1,0],
[1,0,0,0,1,0,0,0,1,0,1,1,1,0,0],
[1,0,1,1,1,1,1,1,1,0,1,0,0,0,0],
[1,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
[1,0,0,0,0,1,1,0,1,1,1,1,1,1,0],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,2],]


def renderMaze(maze):
    x = 0
    y = 0
    for row in maze:
        for block in row:
            if block == 0:
                pygame.draw.rect(gameDisplay, (255, 205, 178), (x, y, 60, 60))
    
            elif block == 1:
                pygame.draw.rect(gameDisplay, (229, 152, 155) ,(x, y, 60, 60))

            elif block == 2:
                pygame.draw.rect(gameDisplay, (255, 183, 0), (x, y, 60, 60))
            elif block == 3:
                pygame.draw.rect(gameDisplay, (120, 150, 100), (x, y, 60, 60))
        
            x = x+60
        y = y+60
        x = 0


def displayText(text):
    renderFont = pygame.font.Font('freesansbold.ttf', 45)

    textsc = renderFont.render(text, True, dark)

    surface, rect = textsc, textsc.get_rect()


    rect.center = ((width/2),(height/2))

    gameDisplay.blit(surface, rect)

    pygame.display.update()

    time.sleep(1) 



x = 1
y = 0
dest = 0
gameDisplay.fill((150,150,255))
while True:
    renderMaze(maze)
    
    
    if dest == 1:
        displayText("Yay! Destination reached!")
        exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                block = maze[y][x-1]
                if block == 0:
                    maze[y][x- 1]= 2
                    maze[y][x] = 0
                    x = x -1

                elif block == 2:
                    maze[y][x-1] = 3
                    maze[y][x] = 0
                    x = x-1                    
                    dest =1

            if event.key == pygame.K_RIGHT:
                block = maze[y][x+1]
                if block == 0:
                    maze[y][x + 1] =2
                    maze[y][x]=0
                    x = x+ 1
                elif block == 2:
                    maze[y][x+1] = 3
                    maze[y][x] = 0
                    x = x + 1
                    dest = 1


            if event.key == pygame.K_UP:
                block = maze[y- 1][x]
                if block == 0:
                    maze[y -1][x]= 2
                    maze[y][x]= 0
                    y =y -1
                elif block == 2:
                    maze[y -1][x] = 3
                    maze[y][x] = 0
                    y = y- 1
                    dest=1
                    
            if event.key == pygame.K_DOWN:
                block=maze[y +1][x]
                if block == 0:
                    maze[y+ 1][x]=2
                    maze[y][x]=0
                    y = y + 1
                elif block == 2:
                    maze[y+1][x] = 3
                    maze[y][x] = 0
                    y = y+ 1
                    dest = 1
                    
        
    pygame.display.update()



