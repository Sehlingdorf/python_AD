import math

#---------------------------------------------------------------------------------------#
class TracerFloat:
  def __init__(self, value):
    self.value = value  
    self.tangent = 0

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str(self.value)
#---------------------------------------------------------------------------------------#
  def __add__(self, other):
    tmp = TracerFloat(None)
    if isinstance(other, TracerFloat):
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
    tmp = TracerFloat(None)
    if isinstance(other, TracerFloat):
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
    tmp = TracerFloat(None)
    if isinstance(power, TracerFloat):
      tmp.value = self.value ** power.value
      tmp.tangent = power.tangent*math.log(self.value)*self.value**power.value + power.value*self.tangent*self.value**(power.value-1)
      return tmp
    else:
      tmp.value = self.value ** power
      tmp.tangent = power * self.value ** (power-1) * self.tangent
      return tmp
      
  def sin(self):
    tmp = TracerFloat(None)
    tmp.value = math.sin(self.value)
    tmp.tangent = math.cos(self.value) * self.tangent
    return tmp

  def exp(self):
    tmp = TracerFloat(None)
    tmp.value = math.exp(self.value)
    tmp.tangent = math.exp(self.value) * self.tangent
    return tmp 
#---------------------------------------------------------------------------------------#
if __name__ == '__main__':
  a = TracerFloat(2)
  b = TracerFloat(3)
  p = TracerFloat(2)

  a.tangent = 1

  c = (a**p)*b+2
  print(c.value, c.tangent)
  ###
  a = TracerFloat(0)
  a.tangent = 1

  b = TracerFloat.exp(a)
  print(b.value, b.tangent)
  ###
  a = TracerFloat(2)
  c = TracerFloat(3)
  a.tangent = 1
  b = a**c
  print(b.value, b.tangent)
  ###
  a  = TracerFloat(2)
  a.tangent = 1
  c = a/3
  print(c.value, c.tangent)
  ###
  a  = TracerFloat(2)
  a.tangent = 1
  c = 3/a
  print(c.value, c.tangent)
