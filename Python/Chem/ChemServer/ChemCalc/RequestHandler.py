import json

def from_file(filename:str) -> dict:
  data = {}
  with open(filename) as file:
    data = json.loads(file.read())
  return data


def from_request(request:str) -> dict:
  return json.loads(request)

def from_cli_parameters(reaction:str, reagent_masses:list[str]) -> dict:
  data = {}
  data["reaction"] = reaction
  # another level of comprehension needs for type cast of masses to proper type (float)
  data["reagent_masses"] = {compound:float(mass) for compound, mass in [component.split('=') for component in reagent_masses]}
  return data



