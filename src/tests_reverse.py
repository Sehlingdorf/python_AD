import AD_adjoint as AD

#---------------------------------------------------------------------------------------#
a = AD.TFrev(3, is_input=True)
b = AD.TFrev(10, is_input=True)
c = 2 ** a
print(AD.get_gradient([a,b]))
AD.print_tape()
AD.reset_tape()
