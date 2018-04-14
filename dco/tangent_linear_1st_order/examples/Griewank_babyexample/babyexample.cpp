#include <iostream>
using namespace std;
#include "dco_t1s_type.hpp"

const int n = 2;

void f(dco_t1s_type *x, dco_t1s_type &y) {
  y = 0;
  y = ( sin(x[0]/x[1]) + x[0]/x[1] - exp(x[1])) * (x[0]/x[1] - exp(x[1]));
}

void test(dco_t1s_type &x, dco_t1s_type &y) {
  y=0;
  y=(x+3)/x;
}

int main() {
  dco_t1s_type x[n], y;
  x[0].v = 1.5;
  x[1].v = 0.5;
  for (int i=0; i<n; i++) {
    x[i].t=1;
    cout << x[0].t << "  " << x[1].t << endl;
    cout << x[0].v << "  " << x[1].v << endl;
    f(x,y);
    x[i].t=0;
    cout << y.t << endl;
  }
  cout << y.v << endl;

  return 0;
}
