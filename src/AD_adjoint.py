import math

TF_UNDEF = -1
TF_CONST = 0
TF_ASG = 1
TF_ADD = 2
TF_SUB = 3
TF_MUL = 4
TF_EXP = 5
TF_POW = 6
#---------------------------------------------------------------------------------------#
class tape_entry:
  def __init__(self):
    self.oc = TF_UNDEF
    self.arg1 = TF_UNDEF
    self.arg2 = TF_UNDEF
    self.value = 0
    self.adjoint = 0

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str(self.value)

#---------------------------------------------------------------------------------------#
global vac
vac = 0
tape_size = 100
tape = [tape_entry() for i in range(tape_size)]
#---------------------------------------------------------------------------------------#
class TFrev:
  def __init__(self, value, is_input=False, from_operation=False):
    """Creation and initialization at once."""
    if is_input == True:
      #this ist the constructor (c++)
      global vac
      tape[vac].oc = TF_CONST
      tape[vac].value = value
      vac += 1
      # this is the operator= overloading (c++)
      self.adress = vac
      self.value = value
      tape[vac].oc = TF_ASG
      tape[vac].value = value
      tape[vac].arg1 = vac - 1
      vac += 1
      #return TFrev(value, False, True)

    if from_operation == True:
      vac += 1 # this is the increment of the operation 
      self.value = value
      self.adress = vac
      tape[vac].oc = TF_ASG
      tape[vac].value = value
      tape[vac].arg1 = vac - 1
      #return self

#---------------------------------------------------------------------------------------#
  def __add__(self, other):   
    if isinstance(other, TFrev):
      global vac
      tape[vac].oc = TF_ADD
      tape[vac].arg1 = self.adress
      tape[vac].arg2 = other.adress
      tape[vac].value = self.value + other.value

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      return tmp
    else:
      tape[vac].oc = TF_CONST
      tape[vac].value = other
      vac += 1
      tape[vac].oc = TF_ADD
      tape[vac].arg1 = self.adress
      tape[vac].arg2 = vac - 1
      tape[vac].value = self.value + other

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      return tmp
  
  def __radd__(self, other):
    return self.__add__(other)

  def __sub__(self, other):
    return self.__add__(other * -1)

  def __rsub__(self, other):
    return (self * -1).__add__(other)

  def __mul__(self, other):
    if isinstance(other, TFrev):
      global vac
      tape[vac].oc = TF_MUL   
      tape[vac].arg1 = self.adress 
      tape[vac].arg2 = other.adress 
      tape[vac].value = self.value * other.value

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      return tmp
    else:
      tape[vac].oc = TF_CONST
      tape[vac].value = other
      vac += 1
      tape[vac].oc = TF_MUL   
      tape[vac].arg1 = self.adress 
      tape[vac].arg2 = vac - 1 
      tape[vac].value = self.value * other

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      return tmp

  def __rmul__(self, other):
    return self.__mul__(other)

  def __truediv__(self, other):
    return self.__mul__(other ** (-1))

  def __rtruediv__(self, other):
    return (self ** (-1)).__mul__(other)

  def __pow__(self, power):
    if isinstance(power, TFrev):
      global vac
      tape[vac].oc = TF_POW   
      tape[vac].arg1 = self.adress 
      tape[vac].arg2 = power.adress 
      tape[vac].value = self.value ** power.value

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      return tmp
    else:
      tape[vac].oc = TF_CONST
      tape[vac].value = power
      vac += 1
      tape[vac].oc = TF_POW
      tape[vac].arg1 = self.adress 
      tape[vac].arg2 = vac - 1 
      tape[vac].value = self.value ** power

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      return tmp
    
#---------------------------------------------------------------------------------------#
def interpret_tape():
    """docstring."""
    global vac
    for i in range(vac,-1,-1): # reversed array
      if tape[i].oc == TF_ASG:
        tape[tape[i].arg1].adjoint += tape[i].adjoint

      elif tape[i].oc == TF_ADD:
        tape[tape[i].arg1].adjoint += tape[i].adjoint
        tape[tape[i].arg2].adjoint += tape[i].adjoint

      elif tape[i].oc == TF_SUB: # everything is currently piped to ADD
        tape[tape[i].arg1].adjoint += tape[i].adjoint
        tape[tape[i].arg2].adjoint -= tape[i].adjoint

      elif tape[i].oc == TF_MUL:
        tape[tape[i].arg1].adjoint += tape[tape[i].arg2].value * tape[i].adjoint
        tape[tape[i].arg2].adjoint += tape[tape[i].arg1].value * tape[i].adjoint
        
      elif tape[i].oc == TF_POW:
        # c=a^b - dc/da
        tape[tape[i].arg1].adjoint += tape[tape[i].arg2].value * tape[tape[i].arg1].value ** (tape[tape[i].arg2].value-1) * tape[i].adjoint
        # c=a^b - dc/db
        tape[tape[i].arg2].adjoint += tape[tape[i].arg1].value ** tape[tape[i].arg2].value * math.log(tape[tape[i].arg2].value) * tape[i].adjoint

      elif tape[i].oc == TF_EXP:
        pass

def reset_tape(): 
  global vac
  vac = 0
  global tape_size
  tape = [tape_entry() for i in range(tape_size)]

def get_gradient(input, output=None):
    tape[vac-1].adjoint = 1
    interpret_tape()
    gradient = [tape[input_val.adress].adjoint for input_val in input]
    return gradient
  
def print_tape():
    print("tape:")
    global vac
    for i in range(vac):
      print(i, ": [ ", tape[i].oc, ", ", tape[i].arg1, ", ", tape[i].arg2, ", ", tape[i].value, ", ", tape[i].adjoint, " ]" )
#---------------------------------------------------------------------------------------#
if __name__ == '__main__':
  if 1==1:
    a = TFrev(2, is_input=True)
    b = TFrev(1, is_input=True)
    c = a + b 
    print_tape()
    reset_tape()
    print_tape()

###Naumann example
  if 1==1:
    def func(x, y):
      for val in x:
        tmp = val*val
        y = y + tmp
      return y * y
    
    def func2(x,y):
      for val in x:
        y += val*val
      return y * y
    n = 4

    a = [TFrev(1, is_input=True) for i in range(n)]    
    y = TFrev(0, is_input=True)
    print(y.adress)
    #print_tape()
    func(a, y)
    print_tape()
    print(a[1].adress)
    print_tape()
    print(get_gradient(a))  




