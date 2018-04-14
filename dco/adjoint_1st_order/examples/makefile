CPPC=g++ -O3

main : dco_a1s_type.o main.o
	$(CPPC) -o $@ $^

%.o : %.cpp
	$(CPPC) -c $<

clean :
	rm -f *.o main 

