# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 640
HEIGHT = 640
FPS = 20
game_name = "My Game"
 
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cделаем фон
background = pygame.image.load('pictures/unnamed.jpg')

# Название игры
pygame.display.set_caption(game_name)
clock = pygame.time.Clock()

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
    
    # Рендеринг
    screen.fill(BLACK)
    # Рисуем фон.
    screen.blit(background, (10, 10))
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
