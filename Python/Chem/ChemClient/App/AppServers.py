from abc import ABC, abstractmethod

class BaseServer(ABC):
  def __init__(self, input, output, session):
      self.input = input
      self.output = output
      self.session = session
      self.register_callbacks()

  @abstractmethod
  def register_callbacks(self):
      """Implemented by subclasses to define server logic for handling inputs and outputs"""
      pass

class ConverterInterface(ABC):
  @abstractmethod
  def setup_conversion(self):
      pass
    
class CalculatorInterface(ABC):
  @abstractmethod
  def setup_calculation():
      pass


  
