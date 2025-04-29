import spotipy

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from screen import Screen
from threading import Thread
from time import sleep

from screens import time, spotify

load_dotenv()

rgb_options = RGBMatrixOptions()
rgb_options.rows = 32
rgb_options.cols = 64
rgb_options.disable_hardware_pulsing = 0

matrix = RGBMatrix(options=rgb_options)
matrix.brightness = 100

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-playback-state", open_browser=False, cache_path="/tmp/spotify_token"))

screens = {
    'time': time.Time(matrix),
    'spotify': spotify.Spotify(matrix)
}

screens_threads = {}

for name, screen in screens.items():
    print(f"[Thread]({name}) Starting...")
    try:
        screens_threads.update({name: Thread(target=screen.update)})
        screens_threads.get(name).start()
        print(f"[Thread]({name}) Started")
    except Exception as err:
        print(err)
        print(f"[Thread]({name}) Failed to start")

spotify = screens.get('spotify')

Screen.store.update({'sp': sp})

time_screen = screens.get('time')

# Screen logic
while True:
    try:
        while spotify.playing:
            Screen.show_screen(spotify)
        Screen.show_screen(time_screen)
    except:
        break

# Join all threads
for name, screen_thread in screens_threads.items():
    print(f"[Thread]({name}) Stopping...")
    screen_thread.join()
    print(f"[Thread]({name}) Stopped")
