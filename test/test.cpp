#include "libgnssro.h"
#include <assert.h>
#include <iostream>

int main()
{
	Planck myplanck(6.626070e-34,1.380649e-23);
	float R = myplanck(15000.,293.15);
	std::cout << R << std::endl;
	assert(R == R);
}
