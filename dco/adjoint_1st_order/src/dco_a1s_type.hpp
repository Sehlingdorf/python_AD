#ifndef DCO_A1S_INCLUDED_
  #define DCO_A1S_INCLUDED_
  #define DCO_A1S_TAPE_SIZE 1000000

  #define DCO_A1S_UNDEF -1
  #define DCO_A1S_CONST 0
  #define DCO_A1S_ASG 1
  #define DCO_A1S_ADD 2
  #define DCO_A1S_SUB 3
  #define DCO_A1S_MUL 4
  #define DCO_A1S_SIN 5
  #define DCO_A1S_COS 6
  #define DCO_A1S_EXP 7

  class dco_a1s_tape_entry {
    public:
      int oc;
      int arg1;
      int arg2;
      double v;
      double a;
      dco_a1s_tape_entry() : oc(DCO_A1S_UNDEF), arg1(DCO_A1S_UNDEF), arg2(DCO_A1S_UNDEF), v(0), a(0) {};
  };

  class dco_a1s_type {
    public:
      int va;
      double v;
      dco_a1s_type() : va(DCO_A1S_UNDEF), v(0) {};
      dco_a1s_type(const double&);
      dco_a1s_type& operator=(const dco_a1s_type&);
  };

  dco_a1s_type operator*(const dco_a1s_type&, const dco_a1s_type&);
  dco_a1s_type operator+(const dco_a1s_type&, const dco_a1s_type&);
  dco_a1s_type operator-(const dco_a1s_type&, const dco_a1s_type&);
  dco_a1s_type sin(const dco_a1s_type&);
  dco_a1s_type exp(const dco_a1s_type&);
  void dco_a1s_print_tape();
  void dco_a1s_interpret_tape();
  void dco_a1s_reset_tape();

#endif
