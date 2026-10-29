import pygame
from game.utils.save_manager import load_save

CHAPTERS = [
    {"id": "ch1_hello", "scene": "chapter_01", "year": "1995", "title": "Hello World"},
    {"id": "ch2_xml", "scene": "chapter_02", "year": "2005", "title": "XML Hell"},
    {"id": "ch3_spring", "scene": "chapter_03", "year": "2010", "title": "Spring Revolution"},
    {"id": "ch4_lambda", "scene": "chapter_04", "year": "2014", "title": "Lambda Clean"},
    {"id": "ch5_jigsaw", "scene": "chapter_05", "year": "2017", "title": "Jigsaw Modules"},
    {"id": "ch6_modern", "scene": "chapter_06", "year": "2026", "title": "Virtual Threads"},
]


class ChapterSelectScene:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("couriernew", 32, bold=True)
        self.font_btn = pygame.font.SysFont("couriernew", 20)

        self.save_data = load_save()
        self.completed = self.save_data.get("completed_levels", [])

        self.buttons = []
        start_y = 200
        for i, ch in enumerate(CHAPTERS):
            rect = pygame.Rect(312, start_y + i * 70, 400, 50)
            self.buttons.append((rect, ch))

    def on_enter(self):
        # Обновляем данные при входе в сцену
        self.save_data = load_save()
        self.completed = self.save_data.get("completed_levels", [])

    def on_exit(self):
        pass

    def update(self, dt):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, ch in self.buttons:
                if rect.collidepoint(event.pos):
                    is_unlocked = (ch["id"] in self.completed) or (ch["id"] == "ch1_hello")
                    if is_unlocked:
                        # В будущем здесь будет переход к нужной главе
                        # Пока все ведут на заглушки или Ch1
                        if ch["id"] == "ch1_hello":
                            return "chapter_01"
                        elif ch["id"] == "ch2_xml":
                            return "chapter_02"
                        else:
                            pass  # Остальные в разработке
        return None

    def draw(self, screen):
        screen.fill((20, 20, 30))

        title = self.font_title.render("SELECT CHAPTER", True, (0, 255, 0))
        screen.blit(title, (1024 // 2 - title.get_width() // 2, 80))

        for rect, ch in self.buttons:
            is_unlocked = (ch["id"] in self.completed) or (ch["id"] == "ch1_hello")

            # Отрисовка кнопки
            bg_color = (50, 50, 60) if is_unlocked else (30, 30, 30)
            border_color = (0, 255, 0) if is_unlocked else (80, 80, 80)
            text_color = (255, 255, 255) if is_unlocked else (100, 100, 100)

            pygame.draw.rect(screen, bg_color, rect, border_radius=5)
            pygame.draw.rect(screen, border_color, rect, 2, border_radius=5)

            # Текст
            label = f"{ch['year']} — {ch['title']}"
            if not is_unlocked:
                label += " 🔒"

            text_surf = self.font_btn.render(label, True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)