#include <iostream>
using namespace std;
#include "dco_t1s_type.hpp"

const int n = 4;

void f(dco_t1s_type *x, dco_t1s_type &y) {
  y = 0;
  for (int i=0; i<n; i++) y=y+x[i]*x[i];
  y=y*y;
}

int main() {
  dco_t1s_type x[n], y;
  for (int i=0; i<n; i++) x[i]=1;
  for (int i=0; i<n; i++) {
    x[i].t=1;
    f(x,y);
    x[i].t=0;
    cout << y.t << endl;
  }

  return 0;
}
