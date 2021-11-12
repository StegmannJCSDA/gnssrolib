#ifndef _MEDIUM_H
#define _MEDIUM_H

#include<iostream>

namespace gnssro
{
	class medium
	{
		public:
			std::string class_name;
			virtual ~medium() = 0;
	};
}

#endif  // _MEDIUM_H
