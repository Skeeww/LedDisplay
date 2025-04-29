from time import sleep
from datetime import datetime

class Screen():
    current_screen = None
    store = {}

    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix
        self.refresh_rate = 0.5
        self.dark_theme = False
        self.is_active = False

    def process(self):
        raise NotImplementedError("The subclass must implement this method")
    
    def update(self):
        while True:
            if datetime.now().hour >= 21 or datetime.now().hour <= 6:
                self.dark_theme = True
            else:
                self.dark_theme = False
            if self.is_active:
                self.process()
            sleep(1 / self.refresh_rate) if self.refresh_rate > 0 else sleep(1)

    def show(self):
        self.is_active = True
        print(f"[{self.name}] Show")

    def hide(self):
        self.is_active = False
        print(f"[{self.name}] Hide")

    @staticmethod
    def show_screen(screen):
        if Screen.current_screen != screen:
            if Screen.current_screen != None:
                Screen.current_screen.hide()
            Screen.current_screen = screen
            Screen.current_screen.show()
