import pygame
import os
import random

pygame.font.init()
WIN_CASE_HEIGHT = 20
WIN_CASE_WIDTH = 15

CASE_SIZE = 34

WIN_WIDTH = WIN_CASE_WIDTH * CASE_SIZE
WIN_HEIGHT = WIN_CASE_HEIGHT * CASE_SIZE + 30

pygame.display.set_caption("Tetris")

TABLE = []
for i in range(0, WIN_CASE_HEIGHT):
    tmp = []
    for j in range(0, WIN_CASE_WIDTH):
        tmp.append("0")
    TABLE.append(tmp)

BLOCK1 = [["x"],
          ["x"],
          ["x"],
          ["x"]]

BLOCK2 = [[ "x", "0"],
          [ "x", "0"],
          [ "x", "x"]]

BLOCK3 = [["0", "x", "0"],
          ["x", "x", "x"]]

BLOCK4 = [["x", "x", "0"],
          ["0", "x", "x"]]

BLOCK5 = [["x", "x"],
          ["x", "x"]]

STRUCTURES = [BLOCK1, BLOCK2, BLOCK3, BLOCK4, BLOCK5]

BLOCK_IMG = pygame.image.load(os.path.join("imgs", "block.jpg"))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))


def setOrientation(block, orientation):
    rows = len(block[0])
    columns = len(block)
    if orientation % 2 == 0:
        rows = len(block)
        columns = len(block[0])
    tmp = []
    for i in range(0, columns):
        tmp2 = []
        for j in range(0, rows):
            if orientation % 4 == 0 or orientation == 0:
                tmp2.append(block[j][i])
            elif orientation % 4 == 1:
                tmp2.append(block[i][len(block[0]) - 1 - j])
            elif orientation % 4 == 2:
                tmp2.append(block[len(block) - j - 1][len(block[0]) - i - 1])
            elif orientation % 4 == 3:
                tmp2.append(block[len(block) - i - 1][j])
        tmp.append(tmp2)




    return tmp


def printarray(a):
    s = ""
    for i in range(0, len(a)):
        for j in range(0, len(a[0])):
            s = s + " [ " + str(a[i][j]) + " ] "

        s = s + "\n"
    print(s)


def getMirror(structure):
    tmp = []
    for i in range(0, len(structure)):
        tmp2 = []
        for j in range(0, len(structure[0])):
            tmp2.append(structure[i][len(structure[0]) - j - 1])
        tmp.append(tmp2)
    return tmp




class Block:
    velY = 1
    velX = 0
    stopped = False
    img = BLOCK_IMG

    def __init__(self, x, y):
        # Chosing which block
        self.orientation = random.randint(1, 5)
        self.structure = setOrientation(STRUCTURES[random.randint(0, 4)], self.orientation)
        self.height = self.img.get_width() / CASE_SIZE  # set height depending on image
        self.tick_count = 0
        # chosing orientation
        if random.randint(0, 2) == 1:
            self.structure = getMirror(self.structure)
        printarray(self.structure)

        self.x = x
        self.y = y

    def changeOrientation(self):
        self.orientation += 1
        if self.x+(len(self.structure)*CASE_SIZE) >= WIN_WIDTH:
            self.x = WIN_WIDTH - (len(self.structure)*CASE_SIZE)
        self.structure = setOrientation(self.structure, self.orientation)

