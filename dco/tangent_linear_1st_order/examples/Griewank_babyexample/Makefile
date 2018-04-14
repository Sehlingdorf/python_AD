CXX=g++
CXXFLAGS=-O3

binaries=main main_FD

all: $(binaries)

main: dco_t1s_type.cpp babyexample.cpp
	$(CXX) -o main dco_t1s_type.cpp babyexample.cpp

main_FD: babyexample_FD.cpp
	$(CXX) -o main_FD babyexample_FD.cpp

clean: 
	rm -f *.o $(binaries) 
