add_executable( Test test.cpp )

add_executable( Test_Point test_point.cpp )

include_directories(../src)

find_library(libgnssro
	     NAMES libgnssro.a
		 )

target_link_libraries(Test
		              libgnssro
					  )

target_link_libraries(Test_Point
                      libgnssro
                      )
