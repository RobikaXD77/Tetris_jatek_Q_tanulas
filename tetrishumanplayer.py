import pygame
import random
import tetrishumanplayer
import pygame
import numpy as np
import time

colors = [
    (0, 0, 0),
    (0, 128, 255)
]

# Tetrominos
class Figure:
    x = 0
    y = 0

    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]],
        [[0, 1, 5, 6], [2, 6, 5, 9]],
        [[2, 3, 6, 5], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]]
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
        self.conversion = np.zeros((20,10))

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])



class Tetris:
    level = 1
    score = 0
    state = "start"
    field = []
    height = 20
    width = 10
    x = 100
    y = 60
    zoom = 20

    def __init__(self):
        pygame.init()
        height = 20
        width = 10
        self.height = 20
        self.width = 10
        self.field = np.zeros((20,10), dtype=np.int32)
        self.score = 0
        self.reward = 0
        self.lose = False
        self.done = False
        self.figure = Figure(3,0)
        self.state = "start"
        self.screen = pygame.display.set_mode((400, 500))
        self.holes = 0
        self.height_counter = 20
        self.bumpiness = 0
        self.counter = 0
        self.fps = 25
        self.clock = pygame.time.Clock()
    
            
    def new_figure(self):
        self.figure = Figure(3,0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
        self.reward += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            self.lose = True
            self.reward -= 10
        self.score += 1
        self.reward += 1

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
           self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
           self.figure.rotation = old_rotation

    
    def auto_go_down(self):
        counter = 0
        doit = True

        while doit == True:
            counter +=1

            if counter == 10000:
                self.go_down()
                counter = 0
                
    
    # Render ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def render(self):
        
            pygame.display.set_caption("Tetris")


            self.counter += 1
            if self.counter == 100000:
               self.counter = 0

            if self.counter % (self.fps // self.level // 2) == 0:
                if self.state == "start":
                    self.go_down()
        
            self.screen.fill((255, 255, 255))

            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(self.screen,(128, 128, 128), [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom], 1)
                    if self.field[i][j] > 0:
                        pygame.draw.rect(self.screen, colors[self.field[i][j]],
                                            [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2, self.zoom - 1])

            if self.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in self.figure.image():
                            pygame.draw.rect(self.screen, colors[self.figure.color],
                                                [self.x + self.zoom * (j + self.figure.x) + 1,
                                                self.y + self.zoom * (i + self.figure.y) + 1,
                                                self.zoom - 2, self.zoom - 2])

            font = pygame.font.SysFont('Calibri', 25, True, False)
            font1 = pygame.font.SysFont('Calibri', 65, True, False)
            text = font.render("Score: " + str(self.score), True, (0, 0, 0))
            text_game_over = font1.render("Game Over", True, (255, 125, 0))

            self.screen.blit(text, [0, 0])
            if self.state == "gameover":
                self.done = True
                self.screen.blit(text_game_over, [20, 200])
        
            pygame.display.flip()
            self.clock.tick(self.fps)

    # Play the game yourself----------------------------------------------------------------------------------------------------------------------------------
    def player_input(self):
            for event in list(pygame.event.get()):
                        if event.type == pygame.QUIT:
                            done = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.rotate()
                            if event.key == pygame.K_DOWN:
                                self.go_down()
                            if event.key == pygame.K_LEFT:
                                self.go_side(-1)
                            if event.key == pygame.K_RIGHT:
                                self.go_side(1)
                            if event.key == pygame.K_SPACE:
                                self.go_space()
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()

    def playergame(self):  
        while not self.done:
            self.render()
            self.player_input()

game = Tetris()
game.playergame()

