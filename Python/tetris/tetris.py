#!/home/azat/anaconda3/envs/game/bin/python
from random import choice, randrange

import pygame
from settings import *
from copy import deepcopy

def main():
  W, H, TILE, FPS = 10, 20, 35, 60
  shapes = ["square", "line", "tblock", "lblock", "revlblock", "squiz", "revsquiz"]
  Game = GameSession(W, H, TILE)
  square = Figure("square")
  line = Figure("line")
  figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
  anim_count, anim_speed, anim_limit = 0, FPS, 2000
  fig = deepcopy(Figure(choice(shapes)))
  field = [[0 for i in range(W)] for j in range(H)]
  
  def check_borders():
    if fig.figure[i].x < 0 or fig.figure[i].x > W - 1:
       return False
    elif fig.figure[i].y > H - 1 or field[fig.figure[i].y][fig.figure[i].x]:
       return False
    return True


  while True:
    dx = 0
    Game.game_sc.fill(pygame.Color('black'))

    for event in pygame.event.get():
       if event.type == pygame.QUIT:
          exit()

       if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_LEFT:
            dx = -1

         elif event.key == pygame.K_RIGHT:
            dx = 1
         elif event.key == pygame.K_DOWN:
            anim_limit = 100

    # move x
    fig_old = deepcopy(fig)
    for i in range(4):
      fig.figure[i].x += dx
      if not check_borders():
         fig = deepcopy(fig_old)
         break 
 
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
       anim_count = 0
       fig_old = deepcopy(fig)
       for i in range(4):
         fig.figure[i].y += 1
         if not check_borders():
            # fill cells by figure
            for i in range(4):
               field[fig_old.figure[i].y][fig_old.figure[i].x] = pygame.Color("yellow")
            fig = deepcopy(Figure(choice(shapes)))
            anim_limit = 2000
            break

    # draw the grid
    [pygame.draw.rect(Game.game_sc, (40, 40, 40), i_rect, 1) for i_rect in Game.grid]


    # draw the figure
    for i in range(4):
       figure_rect.x = fig.figure[i].x * TILE
       figure_rect.y = fig.figure[i].y * TILE
       pygame.draw.rect(Game.game_sc, pygame.Color("yellow"), figure_rect)
    
    # draw the field
    for y, raw in enumerate(field):
       for x, col in enumerate(raw):
          if col:
            figure_rect.x = fig.figure[i].x * TILE
            figure_rect.y = fig.figure[i].y * TILE
            pygame.draw.rect(Game.game_sc, col, figure_rect)
    
    pygame.display.flip()
    Game.clock.tick(FPS)


if __name__ == "__main__":
  main()
