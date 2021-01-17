class Heap(list):

  def heapify(self, i):
    #''' Rearrange subtree which is started from i-node.  Asymptotic: O(log(n))'''
    heapsize = len(self)
    largest = i

    while (2 * i) <= heapsize:

      left = 2*i + 1      
      right = 2*i + 2

      # change element with maximal child
      if left < heapsize and self[left] > self[largest]:
        largest = left

      if right < heapsize and self[right] > self[largest]:
        largest = right

      # continue with element
      if largest != i:
        self[i], self[largest] = self[largest], self[i]
        i = largest

      else:       
        break

  def build_heap(self):
   #''' You should call this method after you make heap from list to be sure that you have right structure of heap.
    #   Asymptotic: O(n)''' 
    heapsize = len(self) 
    for i in range(heapsize // 2 + 1, -1, -1):
      self.heapify(i)
  
  def change_key(self, index, key):
    #''' Using both negative and postive priority is not recommended.
     #   Asymptotic: O(log(n)) '''
    self[index] = key
 #   if key < 0:
  #    raise ValueError("key should be a non-negative")

    while self[index] > self[index // 2]:
      self[index], self[index // 2] = self[index // 2], self[index] 
      index = index // 2

  def append(self, x):
    #''' Add element and store the order.
     #   Asymptotic: O(log(n)). The main operation is change_key. Only adding element is O(1)'''
    super(Heap, self).append(x)
    heapsize = len(self)
    self.change_key(heapsize-1, x)

  def extract_max(self):
    #''' Take maximal element. This action have O(1) asymptotic. '''
    if self == Heap([]):
      raise("Heap is empty")

    self[0], self[-1] = self[-1], self[0]
    element = self.pop()
    self.heapify(0)
    return element

  def __add__(self, other):
#    ''' Produce new priority queue which is sum of previous '''
    new = Heap(super(Heap, self).__add__(other))
    new.build_heap()  
    return new

  def merge(self, other):  
 #   ''' Extend one priority queue by another '''  
    self.extend(other)
    self.build_heap()

