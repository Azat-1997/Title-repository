# put your python code here

# This implementaion will have priority queue and O(nlog(n) + mlog(n)) asymptotic
from math import inf
from sys import stdin
from Heap import Heap

def build_graph():
  graph = {}
  # dictionary: key - arc, value - length.
  arches = {}

  for line in stdin:
    enter, out, length = map(int, line.strip().split())
    if enter not in graph:
      graph[enter] = {out}
    else:
      graph[enter].add(out)

    arches[(enter, out)] = length

  return {"graph":graph, "arches_length":arches}


def get_shortest_path(graph:dict, arches:dict, start, end=None, max_iteration=100):

  path = []
  v = max(graph.keys()) + 1 
  hpq = Heap([(0, start)])
  dist = [inf] * v
  dist[start] = 0
  anc = [None] * v
 
  while hpq:  
    # get closest node. Actually, we extract pair.
     hpq_dist, node = hpq.extract_max()
# !!! Core of algorithm have weakness against cycles !!!          
     if node == end:
        break

     if -1 * hpq_dist != dist[node]:
        continue

     #print(f"{node} processing")

     for child in graph[node]:

        if dist[child] > dist[node] + arches[(node, child)]:
          dist[child] = dist[node] + arches[(node, child)]
          anc[child] = node
          hpq.append((-1 * dist[child],  child))
                
  # restore path
  vertice = end
  while vertice != start:
    if vertice is not None:
      path.append(vertice)

      vertice = anc[vertice]
  else:
    path.append(vertice)
 
  return reversed(path)

 
      
def main():
  weighted_graph = build_graph()
  graph, arches = weighted_graph["graph"], weighted_graph["arches_length"]
  path = get_shortest_path(graph, arches, start=0, end=6) 
  for i in path:
    print(i + 1, end= " ")
  print()


if __name__ == "__main__":
  main()



