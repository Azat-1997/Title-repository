import requests
import csv
from pprint import pformat
from json import loads as read_config
from json import dumps as write_payload
from shiny import ui, App, reactive, render
from App.AppUIs import BaseUI, FluidPageUI
from App.AppServers import CalculatorInterface, BaseServer

CLIENT_CONFIG = 'client_config.json'


class ChemCalculatorUI(FluidPageUI):
  
  @staticmethod
  def create_solution_section(content_id, title):
    return ui.div([ui.h5(title), ui.output_text_verbatim(content_id)])
  
  def create_input(self):
        return [ui.input_text("reaction", "Enter the reaction equation"),
                ui.input_text_area("textarea", "Reagent masses in CSV (no header)", ""),
                ui.input_action_button("calculate", "Take a solution")]
      
  def create_output(self):
    return [
    self.create_solution_section("equation", "Equation:"),
    self.create_solution_section("reagent_masses", "Reagent masses:"),
    self.create_solution_section("product_masses", "Product masses:")
    ]
        
  

class ChemCalculatorServer(BaseServer, CalculatorInterface):
  
  def register_callbacks(self):
    self.setup_calculation()
  
  @staticmethod
  def get_settings_from_config(config_name:str) -> dict:
    config = None
    with open(config_name) as config:
      config = read_config(config.read())
      
    if config is None:
      raise Exception("Config doesn`t exist or have improper format")
    
    return config
    
  @classmethod  
  def get_solution(cls, data:dict):
    # take essential settings before making a call to FastAPI app
    config = cls.get_settings_from_config(CLIENT_CONFIG)
    host = config["chem-api-host"]
    port = config["chem-api-port"]
    method = config["chem-api-method"]
    response = requests.Response()
    response.status_code = 500
    try:
      response = requests.post(url=f"http://{host}:{port}/{method}", json=data)
    except:
      print("Log of unexpected error...")
      
    return response
      
    
  def setup_calculation(self):
    
    def __format_solution_section(solution_attribute:dict):
      return "\n".join([f"{entry['compound']}: {entry['mass']}" for entry in solution_attribute])
    
    @reactive.event(self.input.calculate)
    def produce_solution() -> dict:
      reader = csv.reader(self.input.textarea().strip().split('\n'), delimiter=';')
      data = {}
      data["reaction"] = self.input.reaction() 
      data["reagent_masses"] = [{'compound':compound, 'mass':float(mass)} for compound, mass in reader]
      # make a call to FastAPI application
      response = self.get_solution(data)
      if response.ok:
        return response.json()
      else:
        raise requests.HTTPError("Problem during requesting solver service...")
      
    @self.output
    @render.text("equation")
    def equation():
      return produce_solution()["reaction"]
    
    @self.output    
    @render.text("reagent_masses")
    def reagent_masses():
      # take a dictionary
      return __format_solution_section(produce_solution()["reagent_masses"])
    
    @self.output
    @render.text("product_masses")
    def product_masses():
      # take a dictionary
      return __format_solution_section(produce_solution()["product_masses"])


app = App(ChemCalculatorUI().get_page(), ChemCalculatorServer)


if __name__ == "__main__":
    app.run()
