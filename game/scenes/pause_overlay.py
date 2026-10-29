import pygame
from game.ui.button import Button


class PauseOverlay:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("couriernew", 36, bold=True)
        self.font_btn = pygame.font.SysFont("couriernew", 20)

        self.btn_resume = Button((400, 250, 224, 40), "[ RESUME ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                                 (255, 255, 255))
        self.btn_restart = Button((400, 310, 224, 40), "[ RESTART LEVEL ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                                  (255, 255, 255))
        self.btn_select = Button((400, 370, 224, 40), "[ CHAPTER SELECT ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                                 (255, 255, 255))
        self.btn_menu = Button((400, 430, 224, 40), "[ MAIN MENU ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                               (255, 255, 255))
        self.btn_quit = Button((400, 490, 224, 40), "[ QUIT ]", self.font_btn, (30, 30, 30), (50, 50, 50),
                               (255, 255, 255))

    def handle_event(self, event):
        if self.btn_resume.handle_event(event): return "resume"
        if self.btn_restart.handle_event(event): return "restart"
        if self.btn_select.handle_event(event): return "chapter_select"
        if self.btn_menu.handle_event(event): return "main_menu"
        if self.btn_quit.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        return None

    def draw(self, screen):
        # Прозрачный черный фон
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.font_title.render("PAUSED", True, (0, 255, 0))
        screen.blit(title, (512 - title.get_width() // 2, 150))

        self.btn_resume.draw(screen)
        self.btn_restart.draw(screen)
        self.btn_select.draw(screen)
        self.btn_menu.draw(screen)
        self.btn_quit.draw(screen)