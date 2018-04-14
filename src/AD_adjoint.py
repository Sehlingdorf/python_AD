
TF_UNDEF = -1
TF_CONST = 0
TF_ASG = 1
TF_ADD = 2
TF_SUB = 3
TF_MUL = 4
TF_EXP = 5
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
tape_size = 1000000*10
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
    global vac
    tape[vac].oc = TF_ADD
    tape[vac].arg1 = self.adress
    tape[vac].arg2 = other.adress
    tape[vac].value = self.value + other.value

    # every operation is treated as an assignement
    tmp = TFrev(tape[vac].value, from_operation=True)
    vac += 1 # this is the increment of the asignemnet
    return tmp

  def __sub__(self, other):
    pass

  def __mul__(self, other):
    global vac
    tape[vac].oc = TF_MUL   
    tape[vac].arg1 = self.adress 
    tape[vac].arg2 = other.adress 
    tape[vac].value = self.value * other.value

    # every operation is treated as an assignement
    tmp = TFrev(tape[vac].value, from_operation=True)
    vac += 1 # this is the increment of the asignemnet
    return tmp

  def exp(self):
    pass
#---------------------------------------------------------------------------------------#
def print_tape():
    print("tape:")
    global vac
    for i in range(vac):
      print(i, ": [ ", tape[i].oc, ", ", tape[i].arg1, ", ", tape[i].arg2, ", ", tape[i].value, ", ", tape[i].adjoint, " ]" )
    
def interpret_tape():
    """docstring."""
    global vac
    for i in range(vac,-1,-1): # reversed array
      if tape[i].oc == TF_ASG:
        tape[tape[i].arg1].adjoint += tape[i].adjoint

      elif tape[i].oc == TF_ADD:
        tape[tape[i].arg1].adjoint += tape[i].adjoint
        tape[tape[i].arg2].adjoint += tape[i].adjoint

      elif tape[i].oc == TF_SUB:
        pass

      elif tape[i].oc == TF_MUL:
        tape[tape[i].arg1].adjoint += tape[tape[i].arg2].value * tape[i].adjoint
        tape[tape[i].arg2].adjoint += tape[tape[i].arg1].value * tape[i].adjoint
        
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
    n = 1000000

    a = [TFrev(1, is_input=True) for i in range(n)]    
    y = TFrev(0, is_input=True)
    print(y.adress)
    #print_tape()
    func(a, y)
    print_tape()
    print(a[1].adress)
    print_tape()
    print(get_gradient(a))  
