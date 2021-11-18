add_library(libgnssro STATIC
	medium.h
	GridDensityMedium.h
	GridDensityMedium.cpp
	libgnssro.cpp
         libgnssro.h
	Point.hpp
)

set_target_properties(libgnssro PROPERTIES VERSION ${PROJECT_VERSION})

set_target_properties(libgnssro PROPERTIES PUBLIC_HEADER libgnssro.h)

target_include_directories(libgnssro PRIVATE src)

install(TARGETS libgnssro
	ARCHIVE DESTINATION lib/static
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
