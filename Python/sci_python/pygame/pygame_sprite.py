# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
from math import sin, cos, pi, ceil
import os 


WIDTH = 640
HEIGHT = 480
FPS = 30
game_name = "My Game"
 
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

sprites = [pygame.image.load("pictures/spin/"+sprite) for sprite in os.listdir("pictures/spin")]

skin = pygame.image.load("pictures/spin/my_sprite.png")

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

def turn(coord:tuple, smooth=90) -> tuple:
    return ceil(coord[0] * cos(pi / smooth) - coord[1] * sin(pi / smooth)), ceil(coord[0] * sin(pi / smooth) + coord[1] * cos(pi / smooth))

class Player(pygame.sprite.Sprite):
    def __init__(self,skin=skin):
        pygame.sprite.Sprite.__init__(self)
        self.image = skin
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.reach_right = False
        self.reach_top = False

    def rot_center(self, angle=30):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):

        if self.rect.right >= WIDTH:
           self.reach_right = True

        elif self.rect.left <= 0:
           self.reach_right = False
        
        
        if self.rect.bottom >= HEIGHT:
           self.reach_top = True

        elif self.rect.top <= 0:
           self.reach_top = False

        state = sprites.pop(0)
        self.image = state
        sprites.append(state)
        self.rect.x += 5 * ((-1) ** int(self.reach_right))
        self.rect.y += 5 * ((-1) ** int(self.reach_top))



# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()

