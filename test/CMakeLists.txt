add_executable( Test test.cpp )

include_directories(../src)

find_library(libgnssro
	     NAMES libgnssro.a
		 )

target_link_libraries(Test
		              libgnssro
					  )
