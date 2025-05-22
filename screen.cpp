#include "includes/screen.h"

Screen::Screen(std::string name, std::shared_ptr<rgb_matrix::RGBMatrix> matrix)
{
    assert(name.length() > 0);
    assert(matrix.get() != nullptr);

    this->name = name;
    this->darkMode = false;

    this->_active = false;
    this->_matrix = matrix;
    this->_displayed = true;
    this->_refreshRate = 0.5;
    this->_darkModeHourFont = rgb_matrix::Font();
}

Screen::~Screen()
{
}

void Screen::process()
{
    this->_matrix->Clear();
    rgb_matrix::Color textColor;
    textColor.r = 255;
    textColor.g = 255;
    textColor.b = 255;
    rgb_matrix::DrawText(
        this->_matrix.get(),
        this->_darkModeHourFont,
        0,
        0,
        textColor,
        "Hello"
    );
}

void Screen::update()
{
    while (this->_active)
    {
        if (this->_displayed)
        {
            this->process();
        }
        std::this_thread::sleep_for(
            std::chrono::milliseconds(int((1000 / this->_refreshRate))));
    }
}

void Screen::start()
{
    if (this->_active)
    {
        spdlog::warn("Screen {} is already active", this->name);
        return;
    }
    
    if(this->_darkModeHourFont.LoadFont("./assets/fonts/04B_30__.TTF"))
    {
        spdlog::info("Font loaded successfully");
    } else {
        spdlog::error("Font failed to load");
        return;
    }

    this->_active = true;
    this->_thread = std::thread(std::bind(&Screen::update, this));

    spdlog::info("Screen {} is started", this->name);
}

void Screen::stop()
{
    if (!this->_active)
    {
        spdlog::warn("Screen {} is already stopped", this->name);
        return;
    }

    this->_active = false;
    this->_thread.join();

    spdlog::info("Screen {} stopped", this->name);
}
