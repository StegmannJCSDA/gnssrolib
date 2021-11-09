#ifndef _MEDIUM_H
#define _MEDIUM_H

#include<iostream>

namespace gnssro
{
	class media
	{
		public:
			std::string class_name;
			virtual ~media() = 0;
	}
}

#endif  // _MEDIUM_H
