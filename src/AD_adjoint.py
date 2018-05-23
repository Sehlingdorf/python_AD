import math

TF_UNDEF = -1
TF_CONST = 0
TF_ASG = 1
TF_ADD = 2
TF_SUB = 3
TF_MUL = 4
TF_EXP = 5
TF_LOG = 6
TF_POW = 7
TF_SIN = 8
TF_COS = 9
#---------------------------------------------------------------------------------------#
class tape_entry:
  """Contains all data for one operation. Self representation is value."""
  def __init__(self):
    self.oc = TF_UNDEF # operation code
    self.arg1 = TF_UNDEF # First operation argument
    self.arg2 = TF_UNDEF # Second operation argument (optional)
    self.value = 0 
    self.adjoint = 0

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str(self.value)

#---------------------------------------------------------------------------------------#
# Initialize tape, list of tape entries
# Either a static tape size is given (delete all "tape.append(tape_entry())" from this file)
# or currently all the tape is dynamically getting bigger without user interaction.
global vac
vac = 0
tape_size = 1
tape = [tape_entry() for i in range(tape_size)]
#---------------------------------------------------------------------------------------#
class TFrev:
  """Tracer Float reverse (TFrev) is the used datatype for adjoint AD mode."""
  def __init__(self, value, is_input=False, from_operation=False):
    """Creation and initialization at once."""
    if is_input == True:
      #this ist the constructor (c++)
      global vac
      tape[vac].oc = TF_CONST
      tape[vac].value = value
      vac += 1
      tape.append(tape_entry())
      # this is the operator= overloading (c++)
      self.adress = vac
      self.value = value
      tape[vac].oc = TF_ASG
      tape[vac].value = value
      tape[vac].arg1 = vac - 1
      vac += 1
      tape.append(tape_entry())
      #return TFrev(value, False, True)

    if from_operation == True:
      vac += 1 # this is the increment of the operation 
      tape.append(tape_entry())
      self.value = value
      self.adress = vac
      tape[vac].oc = TF_ASG
      tape[vac].value = value
      tape[vac].arg1 = vac - 1
      #return self

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str(tape[self.adress].value)
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
      tape.append(tape_entry())
      return tmp
    else:
      tape[vac].oc = TF_CONST
      tape[vac].value = other
      vac += 1
      tape.append(tape_entry())
      tape[vac].oc = TF_ADD
      tape[vac].arg1 = self.adress
      tape[vac].arg2 = vac - 1
      tape[vac].value = self.value + other

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      tape.append(tape_entry())
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
      tape.append(tape_entry())
      return tmp
    else:
      tape[vac].oc = TF_CONST
      tape[vac].value = other
      vac += 1
      tape.append(tape_entry())
      tape[vac].oc = TF_MUL   
      tape[vac].arg1 = self.adress 
      tape[vac].arg2 = vac - 1 
      tape[vac].value = self.value * other

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      tape.append(tape_entry())
      return tmp

  def __rmul__(self, other):
    return self.__mul__(other)

  def __truediv__(self, other):
    if isinstance(other, TFrev):
      assert tape[other.adress].value != 0, "Division by zero."
    else:
      assert other != 0, "Division by zero."
    return self.__mul__(other ** (-1))

  def __rtruediv__(self, other):
    if isinstance(self, TFrev):
      assert tape[self.adress].value != 0, "Division by zero."
    else:
      assert self != 0, "Division by zero."
    return (self ** (-1)).__mul__(other)

  def __neg__(self):
    return self.__mul__(-1)

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
      tape.append(tape_entry())
      return tmp
    elif not isinstance(power, TFrev):
      tape[vac].oc = TF_CONST
      tape[vac].value = power
      vac += 1
      tape.append(tape_entry())
      tape[vac].oc = TF_POW
      tape[vac].arg1 = self.adress 
      tape[vac].arg2 = vac - 1 
      tape[vac].value = self.value ** power

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      tape.append(tape_entry())
      return tmp
    # other possibility is that 2(notTF) ** TF, that operation is curr not covered
    
  def exp(self):
    if isinstance(self, TFrev):
      global vac
      tape[vac].oc = TF_EXP  
      tape[vac].arg1 = self.adress 
      tape[vac].value = math.exp(self.value) 

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      tape.append(tape_entry())
      return tmp
    elif not isinstance(self, TFrev):
      return math.exp(self)

  def log(self):
    if isinstance(self, TFrev):
      assert self.value > 0, "log(x <= 0) is undefined." 
      global vac
      tape[vac].oc = TF_LOG 
      tape[vac].arg1 = self.adress 
      tape[vac].value = math.log(self.value) 

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      tape.append(tape_entry())
      return tmp
    elif not isinstance(self, TFrev):
      assert self.value > 0, "log(x <= 0) is undefined." 
      return math.log(self)

  def sin(self):
    if isinstance(self, TFrev):
      global vac
      tape[vac].oc = TF_SIN
      tape[vac].arg1 = self.adress 
      tape[vac].value = math.sin(self.value) 

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      tape.append(tape_entry())
      return tmp
    elif not isinstance(self, TFrev):
      return math.sin(self)

  def cos(self):
    #return TFrev.sin(self+math.pi/2)
    if isinstance(self, TFrev):
      global vac
      tape[vac].oc = TF_COS
      tape[vac].arg1 = self.adress 
      tape[vac].value = math.cos(self.value) 

      # every operation is treated as an assignement
      tmp = TFrev(tape[vac].value, from_operation=True)
      vac += 1 # this is the increment of the asignemnet
      tape.append(tape_entry())
      return tmp
    elif not isinstance(self, TFrev):
      return math.cos(self)

