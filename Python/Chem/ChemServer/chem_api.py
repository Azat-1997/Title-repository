from collections import OrderedDict
import uvicorn
from json import loads as read_config
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from ChemCalc.RequestHandler import from_request
from ChemCalc.ChemCalcOOP import ReactionSolver

class ChemicalRequest(BaseModel):
  reaction: str
  reagent_masses: list[dict]
  product_masses: Optional[list[dict]] = None

class ChemicalResponse(BaseModel):
   reaction: str
   reagent_masses: list[dict]
   product_masses: list[dict]
  
CONFIG_NAME = 'server_config.json' 
host = None
port = None
with open(CONFIG_NAME) as config:
      server_config = read_config(config.read())
      host = server_config['fastapi-server-host']
      port = server_config['fastapi-server-port']
    
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the main page"}
  
@app.post("/solve", response_model=ChemicalResponse)
async def solve_reaction(data:ChemicalRequest) -> ChemicalResponse:
    if ReactionSolver._is_balanced_reaction(data.reaction):
      solver = ReactionSolver.from_balanced_reaction(data.reaction)
    else:
      solver = ReactionSolver.from_unbalanced_reaction(data.reaction)
    reagent_masses = {compound["compound"]:compound["mass"] for compound in data.reagent_masses}
    reagents, products = solver.find_products_amount(reagent_masses)

    response = {}
    response["reaction"] = solver.get_reaction()
    # After enomouros attempts the probable root case of failing was revealed
    # after calculation with chempy methods application gets custom float-class
    # and it`s breake the application
    # There some fix for ChemCalcOOP and adding one feature also
    # cast all numeric data explicitly to standart float (DONE)
    # add special method for printing reaction (DONE)
    response["reagent_masses"] = [{"compound":compound, "mass":mass} for compound, mass in reagents.items()]
    response["product_masses"] = [{"compound":compound, "mass":mass} for compound, mass in products.items()]
    response = ChemicalResponse(**response)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
