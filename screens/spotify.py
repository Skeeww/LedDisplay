from PIL import Image, ImageFont, ImageDraw
from time import sleep
from threading import Thread, Lock
import requests, shutil

from screen import Screen

class Spotify(Screen):
    def __init__(self, matrix):
        super().__init__("Spotify", matrix)
        self.screen_image = Image.new("RGB", (64, 32))
        self.font = ImageFont.truetype("./assets/fonts/TT Mussels Trial Bold.otf", 16)
        self.font2 = ImageFont.truetype("./assets/fonts/Bypass.ttf", 16)
        self.cover = None
        self.cover_id = None
        self.text_i = 0
        self.current_playing = None
        self.playing = False
        self.data_cover_lock = Lock()
        self.update_info_thread = Thread(target=self.update_info)
        self.update_info_thread.start()

    def update_info(self):
        while True:
            if Screen.store.get('sp') == None:
                self.playing = False
                continue
            else:
                self.data_cover_lock.acquire(True)
                self.current_playing = Screen.store.get('sp').current_playback()
            
            if not(self.current_playing) or not(self.current_playing['item']):
                self.playing = False
                self.data_cover_lock.release()
            else:
                self.playing = True
                if self.current_playing['item']['id'] != self.cover_id:
                    self.data_cover_lock.release()
                    cover_img_req = requests.get(self.current_playing['item']['album']['images'][2]['url'], stream=True)
                    if cover_img_req.status_code == 200:
                        with open(f"/tmp/cover.jpg", "wb") as cover_file:
                            shutil.copyfileobj(cover_img_req.raw, cover_file)
                            self.cover_id = self.current_playing['item']['id']
                else:
                    self.data_cover_lock.release()
            sleep(10)

    def process(self):
        img = self.screen_image.copy()
        screen = ImageDraw.Draw(img)

        if self.dark_theme:
            self.matrix.brightness = 30
        else:
            self.matrix.brightness = 100
        
        self.data_cover_lock.acquire(True)
        if not(self.playing) or not(self.current_playing):
            self.refresh_rate = 1
            spotify_logo = Image.open("./assets/images/spotify.png").resize((25, 25), Image.NEAREST)
            img.paste(spotify_logo, (10, 3))
            screen.text((35, 0), "Zzz", "#1DB954", font=self.font)
            self.matrix.Clear()
            self.matrix.SetImage(img.convert('RGB'))
            self.data_cover_lock.release()
            return

        self.refresh_rate = 30

        # Title
        title_label = f"{self.current_playing['item']['name']} - {self.current_playing['item']['artists'][0]['name']}"
        screen.text((64 - self.text_i, 3), title_label, font=self.font)
        text_length = round(screen.textlength(title_label, font=self.font))
        if self.text_i > text_length + 64:
            self.text_i = 0
        else:
            self.text_i += 1

        # Cover
        if not(self.cover) or self.current_playing['item']['id'] != self.cover_id:
            cover_img_req = requests.get(self.current_playing['item']['album']['images'][2]['url'], stream=True)
            if cover_img_req.status_code == 200:
                with open(f"/tmp/cover.jpg", "wb") as cover_file:
                    shutil.copyfileobj(cover_img_req.raw, cover_file)
                    self.cover_id = self.current_playing['item']['id']
        self.cover = Image.open("/tmp/cover.jpg").resize((20, 20), Image.BICUBIC)
        img.paste(self.cover, (0, 5))

        # Play/Pause button
        if not(self.current_playing['is_playing']):
            screen.polygon([(22, 18), (25, 21), (22, 24)], "green")
        else:
            screen.line([(22, 18), (22, 24)], "green", 2)
            screen.line([(25, 18), (25, 24)], "green", 2)
        
        # Progress bar
        if self.current_playing['item']:
            screen.line([(28, 21), (28 + round(33 * self.current_playing['progress_ms'] / self.current_playing['item']['duration_ms']), 21)], "#1DB954", 1)

        self.data_cover_lock.release()

        self.matrix.Clear()
        self.matrix.SetImage(img.convert('RGB'))
