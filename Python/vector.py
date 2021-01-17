#!/usr/bin/python3

class vector:
  
  def __init__(self,x=0,y=0,z=0):
    self.x = x
    self.y = y
    self.z = z

  def __str__(self):
    return str(self.x)+','+str(self.y)+','+str(self.z)

  def __add__(self,other):
    return vector(self.x + other.x,
    self.y + other.y,
    self.z + other.z)

  def __sub__(self,other):
    return vector(self.x - other.x,
    self.y - other.y,
    self.z - other.z)

  def __mul__(self,other):
    if type(other) in {int, float}:

      return vector(self.x * other, self.y * other, self.z * other)

    else:

      return self.x * other.x + self.y * other.y + self.z * other.z

  def vector_mul(self,other):
    return vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)



a = vector(1,0,-3)
b = vector(0,2,5)
c = vector(-1,4,2)
print(a)
print(a * 5)
print(a * c)
print(c * a)
print(c.vector_mul(a))
print(a.vector_mul(c))
d = a + c
print(d)
