import os
import pygame

class Duke:
    def __init__(self, era: str = "1995", pos=(800, 400)):
        self.era = era
        self.pos = pos
        self.state = "idle"
        self.image = None
        self.font = pygame.font.SysFont("couriernew", 16, bold=True)
        self.load_sprite()

    def set_state(self, new_state: str):
        self.state = new_state
        self.load_sprite()

    def load_sprite(self):
        filename = f"duke_{self.era}_{self.state}.png"
        path = os.path.join("assets", "sprites", filename)
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            # ЗАГЛУШКА (Placeholder), если ChatGPT еще не сгенерировал спрайт
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.image.fill((180, 30, 30)) # Красная рубашка
            text = self.font.render("DUKE", True, (255, 255, 255))
            self.image.blit(text, (10, 25))

    def draw(self, surface):
        surface.blit(self.image, self.pos)