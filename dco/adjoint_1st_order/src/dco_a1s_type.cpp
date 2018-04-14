#include <cmath>
#include <iostream>
using namespace std;
#include "dco_a1s_type.hpp"

static int dco_a1s_vac=0; 
dco_a1s_tape_entry dco_a1s_tape[DCO_A1S_TAPE_SIZE];

dco_a1s_type::dco_a1s_type(const double& x): v(x) { 
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_CONST; 
  dco_a1s_tape[dco_a1s_vac].v=x; 
  va=dco_a1s_vac++;
};

dco_a1s_type& dco_a1s_type::operator=(const dco_a1s_type& x) {
  if (this==&x) return *this;
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_ASG; 
  dco_a1s_tape[dco_a1s_vac].v=v=x.v;
  dco_a1s_tape[dco_a1s_vac].arg1=x.va;
  va=dco_a1s_vac++;
  return *this;
}

dco_a1s_type operator*(const dco_a1s_type& x1, const dco_a1s_type& x2) {
  dco_a1s_type tmp;
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_MUL; 
  dco_a1s_tape[dco_a1s_vac].arg1=x1.va; 
  dco_a1s_tape[dco_a1s_vac].arg2=x2.va; 
  dco_a1s_tape[dco_a1s_vac].v=tmp.v=x1.v*x2.v; 
  tmp.va=dco_a1s_vac++;
  return tmp;
}

dco_a1s_type operator+(const dco_a1s_type& x1, const dco_a1s_type& x2) {
  dco_a1s_type tmp;
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_ADD; 
  dco_a1s_tape[dco_a1s_vac].arg1=x1.va; 
  dco_a1s_tape[dco_a1s_vac].arg2=x2.va; 
  dco_a1s_tape[dco_a1s_vac].v=tmp.v=x1.v+x2.v; 
  tmp.va=dco_a1s_vac++;
  return tmp;
}

dco_a1s_type operator-(const dco_a1s_type& x1, const dco_a1s_type& x2) {
  dco_a1s_type tmp;
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_SUB; 
  dco_a1s_tape[dco_a1s_vac].arg1=x1.va; 
  dco_a1s_tape[dco_a1s_vac].arg2=x2.va; 
  dco_a1s_tape[dco_a1s_vac].v=tmp.v=x1.v-x2.v; 
  tmp.va=dco_a1s_vac++;
  return tmp;
}

dco_a1s_type sin(const dco_a1s_type& x) {
  dco_a1s_type tmp;
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_SIN; 
  dco_a1s_tape[dco_a1s_vac].arg1=x.va; 
  dco_a1s_tape[dco_a1s_vac].v=tmp.v=sin(x.v); 
  tmp.va=dco_a1s_vac++;
  return tmp;
}

dco_a1s_type cos(const dco_a1s_type& x) {
  dco_a1s_type tmp;
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_COS; 
  dco_a1s_tape[dco_a1s_vac].arg1=x.va; 
  dco_a1s_tape[dco_a1s_vac].v=tmp.v=cos(x.v); 
  tmp.va=dco_a1s_vac++;
  return tmp;
}

dco_a1s_type exp(const dco_a1s_type& x) {
  dco_a1s_type tmp;
  dco_a1s_tape[dco_a1s_vac].oc=DCO_A1S_EXP; 
  dco_a1s_tape[dco_a1s_vac].arg1=x.va; 
  dco_a1s_tape[dco_a1s_vac].v=tmp.v=exp(x.v); 
  tmp.va=dco_a1s_vac++;
  return tmp;
}

void dco_a1s_print_tape () {
  cout << "tape:" << endl;
  for (int i=0;i<dco_a1s_vac;i++)
    cout << i << ": [ " << dco_a1s_tape[i].oc << ", "
         << dco_a1s_tape[i].arg1 << ", "
         << dco_a1s_tape[i].arg2 << ", "
         << dco_a1s_tape[i].v << ", "
         << dco_a1s_tape[i].a << " ]" << endl;
}

void dco_a1s_reset_tape () {
  for (int i=0;i<dco_a1s_vac;i++)
    dco_a1s_tape[i].a=0;
  dco_a1s_vac=0;
}

void dco_a1s_interpret_tape () {
  for (int i=dco_a1s_vac;i>=0;i--) {
    switch (dco_a1s_tape[i].oc) {
      case DCO_A1S_ASG : {
        dco_a1s_tape[dco_a1s_tape[i].arg1].a+=dco_a1s_tape[i].a;
        break;
      }
      case DCO_A1S_ADD : {
        dco_a1s_tape[dco_a1s_tape[i].arg1].a+=dco_a1s_tape[i].a;
        dco_a1s_tape[dco_a1s_tape[i].arg2].a+=dco_a1s_tape[i].a;
        break;
      }
      case DCO_A1S_SUB : {
        dco_a1s_tape[dco_a1s_tape[i].arg1].a+=dco_a1s_tape[i].a;
        dco_a1s_tape[dco_a1s_tape[i].arg2].a-=dco_a1s_tape[i].a;
        break;
      }
      case DCO_A1S_MUL : {
        dco_a1s_tape[dco_a1s_tape[i].arg1].a+=dco_a1s_tape[dco_a1s_tape[i].arg2].v*dco_a1s_tape[i].a;
        dco_a1s_tape[dco_a1s_tape[i].arg2].a+=dco_a1s_tape[dco_a1s_tape[i].arg1].v*dco_a1s_tape[i].a;
        break;
      }
      case DCO_A1S_SIN : {
        dco_a1s_tape[dco_a1s_tape[i].arg1].a+=cos(dco_a1s_tape[dco_a1s_tape[i].arg1].v)*dco_a1s_tape[i].a;
        break;
      }
      case DCO_A1S_COS : {
        dco_a1s_tape[dco_a1s_tape[i].arg1].a-=sin(dco_a1s_tape[dco_a1s_tape[i].arg1].v)*dco_a1s_tape[i].a;
        break;
      }
      case DCO_A1S_EXP : {
        dco_a1s_tape[dco_a1s_tape[i].arg1].a+=dco_a1s_tape[i].v*dco_a1s_tape[i].a;
        break;
      }
    }
  }
}
    
