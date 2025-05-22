#ifndef SCREEN_H
#define SCREEN_H

#include <cassert>
#include <thread>
#include <string>
#include <memory>

#include "../libs/spdlog/include/spdlog/spdlog.h"
#include "../libs/rpi-rgb-led-matrix/include/led-matrix.h"
#include "../libs/rpi-rgb-led-matrix/include/graphics.h"


class Screen
{
private:
    bool _active;
    bool _displayed;
    float _refreshRate;
    std::shared_ptr<rgb_matrix::RGBMatrix> _matrix;
    std::thread _thread;
    rgb_matrix::Font _darkModeHourFont;

    void update();

protected:
    void process();

public:
    std::string name;
    bool darkMode;

    Screen(std::string name, std::shared_ptr<rgb_matrix::RGBMatrix> matrix);
    ~Screen();
    void start();
    void stop();
};
#endif