import unittest
import numpy as np
import math

import sys
sys.path.append('../src')
import AD_adjoint as AD

#---------------------------------------------------------------------------------------#
class TestsReverseDerivatives_BaseOperations(unittest.TestCase):
  """Testing simple single operations."""

#---------------------------------------------------------------------------------------#
  def test_division(self):
    """Division"""
    AD.reset_tape()
        
    a = AD.TFrev(1, is_input=True)
    b = AD.TFrev(2, is_input=True)
    c = 2 / a
    d = c # additional test of assignment, nothing is added to tape though due to python 
    gradient =  AD.get_gradient([a,b],d)
    analytical_solution = [-2,0]

    self.assertEqual(gradient, analytical_solution)

#---------------------------------------------------------------------------------------#
  def test_exponential(self):
    """Exponential function"""
    AD.reset_tape()
        
    a = AD.TFrev(0, is_input=True)
    b = AD.TFrev.exp(a)
    gradient =  AD.get_gradient([a],b)
    analytical_solution = [1.]

    self.assertEqual(gradient, analytical_solution)

#---------------------------------------------------------------------------------------#
  def test_logarthmic(self):
    """Logarthmic Function"""
    AD.reset_tape()
        
    a = AD.TFrev(1, is_input=True)
    b = AD.TFrev.log(a)
    gradient =  AD.get_gradient([a],b)
    analytical_solution = [1.]

    self.assertEqual(gradient, analytical_solution)

#---------------------------------------------------------------------------------------#
  def test_sinus(self):
    """Sinus"""
    AD.reset_tape()
        
    a = AD.TFrev(0, is_input=True)
    b = AD.TFrev.sin(a)
    gradient =  AD.get_gradient([a],b)
    analytical_solution = [1.]

    self.assertEqual(gradient, analytical_solution)

#---------------------------------------------------------------------------------------#
  def test_cosinus(self):
    """Cosinus"""
    AD.reset_tape()
        
    a = AD.TFrev(math.pi/2, is_input=True)
    b = AD.TFrev.cos(a)
    gradient =  AD.get_gradient([a],b)
    analytical_solution = [-1.]

    self.assertEqual(gradient, analytical_solution)

#---------------------------------------------------------------------------------------#
class TestsReverseDerivatives_Functions(unittest.TestCase):
  """Testing mor complex compund operations with analytical (hard coded) derivatives."""

#---------------------------------------------------------------------------------------#
  def test_RootMeanSquare(self):
    """Root mean square"""
    AD.reset_tape()
    def func(x,y):
      for val in x:
        y+=val**2
      return y**0.5
    n=3
    input = [AD.TFrev(1, is_input=True) for i in range(n)]
    output = AD.TFrev(0, is_input=True)
    func(input,output)
    gradient = AD.get_gradient(input)
    analytical_solution = [1./3.**0.5, 1./3.**0.5, 1./3.**0.5]
    self.assertTrue(np.allclose(gradient, analytical_solution))

#---------------------------------------------------------------------------------------#
  def test_naumann_listing_2_2(self):
    """Square of sum of squares"""
    AD.reset_tape()
    def func(x,y):
      for val in x:
        y+=val*val
      return y*y  
    n=4
    input = [AD.TFrev(1, is_input=True) for i in range(n)]
    output = AD.TFrev(0, is_input=True)
    func(input,output)
    gradient = AD.get_gradient(input)
    analytical_solution = [16, 16, 16, 16]
    self.assertEqual(gradient, analytical_solution)

#---------------------------------------------------------------------------------------#
  def test_randomfunction1(self):
    """Random function with hard-coded derivative."""
    AD.reset_tape()
    def func(x,y):
      a = AD.TFrev.sin(2*x[0]) + AD.TFrev.cos(3/x[1]) 
      b = -x[2]**2 
      c = 10
      d = -x[0]*x[1] + x[0]*x[1]*x[2]
      y = a + b + c + d
      return y
    n=3
    input = [AD.TFrev(1, is_input=True) for i in range(n)]
    output = AD.TFrev(0, is_input=True)
    func(input,output)
    gradient = AD.get_gradient(input)
    [x0, x1, x2] = [AD.tape[input[0].adress].value,AD.tape[input[1].adress].value,AD.tape[input[2].adress].value]
    analytical_solution = [2*math.cos(2*x0)-x1+x1*x2, -math.sin(3/x1)*(-3/x1**2)-x0+x0*x2, -2*x2 + x0*x1 ]
    self.assertTrue(np.allclose(gradient, analytical_solution))
#---------------------------------------------------------------------------------------#
if __name__ == '__main__':
  unittest.main()
