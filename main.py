import sys
import pygame
from game.engine import Engine
from game.scenes.prologue import PrologueScene01, PrologueScene02
from game.scenes.chapter1 import Chapter1Scene
from game.scenes.chapter_select import ChapterSelectScene  # <--- Импорт меню


# Заглушка для Chapter 2
class DummyChapter2:
    def __init__(self, engine): pass

    def on_enter(self): pass

    def on_exit(self): pass

    def handle_event(self, event): return None

    def update(self, dt): pass

    def draw(self, screen):
        screen.fill((30, 20, 20))
        font = pygame.font.SysFont("couriernew", 24)
        text = font.render("CHAPTER 2: XML HELL (Coming soon)", True, (255, 100, 100))
        screen.blit(text, (200, 350))


def main():
    pygame.init()
    pygame.mixer.init()

    REAL_WIDTH, REAL_HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT))
    pygame.display.set_caption("Syntax Error: Java in the Python")
    clock = pygame.time.Clock()

    VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1024, 768
    virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    engine = Engine(virtual_surface, clock)

    engine.register_scene("prologue_01", PrologueScene01(engine))
    engine.register_scene("prologue_02", PrologueScene02(engine))
    engine.register_scene("chapter_select", ChapterSelectScene(engine))  # <--- Меню
    engine.register_scene("chapter_01", Chapter1Scene(engine))
    engine.register_scene("chapter_02", DummyChapter2(engine))  # <--- Заглушка Ch2

    engine.change_scene("prologue_01")

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.USEREVENT:
                engine.change_scene("chapter_01")
            else:
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    if hasattr(event, 'pos'):
                        scale_x = VIRTUAL_WIDTH / REAL_WIDTH
                        scale_y = VIRTUAL_HEIGHT / REAL_HEIGHT
                        new_pos = (int(event.pos[0] * scale_x), int(event.pos[1] * scale_y))
                        if event.type == pygame.MOUSEMOTION:
                            new_event = pygame.event.Event(event.type, pos=new_pos, rel=event.rel,
                                                           buttons=event.buttons)
                        else:
                            new_event = pygame.event.Event(event.type, pos=new_pos, button=event.button)
                        engine.handle_event(new_event)
                        continue
                engine.handle_event(event)

        engine.update(dt)
        engine.draw()
        scaled_surface = pygame.transform.scale(virtual_surface, (REAL_WIDTH, REAL_HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()