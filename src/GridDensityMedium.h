#ifndef _GRIDDENSITYMEDIUM_H
#define _GRIDDENSITYMEDIUM_H

#include "medium.h"

namespace gnssro
{
	class GridDensityMedium: public medium
	{
		GridDensityMedium(int, int, int);
		~GridDensityMedium();
	};  // end class GridDensityMedium
}

#endif  // _GRIDDENSITYMEDIUM_H
