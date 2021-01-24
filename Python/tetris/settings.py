import pygame

class GameSession:
  def __init__(self, W, H, TILE):
     pygame.init()
     self.game_sc = pygame.display.set_mode((W * TILE, H * TILE))
     self.clock = pygame.time.Clock()
     self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

class Figure:
  def __init__(self, type_fig="square", W=10):

    figures_pos = {"line": [(-1, 0), (-2, 0), (0, 0), (1, 0)],
               "square": [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               "squiz": [(-1, 0), (-1, 1), (0, 0), (0,-1)],
               "revsquiz": [(1, 0), (1, 1), (0, 0), (0, -1)],
               "tblock": [(0, -1), (0, 0), (0, 1), (-1, 0)],
               "lblock": [(-1, -1), (-1, 0), (0, 0), (1, 0)],
               "revlblock": [(-1, 1), (-1, 0), (0, 0), (1, 0)]}

    figures = {shape:[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in figures_pos[shape]] for shape in figures_pos}
    
    self.figure = figures[type_fig]

  def rotate(self):
    pass

  def moveleft(self):
    for i in range(4):
      self.figure[i].x -= 1

  def moveright(self):
    for j in range(4):
      self.figure[j].x += 1





