#ifndef DCO_T1S_INCLUDED_
#define DCO_T1S_INCLUDED_

  class dco_t1s_type {
    public :
      double v; double t;
      dco_t1s_type(const double&);
      dco_t1s_type();
      dco_t1s_type& operator=(const dco_t1s_type&);
  };

  dco_t1s_type operator*(const dco_t1s_type&, const dco_t1s_type&);
  dco_t1s_type operator+(const dco_t1s_type&, const dco_t1s_type&);
  dco_t1s_type operator-(const dco_t1s_type&, const dco_t1s_type&);

  dco_t1s_type operator sin(const dco_t1s_type&);
  dco_t1s_type operator cos(const dco_t1s_type&);
  dco_t1s_type operator exp(const dco_t1s_type&);
#endif
