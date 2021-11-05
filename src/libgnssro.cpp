#include <math.h>       /* exp */
#include "libgnssro.h"

Planck::Planck(float a, float b) : h(a), kB(b) {};

Planck::~Planck(){};

float Planck::operator()(float nu, float T)
{
	return 2.0*h*nu/(299792458.0*299792458)
		/( exp(h*nu/kB*T) - 1.0);
};
