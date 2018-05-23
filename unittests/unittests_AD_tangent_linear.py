import unittest
import math
import numpy as np

import sys
sys.path.append('../src')
import AD_tangent_linear as AD

#---------------------------------------------------------------------------------------#
class TestsTangentlinearDerivatives_BaseOperations(unittest.TestCase):
  """Testing simple single operations."""

#---------------------------------------------------------------------------------------#
  def test_multiply(self):
    a = AD.TFfor(1);
    a.tangent = 1
    c = 2.0*a
    self.assertEqual(c.tangent,2.0)

#---------------------------------------------------------------------------------------#
  def test_logarithmic(self):
    a = AD.TFfor(2);
    a.tangent = 1
    c = AD.TFfor.log(a)
    self.assertEqual(c.tangent,0.5)

#---------------------------------------------------------------------------------------#
class TestsTangentlinearDerivatives_Functions(unittest.TestCase):
  """Testing mor complex compund operations with analytical (hard coded) derivatives."""

#---------------------------------------------------------------------------------------#
  def test_RootMeanSquare(self):
    """Root mean square"""
    def func(x,y):
      for val in x:
        y+=val**2
      return y**0.5
    n=3
    input = [AD.TFfor(1) for i in range(n)]
    gradient = []
    for i in range(n):
      input[i].tangent = 1
      output = 0.0
      gradient.append(func(input,output).tangent)
      input[i].tangent = 0
    
    analytical_solution = [1./3.**0.5, 1./3.**0.5, 1./3.**0.5]
    self.assertTrue(np.allclose(gradient, analytical_solution))

#---------------------------------------------------------------------------------------#
  def test_naumann_listing_2_2(self):
    """Square of sum of squares"""
    def func(x,y):
      for val in x:
        y+=val*val
      return y*y
    n=4
    input = [AD.TFfor(1) for i in range(n)]
    gradient = []
    for i in range(n):
      input[i].tangent = 1
      output = 0.0
      gradient.append(func(input,output).tangent)
      input[i].tangent = 0

    analytical_solution = [16, 16 ,16, 16]
    self.assertEqual(gradient, analytical_solution)

#---------------------------------------------------------------------------------------#
  def test_randomfunction1(self):
    """Random function with hard-coded derivative."""
    def func(x,y):
      a = AD.TFfor.sin(2*x[0]) + AD.TFfor.cos(3/x[1]) 
      b = -x[2]**2 
      c = 10
      d = -x[0]*x[1] + x[0]*x[1]*x[2]
      y = a + b + c + d
      return y
    n=3
    input = [AD.TFfor(1) for i in range(n)]
    gradient = []
    for i in range(n):
      input[i].tangent = 1
      output = 0.0
      gradient.append(func(input,output).tangent)
      input[i].tangent = 0

    [x0, x1, x2] = [input[0].value,input[1].value,input[2].value]
    analytical_solution = [2*math.cos(2*x0)-x1+x1*x2, -math.sin(3/x1)*(-3/x1**2)-x0+x0*x2, -2*x2 + x0*x1 ]
    self.assertTrue(np.allclose(gradient, analytical_solution))

#---------------------------------------------------------------------------------------#
if __name__ == '__main__':
  unittest.main()
