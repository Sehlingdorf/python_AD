#include <iostream>
#include <cmath>
using namespace std;

const int n = 2;


double f_mod(double *x) {
  double y = 0;
  y = ( sin(x[0] / x[1]) + x[0] / x[1] - exp(x[1]));
  y = y * (x[0] / x[1] - exp(x[1]));
  return y;
}

double central_diff(double *x) {
   // FD step size
   double h = 1e-3;
   double c_FD = 0;
   // xp -> x plus, x -> x minus
   double xp[n], xm[n], yp, ym;
   xp[0]=x[0] ; xp[1]=x[1]+h; 
   xm[0]=x[0] ; xm[1]=x[1]-h; 

   c_FD = ( f_mod(xp)- f_mod(xm) ) / (2*h);
   return c_FD;
}

int main() {

  // FD calculation
  double x[n];
  x[0]=1.5; x[1]=0.5;
  cout  << central_diff(x) << endl;

  return 0;
}
