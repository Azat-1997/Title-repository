from sys import argv, stdout, stderr, stdin
from time import sleep
from os import system, name
from collections import deque

def get_moore(cell, n, m, rank=1):
  # get the neigbores in Moore's neigborehood
  res = {}
  for i in range(-rank, rank+1):
    for j in range(-rank, rank+1):
      if i != 0 or j != 0:
        neigbore = ((cell[0]+i)%n, (cell[1]+j)%m) 
        if neigbore not in res.keys():
          res[neigbore] = 1
        else:
          res[neigbore] += 1
  return res
  

def is_survive():
  pass

def is_birth():
  pass


def generate(n, m, living_cells):
  new_cells = set()
  old_cells = set()
  all_ngb = set()
  
  for cell in living_cells:
    ng = get_moore(cell, n, m)
    all_ngb.update(set(ng.keys())) 
    if len(set(ng.keys()) & living_cells) in {2, 3}:
      old_cells.add((cell[0], cell[1]))
      
      
  for cell in all_ngb:
    if cell not in living_cells:
      total_count = 0
      moore = get_moore(cell, n, m)
      for coord, count in moore.items():
         if coord in living_cells:
            total_count += count
      if total_count == 3:
        new_cells.add((cell[0], cell[1]))
  
  return old_cells ^ new_cells
  
  

def get_field_conf(n, m, generation):
  field = []
  for i in range(n):
    for j in range(m):
      if (i, j) in generation:
        field.append("X")
      else:
        field.append(".")
        
    field.append("\n")
  return "".join(field)
	
def print_generation(n, m, generation):
  for i in range(n):
    for j in range(m):
      if (i, j) in generation:
        stdout.write("X")
      else:
        stdout.write(".")
        
    stdout.write("\n")

    
if __name__ == "__main__":
 fps = 120
 max_steps = 640
 
 file = open(argv[1])  

 n, m = map(int, file.readline().split())
 nrow = 0
 living_cells = set()
 for line in file:
   for ncol, sym in enumerate(line):
     if sym == "X":
       living_cells.add((nrow, ncol))
   nrow +=1
 file.close()

 generation = generate(n, m, living_cells)
 demo = []
 print("Steps evaluation...")
 for i in range(max_steps):
   demo.append(get_field_conf(n, m, generation))
   generation = generate(n, m, generation)

 while True:
   for step in demo:
     print(step)
     sleep(1/fps)
     system('cls' if name == 'nt' else 'clear')



