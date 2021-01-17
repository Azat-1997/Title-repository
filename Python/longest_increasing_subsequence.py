#!/usr/bin/python
def increase_max_seq(xs:list):

  counts = [1] * len(xs)
  indexes = set()
  for j, elem_j in enumerate(xs[1:], start = 1):

    for i, elem_i in enumerate(xs[:j]):

      if elem_j > elem_i and counts[j] <= counts[i]:

        counts[j] = counts[i] + 1
        indexes.add(i)
        indexes.add(j)
  
  values = []
  for k in indexes:
    values.append(xs[k])
  
  return values
