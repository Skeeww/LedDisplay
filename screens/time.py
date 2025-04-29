from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from time import sleep

from screen import Screen

class Time(Screen):
    def __init__(self, matrix):
        super().__init__("Time", matrix)
        self.screen_image = Image.new("RGBA", (64, 32))
        self.japan_image = Image.open("./assets/images/time_background.png").convert("RGBA")
        self.cloud_image = Image.open("./assets/images/cloud_background.png").convert("RGBA").resize((64, 32), Image.NEAREST)
        self.hour_font = ImageFont.truetype("./assets/fonts/Bypass.ttf", 22)
        self.hour_font2 = ImageFont.truetype("./assets/fonts/04B_30__.TTF", 15)
        self.refresh_rate = 1

    def process(self):
        date = datetime.now()
        img = self.screen_image.copy()
        if not(self.dark_theme):
            self.matrix.brightness = 100
            img.paste(self.cloud_image, (0, 0))
            time_screen = ImageDraw.Draw(img)
            time_screen.text((2, 6), date.strftime("%H:%M"), "#4C4C6D", self.hour_font, align="center")
            img.paste(self.japan_image, (0, 14), self.japan_image)
        else:
            self.matrix.brightness = 30
            time_screen = ImageDraw.Draw(img)
            x = int(abs(64 - time_screen.textlength(date.strftime("%H:%M"), self.hour_font2)) / 2) + 1
            time_screen.text((x, 7), date.strftime("%H:%M"), "#FFFFFF", self.hour_font2)
        self.matrix.Clear()
        self.matrix.SetImage(img.convert('RGB'))
