import pygame
import numpy as np
import random
from gym import Env
from gym.spaces import Discrete, Box
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

    def figarray(self):
        self.matrix = self.figures[self.type][self.rotation]
        # []
        if self.matrix == [1,2,5,6]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y), (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y), (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
        # I
        if self.matrix == [4,5,6,7]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 1, (self.x) + 0] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 3] = 1
        if self.matrix == [1, 5, 9, 13]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
           self.conversion[(self.y) + 3, (self.x) + 1] = 1
        # Z
        if self.matrix == [0, 1, 5, 6]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 0] = 1
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
        if self.matrix == [2, 6, 5, 9]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
        # rZ
        if self.matrix == [2, 3, 6, 5]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 2] = 1
           self.conversion[(self.y) + 0, (self.x) + 3] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
        if self.matrix == [1, 5, 6, 10]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 2, (self.x) + 2] = 1
        # L
        if self.matrix == [1, 2, 6, 10]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 0, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 2, (self.x) + 2] = 1
        if self.matrix == [5, 6, 7, 9]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 3] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
        if self.matrix == [2, 6, 10, 11]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 2, (self.x) + 2] = 1
           self.conversion[(self.y) + 2, (self.x) + 3] = 1
        if self.matrix == [3, 5, 6, 7]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 3] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 3] = 1
        # rL
        if self.matrix == [1, 2, 5, 9]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 0, (self.x) + 2] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
        if self.matrix == [0, 4, 5, 6]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 0] = 1
           self.conversion[(self.y) + 1, (self.x) + 0] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
        if self.matrix == [1, 5, 9, 8]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
           self.conversion[(self.y) + 2, (self.x) + 0] = 1
        if self.matrix == [4, 5, 6, 10]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 1, (self.x) + 0] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 2, (self.x) + 2] = 1
        # T
        if self.matrix == [1, 4, 5, 6]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 0] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
        if self.matrix == [1, 4, 5, 9]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 0] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
        if self.matrix == [4, 5, 6, 9]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 1, (self.x) + 0] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
        if self.matrix == [1, 5, 6, 9]:
           self.conversion = np.zeros((20,10))
           self.conversion[(self.y) + 0, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 1] = 1
           self.conversion[(self.y) + 1, (self.x) + 2] = 1
           self.conversion[(self.y) + 2, (self.x) + 1] = 1
        

        return self.conversion

class TetrisEnv(Env):

    level = 1
    score = 0
    x = 100
    y = 60
    zoom = 20
#------------------------------------------------------------------------------------ #Tetris __Init__ #------------------------------------------------------------------------------------

    def __init__(self):
            self.game = "start"
            self.height = 20
            self.width = 10
            self.field = np.zeros((20,10), dtype = np.int32)
            self.figure = Figure(3,0)
            self.score = 0
            self.reward = 0
            self.done = False
            self.counter = 0
            self.holes = 0
            self.height_counter = 20
            self.bumpiness = 0
            # Actions we can take: rotate, go_left, go_right, drop
            self.action_space = Discrete(40)
            # Board Array info
            self.observation_space = Box (low = np.zeros((20,10)), high = np.ones((20,10)), dtype = np.int32)
            # Set starting space
            self.state = np.reshape((self.field) + (self.figure.figarray()),200,)
            



