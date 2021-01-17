#!/usr/bin/python

def bubble_sort(xs:list):

  for i, elem_i in enumerate(xs[:-1]):

    for j, elem_j in enumerate(xs[:-i-1]):

      if xs[j] > xs[j+1]:
        
        xs[j], xs[j+1] = xs[j+1], xs[j]
  
  return xs


def insert_sort(lst):

  N = len(lst)

  for i in range(1,N):

    for j in range(i):
      
      if lst[i] < lst[j]:

        lst[i],lst[j] = lst[j],lst[i]


  return lst
