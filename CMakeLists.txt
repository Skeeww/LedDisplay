cmake_minimum_required(VERSION 3.30...4.0.2)

project(LEDDISPLAY
        VERSION 1.0.0
        DESCRIPTION "Software displaying usefull information on RGB LED Matrix"
        HOMEPAGE_URL "https://github.com/Skeeww/LedDisplay"
        LANGUAGES C CXX)

# RGB LED MATRIX LIB
add_library(rgbmatrix STATIC
        libs/rpi-rgb-led-matrix/lib/options-initialize.cc
        libs/rpi-rgb-led-matrix/lib/multiplex-mappers.cc
        libs/rpi-rgb-led-matrix/lib/hardware-mapping.c
        libs/rpi-rgb-led-matrix/lib/pixel-mapper.cc
        libs/rpi-rgb-led-matrix/lib/framebuffer.cc
        libs/rpi-rgb-led-matrix/lib/led-matrix.cc
        libs/rpi-rgb-led-matrix/lib/utf8-internal.h
        libs/rpi-rgb-led-matrix/lib/graphics.cc
        libs/rpi-rgb-led-matrix/lib/thread.cc
        libs/rpi-rgb-led-matrix/lib/gpio.cc
)
target_include_directories(rgbmatrix PUBLIC libs/rpi-rgb-led-matrix/include)
target_compile_features(rgbmatrix PUBLIC cxx_std_11)

# SPDLOG LIB
add_library(spdlog STATIC
        libs/spdlog/src/bundled_fmtlib_format.cpp
        libs/spdlog/src/stdout_sinks.cpp
        libs/spdlog/src/color_sinks.cpp
        libs/spdlog/src/file_sinks.cpp
        libs/spdlog/src/spdlog.cpp
        libs/spdlog/src/async.cpp
        libs/spdlog/src/cfg.cpp
)
target_include_directories(spdlog PUBLIC libs/spdlog/include)
target_compile_definitions(spdlog PUBLIC SPDLOG_COMPILED_LIB)
target_compile_features(spdlog PUBLIC cxx_std_11)

# BUILD EXECUTABLE
add_executable(main
        main.cpp
        screen.cpp
)
target_include_directories(main PUBLIC includes)
target_link_libraries(main PUBLIC rgbmatrix)
target_link_libraries(main PUBLIC spdlog)
