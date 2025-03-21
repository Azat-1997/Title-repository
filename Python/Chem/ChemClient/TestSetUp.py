import json
from shiny.playwright import controller

class TestingClient:
  def __init__(self, app, page, reaction, csv_mass):
    page.goto(app.url)
    self.equation_controller  =  controller.OutputTextVerbatim(page, "equation")
    self.reagent_controller   =  controller.OutputTextVerbatim(page, "reagent_masses")
    self.product_controller   =  controller.OutputTextVerbatim(page, "product_masses")
    self.csv_mass_controller  =  controller.InputTextArea(page, "textarea")
    self.reaction_controller  =  controller.InputText(page, "reaction")
    self.reaction_controller.set(reaction)
    self.csv_mass_controller.set(csv_mass)
    # Take a solution
    page.click("#calculate")
    
