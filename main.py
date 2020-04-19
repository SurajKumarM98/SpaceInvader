import os
import pygame
import random
import math


def fire_bullet(x, y, a, b):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet.Img, (int(x + a), int(y + b)))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    # print(distance)
    if distance < 27:
        return True
    else:
        return False


class Ship:
    def __init__(self, Img, posX, posY, size):
        self.Img = Img
        self.posX = posX
        self.posY = posY
        self.size = size

    def model(self):
        screen.blit(self.Img, (int(self.posX), int(self.posY)))
        # blit() draws things in the screen once its loaded

    def boundary(self):
        if (self.posX < 0):
            self.posX = 0
        if (self.posX > Swidth - self.size):
            self.posX = Swidth - self.size
        if (self.posY < 0):
            self.posX = 0
        if (self.posY > Swidth - self.size):
            self.posY = Swidth - self.size


class Enemy(Ship):
    def __init__(self, Img, posX, posY, size):
        super().__init__(Img, posX, posY, size)



pygame.init()  # initializing pygame

Swidth = 600
Sheight = 600

# creating screen with resolution 800*600
screen = pygame.display.set_mode((Swidth, Sheight))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join("assets", "galaxy.png"))
pygame.display.set_icon(icon)

# player
# playerImg = pygame.image.load('battleship.png')
player = Ship(pygame.image.load(os.path.join("assets", 'battleship.png')), 270, 510, 64)
player_change = 0

# enemy
# enemyImg = pygame.image.load('galaxy.png')
enemyX = random.randint(0, Swidth - 32)
enemyY = random.randint(0, 120)
enemy = Ship(pygame.image.load(os.path.join("assets", "spaceship.png")), enemyX, enemyY, 32)
# enemyX_change = 1.2
enemyY_change = .4

# bullet
bullet = Ship(pygame.image.load(os.path.join("assets", "rect16.png")), player.posX, player.posY, 16)
bulletY_change = 5

explosion = pygame.image.load(os.path.join("assets", "explosion.png"))
bullet_state = "ready"

running = True
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
enemies = []


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


while running:  # its like an infinite while loop where the game is constantly running and updating
    # changing the background of the screen
    # we want the display to be persistent... so put it in the while loop
    screen.fill((0, 0, 0))  # RGB values
    b_g = pygame.image.load(os.path.join("assets", 'bg.png'))
    screen.blit(b_g, (0, 0))  # image staring from cordinates 0,0

    # we have to go through the list of events that are happening in the game
    # playerX += 0.03  # moving the image towards left
    # print(playerX)

    for event in pygame.event.get():
        # check for event updates and perform updates accordingly
        if event.type == pygame.QUIT:  # checking if the quit button has been pressed
            running = False  # when the value turns false the game exits
        if event.type == pygame.KEYDOWN:  # pressing any key
            if event.key == pygame.K_a:  # pressing the up key
                player_change -= 2.0
            if event.key == pygame.K_d:  # pressing the up key
                player_change += 2.0
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet.posX = player.posX
                    fire_bullet(bullet.posX, player.posY, 2, 5)
                    fire_bullet(bullet.posX, player.posY, 56, 5)
        if event.type == pygame.KEYUP:  # releasing the key
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player_change = 0
    player.posX += player_change
    enemy.posY += enemyY_change

    # enemy.playerY += enemyY_change
    '''
    if enemy.posX <= 0:
        enemyX_change = 1.2
        enemy.posY += enemyY_change
    if enemy.posX >= Swidth - enemy.size:
        enemyX_change = -1.2
        enemy.posY += enemyY_change
    '''
    for enemy in enemies:
        screen.blit(enemy.Img, (enemy.x, enemy.y))

    if enemy.posY >= player.posY:
        running = False

    if bullet_state == "fire":
        fire_bullet(bullet.posX, bullet.posY, 0, 0)
        fire_bullet(bullet.posX + 56, bullet.posY + 5, 0, 0)
        bullet.posY -= bulletY_change
    if bullet.posY < 0:
        bullet.posY = player.posY
        bullet_state = "ready"

    # print(bullet.posY)
    # collision
    collision = isCollision(enemy.posX, enemy.posY, bullet.posX, bullet.posY)
    collision1 = isCollision(enemy.posX, enemy.posY, bullet.posX + 56, bullet.posY + 5)

    # print(distance)
    if collision or collision1:
        screen.blit(explosion, (int(bullet.posX), int(bullet.posY)))
        bullet.posY = player.posY
        bullet_state = "ready"
        score_value += 1



        enemy.posX = random.randint(0, Swidth - 32)
        enemy.posY = random.randint(0, 120)

    player.model()
    enemy.model()
    player.boundary()
    enemy.boundary()
    show_score(textX, textY)



    pygame.display.update()  # constantly update the screen
