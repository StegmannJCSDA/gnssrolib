#ifndef _MEDIA_H
#define _MEDIA_H

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

#endif  // _MEDIA_H
