# import the pygame module
import pygame
from pygame.locals import *
from sys import exit
import os

screen_x = 640
screen_y = 480
score = 0
phase = 1

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Space Invaders")

main_directory = os.path.dirname(__file__)
images_directory = os.path.join(main_directory, "images")

icon = pygame.image.load(os.path.join(images_directory, "ship.png")).convert_alpha()
pygame.display.set_icon(icon)

pygame.font.init()
basic_source = pygame.font.get_default_font()
score_source = pygame.font.SysFont(basic_source, 22)
phase_source = pygame.font.SysFont(basic_source, 25)

class Ship(pygame.sprite.Sprite):
    def __init__(self, x=screen_x/2, y=screen_y-50, length=25, height=25, speed=0.2):
        pygame.sprite.Sprite.__init__(self)
        self.img = None
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.speed = speed

    def draw_ship(self):
        img = pygame.image.load(os.path.join(images_directory, "ship.png")).convert_alpha()
        self.img = pygame.transform.scale(img, (25, 25))


class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, invisible=True, length=18, height=30, speed=0.7, 
        out_of_screen=True, hit=False):
        self.img = None
        self.x = x
        self.y = y
        self.invisible = invisible
        self.length = length
        self.height = height
        self.speed = speed
        self.out_of_screen = out_of_screen
        self.hit = hit

    def draw_shot(self):
        if not self.invisible:
            img = pygame.image.load(os.path.join(images_directory, "shot.png")).convert_alpha()
            self.img = pygame.transform.scale(img, (15, 15))

    def move_shot(self):
        if not self.invisible:
            if self.y < 0:
                self.x = ship.x + ship.length / 4
                self.y = ship.y - ship.height / 2 - self.height / 2
                self.invisible = True
                self.out_of_screen = True
            if not self.invisible and not self.out_of_screen:
                self.y -= self.speed

def move_enemy(enemy_x, enemy_y, enemy_x_change):
    for i in range(num_of_enemies):
        # Enemies moves into the x
        enemyX[i] += enemy_x_change[i]
        # When they came closer to the end of the screen x they go down
        if enemy_x[i] > screen_x:
            enemy_x_change[i] = -enemy_x_change[i]
            enemy_y[i] += 100
        if enemy_x[i] < 0:
            enemy_x_change[i] = -enemy_x_change[i]
            enemy_y[i] += 100


def enemy_shoot():
    for i in range(num_of_enemies):
        if enemy_shot_shoot[i]:
            enemy_shot_y[i] = enemyY[i]+enemy_shot_Size
            enemy_shot_invisible[i] = False
        enemy_shot_shoot[i] = False


def move_enemy_shot():
    for i in range(num_of_enemies):
        # When the shot goes out of the screen y
        if enemy_shot_y[i] + enemy_shot_Size > screen_y:
            enemy_shot_out_of_screen[i] = True
            enemy_shot_invisible[i] = True
            enemy_shot_shoot[i] = True
            enemy_shot_stop[i] = True
            enemy_shot_stop[i] = True
        # Shows the shoot moving throw the screen y
        if not enemy_shot_invisible[i]:
            enemy_shot_y[i] += enemy_shot_speed


def collision(Ax, Ay, Alength, Aheight, Bx, By, Blength, Bheight):
    if Ay + Aheight < By:
        return False
    elif Ay > By + Bheight:
        return False
    elif Ax + Alength < Bx:
        return False
    elif Ax > Bx + Blength:
        return False
    else:
        return True


def enemy_dead(score):
    for j in range(num_of_enemies):
        # If the ship's shot hit the enemy
        if collision(enemyX[j], enemyY[j], enemySize, enemySize, shot.x, shot.y, shot.length, 
            shot.height):
            enemy_destroyed[j] = True
            enemyX[j] = screen_x + 100
            shot.hit = True
            shot.invisible = True
            score = score + 100
            shot.x = ship.x + ship.length / 4
            shot.y = ship.y - ship.height / 2 - shot.height / 2
    return score


