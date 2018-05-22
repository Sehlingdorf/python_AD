import AD_adjoint as AD

#---------------------------------------------------------------------------------------#
if 0==1:
  a = AD.TFrev(3, is_input=True)
  b = AD.TFrev(2, is_input=True)
  c = 2 / a
  AD.print_tape()
  print(AD.get_gradient([a,b]))
  AD.print_tape()
  AD.reset_tape()

if 1==1:
  a = AD.TFrev(2, is_input=True)
  b = AD.TFrev(1, is_input=True)
  c = AD.TFrev(1, is_input=True)

  d = (a**2 + b**2 + c**2)**0.5

  AD.print_tape()
  print(AD.get_gradient([a,b]))
  AD.print_tape()
  AD.reset_tape()
