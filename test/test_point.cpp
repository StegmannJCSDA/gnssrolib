#include<iostream>
#include "libgnssro.h"

int main()
{
  try
  {
    //  Constructing various points:
    gnssro::Point<double,2> p1;
	gnssro::Point<double,2> p2(444.);
	gnssro::Point<double,2> p3(p2);
	gnssro::Point<double,2> p4;
    p2 += p3;
	p3 *= 2.;
	p4 = p2;
	//const gnssro::Point<double> p5 = p2 + p3;
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
