import chempy
from collections import OrderedDict

class ReactionSolver:
  
  def __init__(self, reagents:OrderedDict, products:OrderedDict):
    self.reagents, self.products  = reagents, products 

  def get_reaction(self) -> str:
    left_part  = [f"{coef}{compound}" if coef > 1 else compound for compound, coef in self.reagents.items()] 
    right_part = [f"{coef}{compound}" if coef > 1 else compound for compound, coef in self.products.items()]
    return f"{' + '.join(left_part)} -> {' + '.join(right_part)}"
  @staticmethod
  def calculate_mole(compound:str, mass:float) -> float:
    atomic_mass = chempy.Substance.from_formula(compound).mass
    mole        = mass / atomic_mass
    return mole
  
  @staticmethod
  def calculate_atomic_mass(compound:str) -> float:
    return chempy.Substance.from_formula(compound).mass
  
  @staticmethod 
  def _is_balanced_reaction(reaction:str) -> bool:
    status = False
    compound_processing = False
    for symbol in reaction:
      if symbol.isalpha() and not compound_processing:
        compound_processing = True
        
      elif compound_processing and symbol == ' ':
        compound_processing = False
        
      elif symbol.isdigit() and not compound_processing:
        status = True
        break
      
    return status
  
  @staticmethod
  def _take_coef(compound:str) -> tuple:
      coef = []
      for index, symbol in enumerate(compound):
        if symbol.isalpha():
          break
        elif symbol.isdigit():
          coef.append(symbol)
          
      coef = coef or ['1']
      
      return (compound[index:], int("".join(coef)))
    
  @classmethod  
  def from_unbalanced_reaction(cls, reaction:str):
    # check if we pass balanced case
    if cls._is_balanced_reaction(reaction):
      raise ValueError(f"Reaction - {reaction} already balanced. Please provide unbalanced version of it or use from_balanced_reaction() method")
    
    reagents_part_equation, products_part_equation = reaction.split("->")
    reagents = set(reagent.strip() for reagent in reagents_part_equation.split("+"))
    products = set(product.strip() for product in products_part_equation.split("+"))
    reagents, products = chempy.balance_stoichiometry(reagents, products)
    return cls(reagents, products) 
  
  @classmethod  
  def from_balanced_reaction(cls, reaction:str):
    # extract coefficent from balanced compounds
    
    reagents, products = reaction.split("->")
    reagents = OrderedDict([cls._take_coef(reagent.strip()) for reagent in reagents.split("+")])
    products = OrderedDict([cls._take_coef(product.strip()) for product in products.split("+")])
    return cls(reagents, products)
  
  
  def _calculate_ratio(self, masses_of_reagents:dict, accuracy=3) -> dict:
    reagents_mole_ratio = {compound : round(self.calculate_mole(compound, mass) / self.reagents[compound], accuracy) for compound, mass in masses_of_reagents.items()}
    return  reagents_mole_ratio
  
  def get_limiting_compound(self, masses_of_reagents:dict) -> str:
    reagents_mole_ratio = self._calculate_ratio(masses_of_reagents)
    return min(reagents_mole_ratio, key=reagents_mole_ratio.get)  


  def find_products_amount(self, masses_of_reagents:dict, accuracy=3) -> tuple[OrderedDict]:
    reagents_mole_ratio = self._calculate_ratio(masses_of_reagents)
    limiting_compound   = min(reagents_mole_ratio, key=reagents_mole_ratio.get)
    mole_limiting = self.calculate_mole(limiting_compound, masses_of_reagents[limiting_compound])
    stoichimetric_coef  = self.reagents[limiting_compound]
    equivalent = mole_limiting / stoichimetric_coef
    reagent_masses = OrderedDict({compound: round(float(coef * equivalent * self.calculate_atomic_mass(compound)), accuracy) for compound, coef in self.reagents.items()})
    product_masses = OrderedDict({compound: round(float(coef * equivalent * self.calculate_atomic_mass(compound)), accuracy) for compound, coef in self.products.items()})
    return (reagent_masses, product_masses)