#---------------------------------------------------------------------------------------#
def interpret_tape():
    """Loop brackward through tape and evaluate derivatives."""
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
        
      elif tape[i].oc == TF_POW: # fails if tape[tape[i].arg1].value is negative
        tape[tape[i].arg1].adjoint += tape[tape[i].arg2].value * tape[tape[i].arg1].value ** (tape[tape[i].arg2].value-1) * tape[i].adjoint
        tape[tape[i].arg2].adjoint += tape[tape[i].arg1].value ** tape[tape[i].arg2].value * math.log(tape[tape[i].arg1].value) * tape[i].adjoint

      elif tape[i].oc == TF_EXP:
        tape[tape[i].arg1].adjoint += math.exp(tape[tape[i].arg1].value) * tape[i].adjoint

      elif tape[i].oc == TF_LOG:
        tape[tape[i].arg1].adjoint += 1/tape[tape[i].arg1].value * tape[i].adjoint

      elif tape[i].oc == TF_SIN:
        tape[tape[i].arg1].adjoint += math.cos(tape[tape[i].arg1].value) * tape[i].adjoint

      elif tape[i].oc == TF_COS:
        tape[tape[i].arg1].adjoint += -math.sin(tape[tape[i].arg1].value) * tape[i].adjoint

def reset_tape(): 
  """Resets complete tape to default values."""
  global vac
  vac = 0
  global tape_size
  global tape
  tape = [tape_entry() for i in range(tape_size)]

def get_gradient(input, output=None):
    """Reads the derivatives of an input vector (of TFrev) from interpreted tape.
    Sets seed at output if given, otherwise last tape entry is taken.
    Output needs to be a scalar TFrev."""
    if output==None:
      tape[vac-1].adjoint = 1
    else:
      assert isinstance(output, TFrev), "Only scalar objective Func is allowed for reverse AD-sweep."
      tape[output.adress].adjoint = 1
    interpret_tape()
    gradient = [tape[input_val.adress].adjoint for input_val in input]
    return gradient

def print_tape():
    """Prints tape in the current state."""
    print("tape:")
    global vac
    for i in range(vac):
      print(i, ": [ ", tape[i].oc, ", ", tape[i].arg1, ", ", tape[i].arg2, ", ", tape[i].value, ", ", tape[i].adjoint, " ]" )
#---------------------------------------------------------------------------------------#
if __name__ == '__main__':
  pass
