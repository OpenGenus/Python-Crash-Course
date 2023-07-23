import pygame

from utils import Position


class Snake:
    def __init__(self, position: Position, size: int = 10):
        self.__position = Position(position.x, position.y)

        self.__size = size
        self.__body_color: pygame.Color = pygame.Color("green")
        self.__body = [[position.x, position.y], [position.x - size, 50], [position.x - 2 * size, 50],
                     [position.x - 3 * size, 50]]

    def get_position(self):
        return self.__position

    def move(self, dx: int, dy: int) -> None:
        self.__position.x += dx
        self.__position.y += dy
        self.__body.insert(0, [self.__position.x, self.__position.y])
        self.__body.pop()

    def grow(self) -> None:
        self.__body.insert(0, [self.__position.x, self.__position.y])

    def draw(self, surface: pygame.Surface) -> None:
        for block in self.__body:
            block_rect = pygame.Rect(block[0], block[1], self.__size, self.__size)
            pygame.draw.rect(surface, self.__body_color, block_rect)

    def has_eaten_itself(self):
        for i in range(1, len(self.__body)):
            block = self.__body[i]
            if block[0] == self.__position.x and block[1] == self.__position.y:
                return True
        return False


class Fruit:
    def __init__(self, position: Position, size: int = 10):
        self.__position = position
        self.__size = size
        self.__color = pygame.Color("red")
        self.__fruit = pygame.Rect(self.__position.x, self.__position.y, self.__size, self.__size)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.__color, self.__fruit)

    def move(self, dx: int, dy: int) -> None:
        self.__position.x += dx
        self.__position.y += dy
        self.__fruit.move_ip(self.__position.x, self.__position.y)

    def get_position(self) -> Position:
        return self.__position
