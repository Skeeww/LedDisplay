#include <ctime>
#include <csignal>
#include <string>
#include <sstream>
#include <thread>
#include <memory>

#include "libs/spdlog/include/spdlog/spdlog.h"
#include "libs/rpi-rgb-led-matrix/include/led-matrix.h"

#include "includes/screen.h"

std::shared_ptr<Screen> g_screen = nullptr;

void handle_sigint(int param) {
    spdlog::warn("Exiting after Ctrl+C");
    if (g_screen) {
        g_screen->stop();
    }
    exit(EXIT_SUCCESS);
}

int main(int argc, char *argv[]) {
    spdlog::info("LedDisplay V1.0.0 - Starting...");

    rgb_matrix::RGBMatrix::Options opts;
    opts.hardware_mapping = "regular";
    opts.cols = 64;
    opts.rows = 32;
    opts.brightness = 100;
    opts.parallel = 1;
    opts.show_refresh_rate = true;

    auto shrPtr_matrix = std::shared_ptr<rgb_matrix::RGBMatrix>(rgb_matrix::RGBMatrix::CreateFromFlags(&argc, &argv, &opts));

    g_screen = std::make_shared<Screen>("Screen de test", shrPtr_matrix);
    
    signal(SIGINT, handle_sigint);
    
    g_screen->start();

    while (true) {};
    return EXIT_SUCCESS;
}
