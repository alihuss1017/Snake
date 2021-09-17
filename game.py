import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)


class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4


Point = namedtuple('Point', 'x,y')

white = (255, 255, 255)
red = (200, 0, 0)
blue1 = (0, 0, 255)
blue2 = (0, 100, 255)
black = (0, 0, 0)

blockSize = 20
speed = 15


class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.direction = Direction.right

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - blockSize, self.head.y), Point(self.head.x - (2 * blockSize), self.head.y)]

        self.score = 0
        self.food = None
        self.placeFood()

    def placeFood(self):
        x = random.randint(0, (self.w - blockSize) // blockSize) * blockSize
        y = random.randint(0, (self.h - blockSize) // blockSize) * blockSize
        self.food = Point(x,y)
        if self.food in self.snake:
            self.placeFood()

    def playStep(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.left
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.right
                elif event.key == pygame.K_UP:
                    self.direction = Direction.up
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.down

        self.move(self.direction)
        self.snake.insert(0, self.head)


        gameOver = False
        if self.isCollision():
            gameOver = True

            return gameOver, self.score

        if self.head == self.food:
            self.score += 1
            self.placeFood()
        else:
            self.snake.pop()

        self.updateUI()
        self.clock.tick(speed)
        return gameOver, self.score

    def isCollision(self):
        if self.head.x > self.w - blockSize or self.head.x < 0 or self.head.y > self.h - blockSize or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def updateUI(self):
        self.display.fill(black)

        for pt in self.snake:
            pygame.draw.rect(self.display, blue1, pygame.Rect(pt.x, pt.y, blockSize, blockSize))
            pygame.draw.rect(self.display, blue2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, red, pygame.Rect(self.food.x, self.food.y, blockSize, blockSize))

        text = font.render("Score: " + str(self.score), True, white)
        self.display.blit(text, [0,0])
        pygame.display.flip()


    def move(self, direction):
        x=self.head.x
        y=self.head.y

        if direction == Direction.right:
            x+=blockSize
        elif direction == Direction.left:
            x-= blockSize
        elif direction == Direction.down:
            y+= blockSize
        elif direction == Direction.up:
            y-= blockSize

        self.head = Point(x,y)


if __name__ == '__main__':
    game = SnakeGame()
    while True:
        gameOver, score = game.playStep()

        if gameOver:
            break
    print('Final Score', score)

    pygame.quit()
