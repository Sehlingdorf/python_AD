import unittest

import AD_adjoint

class TestsForReverseDerivatives(unittest.TestCase):
  def test_naumann_listing_2_2(self):
    def func(x,y):
      for val in x:
        y+=val*val
      return y*y
    n=4
    input = [AD_adjoint.TFrev(1, is_input=True) for i in range(n)]
    output = AD_adjoint.TFrev(0, is_input=True)
    func(input,output)
    gradient = AD_adjoint.get_gradient(input)
    analytical_solution = [16, 16, 16, 16]
    self.assertEqual(gradient, analytical_solution)

if __name__ == '__main__':
  unittest.main()
