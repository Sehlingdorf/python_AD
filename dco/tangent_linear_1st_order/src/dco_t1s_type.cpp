#include <cmath>
using namespace std;
#include "dcp_t1s_type.hpp"

dco_t1s_type::dco_t1s_type(const double& x): v(x), t(0) {};
dco_t1s_type::dco_t1s_type(): v(0), t(0) {};

dco_t1s_type& dco_t1s_type::operator=(const dco_t1s_type& x) {
  if (this==&x) return *this;
  v=x.v;
  t=x.t;
  return *this;
}


dco_t1s_type operator*(const dco_t1s_type& x1, const dco_t1s_type& x2) {
  dco_t1s_type tmp;
  tmp.v=x1.v*x2.v;
  tmp.t=x1.t*x2.v + x1.v*x2.t;
  return tmp;
}

dco_t1s_type operator+(const dco_t1s_type& x1, const dco_t1s_type& x2) {
  dco_t1s_type tmp;
  tmp.v=x1.v+x2.v;
  tmp.t=x1.t+x2.t;
  return tmp;
}  

dco_t1s_type operator-(const dco_t1s_type& x1, const dco_t1s_type& x2) {
  dco_t1s_type tmp;
  tmp.v=x1.v-x2.v;
  tmp.t=x1.t-x2.t;
  return tmp;
}  

dco_t1s_type operator sin(const dco_t1s_type& x) {
  dco_t1s_type tmp;
  tmp.v=sin(x.v);
  tmp.t=cos(x.v)*x.t;
  return tmp;
}  

dco_t1s_type operator cos(const dco_t1s_type& x) {
  dco_t1s_type tmp;
  tmp.v=cos(x.v);
  tmp.t=-sin(x.v)*x.t;
  return tmp;
}
  
dco_t1s_type operator exp(const dco_t1s_type& x) {
  dco_t1s_type tmp;
  tmp.v=exp(x.v);
  tmp.t=tmp.v*x.t;
  return tmp;
}  
