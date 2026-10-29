import pygame
from game.ui.code_editor import CodeEditor
from game.validators.java_validator import validate
from game.entities.duke import Duke
from game.ui.button import Button
from game.utils.save_manager import complete_level
from game.utils.level_loader import get_level_data

ERROR_TRANSLATIONS = {
    "SyntaxError: expected ';'. The compiler is not amused.": "SyntaxError: The compiler is waiting for a semicolon ';' at the end of your statement.",
    "Missing required element: public static void main": "SyntaxError: Where is the entry point? Java needs a 'public static void main' method to start.",
    "Missing required element: public class Main": "SyntaxError: Java requires a 'public class Main' declaration.",
    "Missing required element: System.out.println": "SyntaxError: Use 'System.out.println()' to print text to the console.",
    "StructureError: failed main_method_regex": "SyntaxError: Where is the entry point? Java needs a 'public static void main(String[] args)' method to start."
}


class Chapter1Scene:
    def __init__(self, engine, level_id="ch1_3_hello_world"):
        self.engine = engine
        self.level_id = level_id
        self.level_data = get_level_data(level_id)

        self.font_title = pygame.font.SysFont("couriernew", 24, bold=True)
        self.font_code = pygame.font.SysFont("couriernew", 20)
        self.font_ui = pygame.font.SysFont("couriernew", 16)

        self.duke = Duke(era="1995", pos=(780, 300))  # Подняли Дюка выше

        self.editor_rect = pygame.Rect(50, 100, 650, 500)

        # Загружаем стартовый код из JSON
        starter = self.level_data.get("starter_code", "")
        self.editor = CodeEditor(self.editor_rect, self.font_code, starter)

        # ЖЕСТКО СТАВИМ КУРСОР ВНУТРЬ МЕТОДА MAIN
        search_str = "args) {\n"
        idx = self.editor.text.find(search_str)
        if idx != -1:
            # + 8 пробелов для отступа
            self.editor.cursor_pos = idx + len(search_str) + 8

        self.btn_compile = Button((50, 620, 200, 40), "[ F5: COMPILE ]", self.font_ui, (50, 50, 50), (80, 80, 80),
                                  (255, 255, 255))
        self.btn_python_view = Button((270, 620, 200, 40), "[ PYTHON VIEW ]", self.font_ui, (50, 50, 50), (80, 80, 80),
                                      (255, 255, 255))

        self.show_python_view = False
        self.is_success = False
        self.message = ""
        self.msg_color = (255, 255, 255)
        self.msg_timer = 0.0
        self.transition_timer = -1.0

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self, dt):
        self.editor.update(dt)
        if self.msg_timer > 0:
            self.msg_timer -= dt

        if self.transition_timer > 0:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.engine.change_scene("chapter_select")

    def compile_code(self):
        code = self.editor.get_code()
        result = validate(code, self.level_data["validation"])

        if result.ok:
            self.message = "Compilation Successful! Bytecode generated."
            self.msg_color = (0, 255, 0)
            self.msg_timer = 3.0
            self.duke.set_state("nod")
            self.is_success = True
            complete_level(self.level_id, hints_used=0)
            self.transition_timer = 2.0
        else:
            translated_msg = ERROR_TRANSLATIONS.get(result.message, result.message)
            self.message = translated_msg
            self.msg_color = (255, 50, 50)
            self.msg_timer = 4.0
            self.duke.set_state("drop_cards")

    def handle_event(self, event):
        if self.btn_compile.handle_event(event):
            self.compile_code()
            return None

        if self.btn_python_view.handle_event(event):
            self.show_python_view = not self.show_python_view
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                self.compile_code()
                return None
            elif event.key == pygame.K_ESCAPE:
                return None
            else:
                self.editor.handle_event(event)

        return None

    def draw(self, screen):
        screen.fill((40, 40, 45))

        ide_rect = pygame.Rect(30, 30, 700, 700)
        pygame.draw.rect(screen, (192, 192, 192), ide_rect)
        pygame.draw.rect(screen, (255, 255, 255),
                         (ide_rect.x + 5, ide_rect.y + 30, ide_rect.width - 10, ide_rect.height - 35))
        pygame.draw.rect(screen, (0, 0, 128), (ide_rect.x + 5, ide_rect.y + 5, ide_rect.width - 10, 25))

        title = self.font_ui.render(f"Notepad - {self.level_id}.java", True, (255, 255, 255))
        screen.blit(title, (ide_rect.x + 10, ide_rect.y + 8))

        game_title = self.font_title.render(self.level_data["title"], True, (200, 200, 200))
        screen.blit(game_title, (750, 50))

        self.editor.draw(screen)
        self.btn_compile.draw(screen)
        self.btn_python_view.draw(screen)
        self.duke.draw(screen)

        if self.show_python_view and self.level_data.get("python_view", {}).get("enabled"):
            pv = self.level_data["python_view"]
            panel_rect = pygame.Rect(745, 150, 260, 400)
            pygame.draw.rect(screen, (20, 25, 35), panel_rect)
            pygame.draw.rect(screen, (80, 120, 200), panel_rect, 2)

            title = self.font_ui.render("How would Python do it?", True, (100, 200, 255))
            screen.blit(title, (panel_rect.x + 10, panel_rect.y + 10))

            j_lbl = self.font_ui.render("Java:", True, (200, 200, 200))
            screen.blit(j_lbl, (panel_rect.x + 10, panel_rect.y + 50))
            j_code_1 = self.font_ui.render(pv["java_code"][:20], True, (255, 150, 100))
            j_code_2 = self.font_ui.render(pv["java_code"][20:], True, (255, 150, 100))
            screen.blit(j_code_1, (panel_rect.x + 10, panel_rect.y + 70))
            screen.blit(j_code_2, (panel_rect.x + 25, panel_rect.y + 90))

            p_lbl = self.font_ui.render("Python:", True, (200, 200, 200))
            screen.blit(p_lbl, (panel_rect.x + 10, panel_rect.y + 130))
            p_code = self.font_ui.render(pv["python_code"], True, (100, 255, 100))
            screen.blit(p_code, (panel_rect.x + 10, panel_rect.y + 150))

            pygame.draw.line(screen, (100, 100, 100), (panel_rect.x + 10, panel_rect.y + 190),
                             (panel_rect.right - 10, panel_rect.y + 190))

            comment = pv["comment"]
            words = comment.split()
            line = ""
            y_offset = panel_rect.y + 210
            for word in words:
                if self.font_ui.size(line + word)[0] < 230:
                    line += word + " "
                else:
                    c_surf = self.font_ui.render(line, True, (200, 200, 200))
                    screen.blit(c_surf, (panel_rect.x + 10, y_offset))
                    y_offset += 20
                    line = word + " "
            c_surf = self.font_ui.render(line, True, (200, 200, 200))
            screen.blit(c_surf, (panel_rect.x + 10, y_offset))

        if self.msg_timer > 0:
            msg_surf = self.font_ui.render(self.message, True, self.msg_color)
            screen.blit(msg_surf, (50, 680))