import pygame
from game.utils.settings_manager import load_settings, update_setting
from game.ui.button import Button


class SettingsScene:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("couriernew", 32, bold=True)
        self.font_btn = pygame.font.SysFont("couriernew", 20)

        self.settings = load_settings()

        self.btn_back = Button((400, 550, 224, 50), "[ BACK ]", self.font_btn, (50, 50, 50), (80, 80, 80),
                               (255, 255, 255))
        self.btn_vol_up = Button((500, 250, 50, 40), " + ", self.font_btn, (50, 50, 50), (80, 80, 80), (255, 255, 255))
        self.btn_vol_down = Button((300, 250, 50, 40), " - ", self.font_btn, (50, 50, 50), (80, 80, 80),
                                   (255, 255, 255))
        self.btn_fullscreen = Button((350, 350, 324, 50), "", self.font_btn, (50, 50, 50), (80, 80, 80),
                                     (255, 255, 255))

    def on_enter(self):
        self.settings = load_settings()
        self.update_vol_text()

    def on_exit(self):
        pass

    def update(self, dt):
        pass

    def update_vol_text(self):
        vol_pct = int(self.settings["master_volume"] * 100)
        self.btn_vol_text = self.font_btn.render(f"Master Volume: {vol_pct}%", True, (255, 255, 255))

        fs_text = "Fullscreen: ON" if self.settings["fullscreen"] else "Fullscreen: OFF"
        self.btn_fullscreen.text = f"[ {fs_text} ]"

    def handle_event(self, event):
        if self.btn_back.handle_event(event):
            return "main_menu"

        if self.btn_vol_up.handle_event(event):
            self.settings["master_volume"] = min(1.0, self.settings["master_volume"] + 0.1)
            update_setting("master_volume", self.settings["master_volume"])
            pygame.mixer.music.set_volume(self.settings["master_volume"])
            self.update_vol_text()

        if self.btn_vol_down.handle_event(event):
            self.settings["master_volume"] = max(0.0, self.settings["master_volume"] - 0.1)
            update_setting("master_volume", self.settings["master_volume"])
            pygame.mixer.music.set_volume(self.settings["master_volume"])
            self.update_vol_text()

        if self.btn_fullscreen.handle_event(event):
            self.settings["fullscreen"] = not self.settings["fullscreen"]
            update_setting("fullscreen", self.settings["fullscreen"])

            # Применяем fullscreen
            if self.settings["fullscreen"]:
                pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
            else:
                pygame.display.set_mode((1920, 1080))
            self.update_vol_text()

        return None

    def draw(self, screen):
        screen.fill((20, 20, 30))
        title = self.font_title.render("SETTINGS", True, (0, 255, 0))
        screen.blit(title, (512 - title.get_width() // 2, 100))

        screen.blit(self.btn_vol_text, (512 - self.btn_vol_text.get_width() // 2, 260))
        self.btn_vol_up.draw(screen)
        self.btn_vol_down.draw(screen)

        self.btn_fullscreen.draw(screen)
        self.btn_back.draw(screen)