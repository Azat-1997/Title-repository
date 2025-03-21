from abc import ABC, abstractmethod
from shiny import render, ui, App, reactive

class BaseUI(ABC):
  def __init__(self, title="My Application", placeholder_text="Please provide input"):
      self.title = title
      self.placeholder_text = placeholder_text
      self.page = self.create_page()  # Updated to reference 'self.page' instead of 'self.layout'

  @abstractmethod
  def create_input(self):
      """Implement this method to define inputs for different UIs"""
      pass

  @abstractmethod
  def create_output(self):
      """Implement this method to define outputs for different UIs"""
      pass
    
  @abstractmethod
  def create_page(self):
      """Implement this method to define the whole page structure"""
      pass

  def get_page(self):
      """Return the page layout for use in the App"""
      return self.page


class FluidPageUI(BaseUI):
  def create_page(self):
      page = ui.page_fluid(
          *self.create_input(),
          *self.create_output()
      )
      return page
      
