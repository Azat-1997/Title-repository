#!/usr/bin/python

def fib(n:int) -> int:
  a = 0
  b = 1
  for i in range(n):
    a,b = b, a + b
  
  return n

def fac(n:int) -> int:
  res = 1
  if n:
    for i in range(1,n):
      res *= i

  return res
