import requests
import csv
from json import loads as read_config
from json import dumps as write_payload
from shiny import ui, App, reactive, render
from App.AppUIs import BaseUI, FluidPageUI
from App.AppServers import CalculatorInterface, BaseServer

class ChemCalculatorUI(FluidPageUI):
  
  def create_input(self):
        return [ui.input_text("reaction", "Enter the reaction equation"),
                ui.input_text_area("textarea", "Reagent masses in CSV (no header)", ""),
                ui.input_action_button("calculate", "Take a solution")]
      
  def create_output(self):
        return [ui.output_text_verbatim("solution")]

  

class ChemCalculatorServer(BaseServer, CalculatorInterface):
  def register_callbacks(self):
    self.setup_calculation()
    
  def get_solution(self, data:dict, config_name='server_config.json'):
    response = requests.Response()
    response.status_code = 500
    with open(config_name) as config:
      server_config = read_config(config.read())
      host = server_config['fastapi-server-host']
      port = server_config['fastapi-server-port']
      response = requests.post(url=f"http://{host}:{port}/solve", json=data)
      
    return response
    
    
      
    
  def setup_calculation(self):
    @self.output
    @render.text("solution")
    @reactive.event(self.input.calculate)
    def solution():
      reader = csv.reader(self.input.textarea().strip().split('\n'), delimiter=';')
      data = {}
      data["reaction"] = self.input.reaction() 
      data["reagent_masses"] = [{'compound':compound, 'mass':float(mass)} for compound, mass in reader]
      # make a call to FastAPI application
      response = self.get_solution(data)
      if response.ok:
        return write_payload(response.json())
      else:  
        raise requests.HTTPError("Problem during requesting solver service...")
      
      



app = App(ChemCalculatorUI().get_page(), ChemCalculatorServer)
