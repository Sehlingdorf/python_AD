import math

#---------------------------------------------------------------------------------------#
class TFfor:
  """Tracer Float forward."""

  def __init__(self, value):
    self.value = value  
    self.tangent = 0

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str(self.value)
#---------------------------------------------------------------------------------------#
  def __add__(self, other):
    tmp = TFfor(None)
    if isinstance(other, TFfor):
      tmp.value = self.value + other.value
      tmp.tangent = self.tangent + other.tangent
      return tmp
    else:
      tmp.value = self.value + other
      tmp.tangent = self.tangent
      return tmp

  def __radd__(self, other):
    return self.__add__(other)

  def __sub__(self, other):
    return self.__add__(other * (-1))
  
  def __rsub__(self, other):
    return (self * (-1)).__add__(other)

#---------------------------------------------------------------------------------------#
  def __mul__(self, other):
    tmp = TFfor(None)
    if isinstance(other, TFfor):
      tmp.value = self.value * other.value
      tmp.tangent = self.tangent * other.value + self.value * other.tangent
      return tmp
    else:
      tmp.value = self.value * other
      tmp.tangent = self.tangent * other
      return tmp
  
  def __rmul__(self, other):
    return self.__mul__(other)

  def __truediv__(self, other):
    return self.__mul__(other ** (-1))

  def __rtruediv__(self, other):
    return (self ** (-1)).__mul__(other)

  def __neg__(self):
    return self.__mul__(-1)

  def __pow__(self, power):
    """d/dx f(x)^g(x) = g'*ln(f)*f^g + g*f'*f^(g-1)""" 
    tmp = TFfor(None)
    if isinstance(power, TFfor):
      tmp.value = self.value ** power.value
      tmp.tangent = power.tangent*math.log(self.value)*self.value**power.value + power.value*self.tangent*self.value**(power.value-1)
      return tmp
    else:
      tmp.value = self.value ** power
      tmp.tangent = power * self.value ** (power-1) * self.tangent
      return tmp
      
  def sin(self):
    tmp = TFfor(None)
    tmp.value = math.sin(self.value)
    tmp.tangent = math.cos(self.value) * self.tangent
    return tmp

  def cos(self):
    tmp = TFfor(None)
    tmp.value = math.cos(self.value)
    tmp.tangent = -math.sin(self.value) * self.tangent
    return tmp

  def exp(self):
    tmp = TFfor(None)
    tmp.value = math.exp(self.value)
    tmp.tangent = math.exp(self.value) * self.tangent
    return tmp 

  def log(self):
    
    tmp = TFfor(None)
    tmp.value = math.log(self.value)
    tmp.tangent = 1/self.value * self.tangent
    return tmp 
    
#---------------------------------------------------------------------------------------#
if __name__ == '__main__':
  pass
