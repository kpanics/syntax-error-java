import pygame
import os
from game.ui.button import Button
from game.utils.save_manager import SAVE_PATH, load_save
from game.entities.duke import Duke


class MainMenuScene:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("couriernew", 48, bold=True)
        self.font_btn = pygame.font.SysFont("couriernew", 24)
        self.font_small = pygame.font.SysFont("couriernew", 16)

        self.duke = Duke(era="1995", pos=(800, 400))

        self.btn_continue = Button((400, 380, 224, 50), "[ CONTINUE ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                                   (255, 255, 255))
        self.btn_new = Button((400, 450, 224, 50), "[ NEW GAME ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                              (255, 255, 255))
        self.btn_settings = Button((400, 520, 224, 50), "[ SETTINGS ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                                   (255, 255, 255))
        self.btn_quit = Button((400, 590, 224, 50), "[ QUIT ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                               (255, 255, 255))

        self.show_confirm = False
        self.btn_yes = Button((350, 400, 100, 40), "YES", self.font_small, (100, 30, 30), (150, 50, 50),
                              (255, 255, 255))
        self.btn_no = Button((550, 400, 100, 40), "NO", self.font_small, (30, 100, 30), (50, 150, 50), (255, 255, 255))

    def on_enter(self):
        self.has_save = os.path.exists(SAVE_PATH)
        self.btn_continue.color_normal = (30, 30, 30) if self.has_save else (10, 10, 10)
        self.btn_continue.text_color = (255, 255, 255) if self.has_save else (80, 80, 80)
        self.show_confirm = False

    def on_exit(self):
        pass

    def update(self, dt):
        pass

    def handle_event(self, event):
        if self.show_confirm:
            if self.btn_yes.handle_event(event):
                if os.path.exists(SAVE_PATH):
                    os.remove(SAVE_PATH)  # Удаляем ТОЛЬКО сейв
                return "prologue_01"
            if self.btn_no.handle_event(event):
                self.show_confirm = False
            return None

        if self.has_save and self.btn_continue.handle_event(event):
            save = load_save()
            if not save.get("completed_levels"):
                return "prologue_01"
            return "chapter_select"

        if self.btn_new.handle_event(event):
            self.show_confirm = True

        if self.btn_settings.handle_event(event):
            return "settings"

        if self.btn_quit.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        return None

    def draw(self, screen):
        screen.fill((15, 15, 20))

        title = self.font_title.render("SYNTAX ERROR", True, (0, 255, 0))
        subtitle = self.font_btn.render("Java in the Python", True, (100, 150, 100))

        screen.blit(title, (512 - title.get_width() // 2, 150))
        screen.blit(subtitle, (512 - subtitle.get_width() // 2, 210))

        self.duke.draw(screen)

        self.btn_continue.draw(screen)
        self.btn_new.draw(screen)
        self.btn_settings.draw(screen)
        self.btn_quit.draw(screen)

        if self.show_confirm:
            overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            txt = self.font_btn.render("Erase all progress?", True, (255, 255, 255))
            screen.blit(txt, (512 - txt.get_width() // 2, 300))
            self.btn_yes.draw(screen)
            self.btn_no.draw(screen)