import os
import pygame


class Duke:
    def __init__(self, era: str = "1995", pos=(800, 400)):
        self.era = era
        self.pos = pos
        self.state = "idle"
        self.image = None
        self.font = pygame.font.SysFont("couriernew", 16, bold=True)

        self.sheet = None
        self.frame_width = 0
        self.load_sheet()

    def set_state(self, new_state: str):
        self.state = new_state
        self.update_frame()

    def load_sheet(self):
        path = os.path.join("assets", "sprites", f"duke_{self.era}_sheet.png")
        try:
            self.sheet = pygame.image.load(path).convert_alpha()

            # ВОЛШЕБСТВО: Делаем белый фон прозрачным (если он есть)
            self.sheet.set_colorkey((255, 255, 255))

            # Делим картинку ровно на 5 частей
            self.frame_width = self.sheet.get_width() // 5
            self.height = self.sheet.get_height()
            self.update_frame()
        except (pygame.error, FileNotFoundError):
            # Заглушка, если файла нет
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.image.fill((180, 30, 30))
            text = self.font.render("DUKE", True, (255, 255, 255))
            self.image.blit(text, (10, 25))

    def update_frame(self):
        if not self.sheet:
            return

        states_map = {
            "idle": 0,
            "nod": 1,
            "shrug": 2,
            "drop_cards": 3,
            "point": 4
        }
        frame_index = states_map.get(self.state, 0)

        # Вырезаем нужный кадр из спрайт-листа
        rect = pygame.Rect(frame_index * self.frame_width, 0, self.frame_width, self.height)
        self.image = pygame.Surface((self.frame_width, self.height), pygame.SRCALPHA)
        self.image.blit(self.sheet, (0, 0), rect)

        # Масштабируем Дюка (0.75 = 75% от исходного размера)
        scale_factor = 0.75
        new_w = int(self.frame_width * scale_factor)
        new_h = int(self.height * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_w, new_h))

    def draw(self, surface):
        surface.blit(self.image, self.pos)