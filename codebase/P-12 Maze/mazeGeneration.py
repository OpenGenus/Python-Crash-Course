import random, pygame, time

pygame.init()

wh_maze = 980
ht_maze = 700

gameDisplay = pygame.display.set_mode((wh_maze, ht_maze))
pygame.display.set_caption("MAZE Game")

def generate_maze(height, width):
    maze = [[1 for x in range(width)] for y in range(height)]

    start_x = random.randint(0, height-1)
    
    while start_x % 2 == 0:
        start_x = random.randint(0, height-1)
    
    start_y = random.randint(1, height-1)
    while start_y % 2 == 0:
        start_y = random.randint(1, height-1)

    maze[start_x][start_y] = 0
    
    dfs(maze, height, width, start_x, start_y)

    maze[start_x][start_y] = 2

    end_x = random.randint(1, height-1)
    end_y = random.randint(1, width-1)

    while(maze[end_x][end_y]) != 0:
        end_x = random.randint(1, height-1)
        end_y = random.randint(1, width-1)    
    
    maze[end_x][end_y] = 3

    return maze

def dfs(maze, height, width, start_x, start_y):
    directions = [1, 2, 3, 4]
    random.shuffle(directions)

    for dir in directions:
        if dir == 1:
            if start_x-2 > 0 and maze[start_x - 2][start_y] != 0:
                maze[start_x-1][start_y] = 0
                maze[start_x-2][start_y] = 0
                dfs(maze, height, width, start_x - 2, start_y)

        elif dir == 2:
            if start_x + 2 < height - 1 and maze[start_x + 2][start_y] != 0:
                maze[start_x+1][start_y] = 0
                maze[start_x+2][start_y] = 0
                dfs(maze, height, width, start_x + 2, start_y)

        elif dir == 3:
            if start_y+2 < width -1 and maze[start_x][start_y + 2] != 0:
                maze[start_x][start_y + 1] = 0
                maze[start_x][start_y + 2] = 0
                dfs(maze, height, width, start_x, start_y + 2)

        elif dir == 4:
            if start_y - 2 > 0 and maze[start_x][start_y - 2] != 0:
                maze[start_x][start_y - 1] = 0
                maze[start_x][start_y - 2] = 0
                dfs(maze, height, width, start_x, start_y - 2)




def renderMaze(maze):
    x = 0
    y = 0
    for row in maze:
        for block in row:
            if block == 0:
                pygame.draw.rect(gameDisplay, (255, 200, 178), (x, y, 20, 20))

            elif block == 1:
                pygame.draw.rect(gameDisplay, (229, 152, 155) ,(x, y, 20, 20))

            elif block == 2:
                pygame.draw.rect(gameDisplay, (100, 100, 100) ,(x, y, 20, 20))
            
            elif block == 3:
                pygame.draw.rect(gameDisplay, (150, 200, 95), (x, y, 20, 20 ))

            x = x+20
        y = y+20
        x = 0
        



maze = generate_maze(35, 50)


while(True):
    renderMaze(maze)
    pygame.display.update()
    time.sleep(3)
    break
        
