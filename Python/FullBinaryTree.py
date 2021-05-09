import random

class FullBinaryTree(list):
 def is_right_exist(self, i):
  return len(self) > 2 * i + 2
  
 def is_left_exist(self, i):
  return len(self) > 2 * i + 1
 
 def is_terminal(self, i):
  # if left is absent - right is absent too
  # our tree filled from left to the right
  return (len(self) <= 2 * i + 1)
  
 def get_right(self, i):
  if self.is_right_exist(i):
   return self[2 * i + 2]
  else:
   return None
  
 def get_left(self, i):
  if self.is_left_exist(i):
   return self[2 * i + 1]
  else:
   return None
  
 def get_parent(self, i):
  return self[i // 2]
  
 def get_last_anc(self, i, j):
  pass 
  
  
#########################$  

def main():  
 test = FullBinaryTree([i for i in range(16)])
 print(test)
 print(test.get_right(3))
 print(test.get_left(3))
 print(test.get_parent(3))
 
if __name__ == "__main__":
 main()
