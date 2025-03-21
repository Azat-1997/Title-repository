from ChemCalcOOP import ReactionSolver
import unittest

class TestSolver(unittest.TestCase):
  REACTION_BALANCED = 'H2SO4 + 2KOH -> K2SO4 + 2H2O'
  REACTION_UNBALANCED = 'H2SO4 + KOH -> K2SO4 + H2O'
  solver = ReactionSolver.from_unbalanced_reaction(REACTION_UNBALANCED)
  
  # check static methods
  
  def test_take_coef(self):
    self.assertEqual(ReactionSolver._take_coef('10C3H8'), ('C3H8', 10))

  def test_take_coef_unit(self):
    self.assertEqual(ReactionSolver._take_coef('KOH'), ('KOH', 1))    

  def test_is_balanced_reaction_true(self):
    self.assertTrue(ReactionSolver._is_balanced_reaction(self.REACTION_BALANCED))
    
  def test_is_balanced_reaction_false(self):
    self.assertFalse(ReactionSolver._is_balanced_reaction(self.REACTION_UNBALANCED))
    
  def test_calculate_atomic_mass(self):
    self.assertEqual(ReactionSolver.calculate_atomic_mass('H2SO4'), 98.072)
    
  def test_calculate_mole(self):
    self.assertEqual(round(ReactionSolver.calculate_mole('H2O', 9), 3), 0.5)
    
  # check class methods  
  def test_creation_from_balanced(self):
    ReactionSolver.from_balanced_reaction(self.REACTION_BALANCED)
  
  def test_success_creation_from_unbalanced(self):
    ReactionSolver.from_unbalanced_reaction(self.REACTION_UNBALANCED)
  
  def test_failed_creation_from_unbalanced(self):
    with self.assertRaises(ValueError):
      ReactionSolver.from_unbalanced_reaction(self.REACTION_BALANCED)
      
  # check instance methods
  def test_calculate_ratio(self):
    ratio = self.solver._calculate_ratio({'KOH':2, 'H2SO4':1})
    self.assertLess(round(ratio['KOH'], 3) - 0.018, 0.001)
    self.assertLess(round(ratio['H2SO4'], 3) - 0.010, 0.001)
  
  def test_get_limiting_compound(self):
    self.assertEqual(self.solver.get_limiting_compound({'KOH':2, 'H2SO4':2}), 'KOH')
    self.assertEqual(self.solver.get_limiting_compound({'KOH':2, 'H2SO4':1}), 'H2SO4')
    self.assertEqual(self.solver.get_limiting_compound({'KOH':3}), 'KOH')
    self.assertEqual(self.solver.get_limiting_compound({'H2SO4':3}), 'H2SO4')
  
  def test_find_products_amount(self):
    reagents, products = self.solver.find_products_amount({'KOH':2, 'H2SO4':3}, accuracy=3)
    self.assertLess(reagents['KOH'] - 2.0, 0.001)
    self.assertLess(reagents['H2SO4'] - 1.748, 0.001)
    self.assertLess(products['K2SO4'] - 3.106, 0.001)
    self.assertLess(products['H2O'] - 0.642, 0.001)
    
    

  
if __name__=='__main__':
    unittest.main()