def ship_lose_life(num_of_life):
    for i in range(num_of_enemies):
        if collision(ship.x, ship.y, ship.length, ship.height, enemyX[i], enemy_shot_y[i], 
            enemy_shot_Size, enemy_shot_Size):
            num_of_life -= 1
            enemy_shot_invisible[i] = True
            enemy_shot_y[i] = enemyY[i]+enemy_shot_Size
            enemy_shot_shoot[i] = False
    return num_of_life

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemy_destroyed = []
enemySize = 30
num_of_enemies = 22
img1 = pygame.image.load(os.path.join(images_directory, "alien.png")).convert_alpha()

x, y = 40, 40
for i in range(num_of_enemies):
    if x > screen_x:
        x = 40
        y += 40

    enemyImg.append(pygame.transform.scale(img1, (enemySize, enemySize)))
    enemyX.append(x)
    enemyY.append(y)
    enemyX_change.append(0.05)
    enemy_destroyed.append(False)
    x += 60

# ----------------------------------------------------------------------------------------
# Enemy Shot
enemy_shot_Img = []
enemy_shot_x = []
enemy_shot_y = []
enemy_shot_invisible = []
enemy_shot_shoot = []
enemy_shot_stop = []
enemy_shot_out_of_screen = []
enemy_shot_Size = 10
enemy_shot_speed = 0.15
img2 = pygame.image.load(os.path.join(images_directory, "alien_shot.png")).convert_alpha()
for i in range(num_of_enemies):
    enemy_shot_Img.append(pygame.transform.scale(img2, (enemy_shot_Size, enemy_shot_Size)))
    enemy_shot_x.append(enemyX[i])
    enemy_shot_y.append(enemyY[i]+enemy_shot_Size)
    enemy_shot_out_of_screen.append(True)
    enemy_shot_invisible.append(True)
    enemy_shot_stop.append(False)
    enemy_shot_shoot.append(True)
# ----------------------------------------------------------------------------------------
# Ship life
num_of_life = 3
img3 = pygame.image.load(os.path.join(images_directory, "life.png")).convert_alpha()
life_Img = []
life_x = []
life_y = []
life_check = []
life_size = 20
for i in range(num_of_life):
    life_Img.append(pygame.transform.scale(img3, (life_size, life_size)))
    life_x.append(20*i)
    life_y.append(0)
    life_check.append(True)

ship = Ship()
shot = Shot(0, 0)
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    commands = pygame.key.get_pressed()
    if commands[pygame.K_ESCAPE]:
        running = False
    # Makes the ship move and never goes out the scream
    if commands[pygame.K_UP] and ship.y > 0:
        ship.y -= ship.speed
    if commands[pygame.K_DOWN] and ship.y < screen_y-ship.height:
        ship.y += ship.speed
    if commands[pygame.K_LEFT] and ship.x > 0:
        ship.x -= ship.speed
    if commands[pygame.K_RIGHT] and ship.x < screen_x-ship.length:
        ship.x += ship.speed
    if commands[pygame.K_SPACE]:
        if shot.out_of_screen or shot.hit:
            shot.x = ship.x + ship.length/4
            shot.y = ship.y - ship.height/2 - shot.height/2
            shot.invisible = False
            shot.out_of_screen = False
            shot.hit = False
    screen.fill((0, 0, 0))
    shot.draw_shot()
    shot.move_shot()
    ship.draw_ship()
    num_of_life = ship_lose_life(num_of_life)
    move_enemy(enemyX, enemyY, enemyX_change)
    enemy_shoot()
    score = enemy_dead(score)
    move_enemy_shot()
    text_score = score_source.render(f"Score: {score}", 1, (255, 255, 0))
    screen.blit(text_score, (0, 22))
    text_phase = phase_source.render(f"Fase {phase}", 1, (255, 255, 255))
    screen.blit(text_phase, ((screen_x/2)-25, 5))
    if num_of_life > 0:
        screen.blit(ship.img, (ship.x, ship.y))
    for i in range(num_of_life):
        screen.blit(life_Img[i], (life_x[i], life_y[i]))
    for i in range(num_of_enemies):
        if not enemy_destroyed[i]:
            screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))
        if not enemy_shot_invisible[i]:
            screen.blit(enemy_shot_Img[i], (enemyX[i], enemy_shot_y[i]))
    if not shot.invisible:
        screen.blit(shot.img, (shot.x, shot.y))
    pygame.display.update()