#    def draw(self, win):
 #       for i in range (0, len(self.structure)):
  #          for j in range(0 , len(self.structure[0])):
   #             if self.structure[i][j] == "x":
    #                win.blit(self.img, (self.x + 35*j, self.x + 35*i))


    def move(self):
        self.tick_count += 1
        if self.tick_count % 3 == 0:
            self.y += self.velY * CASE_SIZE
        self.x += self.velX * CASE_SIZE

    def Right(self):
        self.velX += 1

    def Left(self):
        self.velX -= 1



    def stop(self):
        self.velX = 0
        self.velY = 1

    def receive(self):
        self.velY = 0
        self.velX = 0
        self.stopped = True

    def setStopped(self):
        return self.stopped

    def collide(self, map):
        top = round(self.y/CASE_SIZE)
        bottom = round((self.y/CASE_SIZE) + len(self.structure)-1)
        left = round(self.x/CASE_SIZE)
        right = round((self.x/CASE_SIZE) + len(self.structure[0])-1)
 ###
        if bottom + 1 >= len(map):
            self.receive()
            print("collided with base")
            print("true")
            return True
        if left <= 0 or right + 1 >= 15:
            self.velX = 0
            print("colliding with borders")
        for i in range(top, bottom+1):
            if map[i][left - 1] == "x":
                if map[i][left] == "x":
                    if self.velX <= 0:
                        self.velX = 0
                        printarray(self.structure)
                        print("collided with blocks from the left")
            if right+1 < 15 and map[i][right + 1] == "x":
                if map[i][right] == "x":
                    if self.velX >= 0:
                        self.velX = 0
                        printarray(self.structure)
                        print("collided with blocks from the right")
        for i in range(left, right+1):
            if map[bottom+1][i] == "x":
                if map[bottom][i] == "x":
                    self.velY = 0
                    self.setStopped()
                    printarray(self.structure)
                    print("collided with blocks")
                    if self.x == 0:
                        print("Game over")
                    return True
 ###
        return False


class World:
    tick = 0
    def __init__(self, width, height, blocks):
        self.win = pygame.display.set_mode((width, height))
        self.map = []
        for i in range(0, WIN_CASE_HEIGHT):
            tmp = []
            for j in range(0, WIN_CASE_WIDTH):
                tmp.append(" ")
            self.map.append(tmp)

        self.blocks = blocks
        self.base = Base()

    def draw_window(self):
        self.win.blit(BG_IMG, (0, 0))
        self.updatemap()
        self.base.draw(self.win)
        self.drawmap()
        if self.tick % 3 == 0:
            printarray(self.map)

        pygame.display.update()

    def handlecollisions(self):
        block = self.blocks[len(self.blocks)-1]
        self.updatemap()
        if block.collide(self.map):
            self.checklines()
            return self.newblock()
        return block

    def newblock(self):
        tmp = Block(7 * CASE_SIZE, 0)
        self.blocks.append(tmp)
        return tmp

    def updatemap(self):
        for i in range(0, len(self.map)):
            for j in range(0, len(self.map[0])):
                self.map[i][j] = " "
        for x in range(0, len(self.blocks)):
            b = self.blocks[x]
            for i in range(0, len(b.structure)):
                for j in range(0 , len(b.structure[0])):
                    if b.structure[i][j] == "x":
                        self.map[round(b.y/CASE_SIZE) + i][round(b.x/CASE_SIZE) + j] = "x"

    def drawmap(self):
        for i in range(0, len(self.map)):
            for j in range(0, len(self.map[0])):
                if self.map[i][j] == "x":

                    self.win.blit(Block.img, (j*CASE_SIZE, i*CASE_SIZE))

    def checklines(self):
        i = 0
        while i<len(self.map):
            j = 0
            while self.map[i][j] == "x":
                j = j+1
                if j == len(self.map[0])-1:
                    self.destroyline(i)
                    return True
            i = i+1
        return False

    def destroyline(self, line):
        print("test")
        for i in range(0, len(self.map)):
            for j in range(1, len(self.map[0])-line-1):
                self.map[line+j-1][i] = self.map[line+j][i]
        self.updatemap()


class Base:
    WIDTH = BASE_IMG.get_width()
    HEIGHT = BASE_IMG.get_height()
    IMG = BASE_IMG

    def __init__(self):
        self.y = WIN_HEIGHT - 30
        self.x = 0
        self.top = self.y + self.HEIGHT

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    # def collide(self, block):


def main():
    clock = pygame.time.Clock()
    current_block = Block(CASE_SIZE*7, 0)
    blocks = [current_block]
    world = World(WIN_WIDTH, WIN_HEIGHT, blocks)




    run = True
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_block.Right()
                if event.key == pygame.K_LEFT:
                    current_block.Left()
                if event.key == pygame.K_DOWN:
                    last_block = current_block
                    while last_block == current_block :
                        current_block = world.handlecollisions()
                        current_block.move()

                if event.key == pygame.K_SPACE:
                    current_block.changeOrientation()

            else:
                current_block.stop()


        current_block = world.handlecollisions()

        current_block.move()

        world.draw_window()



main()