# ------------------------------------------------------------------------------------- # Defining the game #-----------------------------------------------------------------------------

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
        self.reward += (2*lines) ** 2
        #self.reward += lines

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
            self.game = "gameover"
            self.done = True
            #self.reward -= 5
        self.reward += (2 - (0.51 * self._height()) - (0.36 * self._holes()) - (0.18 * self._bumpiness()))

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

    def _height(self):
        max_height = 20
        last_height = self.height_counter
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] == 1 and max_height > i:
                    max_height = i
                                
                else:
                    continue
        heightdiff = last_height - max_height
        self.height_counter = max_height

        return(heightdiff)
        

    def _holes(self):
        holes = 0
        tophole = False
        for i in range(self.width):
            for j in range(self.height):
                if self.field[j][i] == 1:
                    tophole = True
                if tophole == True and self.field[j][i] == 0:
                        holes += 1
            tophole = False
        holediff = holes - self.holes
        self.holes = holes
        return (holediff)

    def _bumpiness(self):
        
        placeholder_1 = 20
        placeholder_2 = 20
        bumpiness = 0

        for i in range(self.height):
            if self.field[i][0] == 1:
                placeholder_1 = i
                break

        for i in range(1, self.width):
            for j in range(self.height):
                if self.field[j][i] == 1:
                    placeholder_2 = j
                    bumpiness += abs(placeholder_1 - placeholder_2)
                    placeholder_1 = placeholder_2
                    break
                if self.field[19][i] == 0:
                    placeholder_2 = 20
                    bumpiness += abs(placeholder_1 - placeholder_2)
                    placeholder_1 = placeholder_2
                    break

        bumpdiff = bumpiness - self.bumpiness
        self.bumpiness = bumpiness
        return bumpdiff



    #---------------------------------------------------------------------------# Making it into an environment #----------------------------------------------------------------------------------------------

    def getObservation(self):        
        return (self.field) + self.figure.figarray()
    
    # Discrete(13) kell ide
    #def step(self,action):
    #    if action == 0:
    #        self.rotate()
    #        self.go_down()
    #    if 1 <= action <= 5:
    #        for i in range(action):
    #            self.go_side(-1)
    #        self.go_space()
    #    if 6 <= action < 12:
    #        for i in range (action - 5):
    #            self.go_side(1)
    #        self.go_space()
    #    if action == 12:
    #        self.go_space()

    #def step(self,action):
    #    if action == 0:
    #        self.go_space()
    #    if 1 <= action <= 5:
    #        for i in range(action):
    #            self.go_side(1)
    #        self.go_space()
    #    if 6<= action <= 10:
    #        for i in range(action - 5):
    #            self.go_side(-1)
    #        self.go_space()
    #    if 11 <= action <= 15:
    #        self.rotate()
    #        for i in range(action - 10):
    #            self.go_side(+1)
    #        self.go_space()
    #    if 16<= action <= 20:
    #        self.rotate()
    #        for i in range(action - 15):
    #            self.go_side(-1)
    #        self.go_space()
    #    if 21<= action <= 25:
    #        self.rotate()
    #        self.rotate()
    #        for i in range(action - 20):
    #            self.go_side(+1)
    #        self.go_space()
    #    if 26 <= action <= 30:
    #        self.rotate()
    #        self.rotate()
    #        for i in range(action - 25):
    #            self.go_side(-1)
    #        self.go_space()
    #    if 31 <= action <= 35:
    #        self.rotate()
    #        self.rotate()
    #        self.rotate()
    #        for i in range(action - 30):
    #            self.go_side(+1)
    #        self.go_space()
    #    if 36 <= action <= 40:
    #        self.rotate()
    #        self.rotate()
    #        self.rotate()
    #        for i in range(action - 35):
    #            self.go_side(-1)
    #        self.go_space()
            

    #    # OpenAI requires an info slot
    #    info = {}

    #    self.state = self.getObservation()

    #    temp_reward = self.reward
    #    self.reward = 0
    #    time.sleep(0.2)

    #    return self.state, temp_reward, self.done, info

    def step(self,action):
        if 0 <= action <= 4:
            for i in range(action + 1):
                self.go_side(1)
            self.go_space()
        if 5<= action <= 9:
            for i in range(action - 4):
                self.go_side(-1)
            self.go_space()
        if 10 <= action <= 14:
            self.rotate()
            for i in range(action - 9):
                self.go_side(+1)
            self.go_space()
        if 15 <= action <= 19:
            self.rotate()
            for i in range(action - 14):
                self.go_side(-1)
            self.go_space()
        if 20 <= action <= 24:
            self.rotate()
            self.rotate()
            for i in range(action - 19):
                self.go_side(+1)
            self.go_space()
        if 25 <= action <= 29:
            self.rotate()
            self.rotate()
            for i in range(action - 24):
                self.go_side(-1)
            self.go_space()
        if 30 <= action <= 34:
            self.rotate()
            self.rotate()
            self.rotate()
            for i in range(action - 29): # elírva 30ra lehet fos emiatt
                self.go_side(+1)
            self.go_space()
        if 35 <= action <= 39:
            self.rotate()
            self.rotate()
            self.rotate()
            for i in range(action - 34):
                self.go_side(-1)
            self.go_space()
            

        # OpenAI requires an info slot
        info = {}

        self.state = self.getObservation()

        temp_reward = self.reward
        self.reward = 0
        #time.sleep(0.2)

        return self.state, temp_reward, self.done, info

    def reset(self):
        self.game = "start"
        self.field = np.zeros((20,10), dtype = np.int32)
        self.figure = Figure(3,0)
        self.score = 0
        self.reward = 0
        self.holes = 0
        self.height_counter = 20
        self.bumpiness = 0
        self.done = False
        self.state = (self.field) + (self.figure.figarray())
        return self.state
   

    #-------------------------------------------------------------------------------------# Visualization #-------------------------------------------------------------------------------------------------


    def render(self, mode):
        pygame.display.set_caption("Tetris")

        # Rendering parameters
        pygame.init()
        screen = pygame.display.set_mode((400, 500))

        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen,(128, 128, 128), [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom], 1)
                if self.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[self.field[i][j]],
                                        [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2, self.zoom - 1])

        if self.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.figure.image():
                        pygame.draw.rect(screen, colors[self.figure.color],
                                            [self.x + self.zoom * (j + self.figure.x) + 1,
                                            self.y + self.zoom * (i + self.figure.y) + 1,
                                            self.zoom - 2, self.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(self.score), True, (0, 0, 0))
        text_game_over = font1.render("Game Over", True, (255, 125, 0))

        screen.blit(text, [0, 0])
        if self.done == True:
           screen.fill((255, 255, 255))
        
        pygame.display.flip()


#env = TetrisEnv()

