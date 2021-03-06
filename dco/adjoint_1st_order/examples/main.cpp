#include <iostream>
#include <math.h>
#include "dco_a1s_type.hpp"
using namespace std;

const int n=4;

extern dco_a1s_tape_entry dco_a1s_tape[DCO_A1S_TAPE_SIZE];

void f(dco_a1s_type *x, dco_a1s_type &y) {
  y=0;
  for (int i=0;i<n;i++){
    dco_a1s_type val;
    val = x[i]*x[i];
    y=y+val;
  }
  y=y*y;
}

int main() {

  dco_a1s_type x[n], y;
  for (int i=0;i<n;i++) {
    for (int j=0;j<n;j++) x[j]=1;
    f(x,y);
    if (i == 3) dco_a1s_print_tape();
    dco_a1s_tape[y.va].a=1;
    dco_a1s_interpret_tape();

    cout << i << "\t" << dco_a1s_tape[x[i].va].a << endl;
    
    dco_a1s_reset_tape();
  }
  
  dco_a1s_type a, c;
  a = 3;
  //b = 3;
  //c = 0
  dco_a1s_print_tape();
  c = a * 2;
  dco_a1s_print_tape();
  dco_a1s_tape[c.va].a = 1;
  dco_a1s_interpret_tape();
  dco_a1s_print_tape();
  cout << "dc/da = " << dco_a1s_tape[a.va].a << endl;
  //cout << "dc/db = " << dco_a1s_tape[b.va].a << endl;

  double g = 3;
  cout << pow(g,2.0) <<endl;

  return 0;
}
