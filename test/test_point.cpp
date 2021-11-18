#include<iostream>
#include "libgnssro.h"

int main()
{
  try
  {
	using namespace gnssro;
    //  Constructing various points:
    point<double,2> p1;
	point<double,2> p2(444.);
	point<double,2> p3(p2);
	point<double,2> p4;
    p2 += p3;
	p3 *= 2.;
	p4 = p2;
	const point<double,2> p5 = p2 + p3;
	std::cout << p2 << std::endl;
	std::cout << p2[0] << std::endl;
	std::cout << norm(p2) << std::endl;
  }
  catch( int ex )
  {
    return ex;
  }
  return 0;
}
