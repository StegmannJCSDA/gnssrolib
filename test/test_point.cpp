#include<iostream>
#include "libgnssro.h"

int main()
{
  try
  {
    using namespace gnssro;
    //  Constructing various points:
    point<double,3> p1;
    point<double,3> p2(2.0);
    p1 = p2 + p2;
    point<double,3> p4;
    p4 = 2.0*p2;
    std::cout << p2 << std::endl;
    const point<double,3> p5 = p2 - p1;
  }
  catch( int ex )
  {
    return ex;
  }
  return 0;
}
