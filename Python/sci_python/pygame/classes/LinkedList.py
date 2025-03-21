class Stack:
# Stack as example of implementation of LinkedList
  def __init__(self, element = None, address = None):
    self.element = element
    self.address = address

  def push(self, x):
    self.address = Stack(element = self.element, address = self.address)
    self.element = x

  def pop(self):
    if self.element is None:
      raise ValueError("Empty Stack")
    last = self.element
    self.element, self.address = self.address.element, self.address.address  
    return last

