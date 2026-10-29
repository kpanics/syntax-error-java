import pygame

class Engine:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.scenes = {}
        self.current_scene = None

    def register_scene(self, key: str, scene_instance):
        self.scenes[key] = scene_instance

    def change_scene(self, key: str):
        if self.current_scene:
            self.current_scene.on_exit()
        self.current_scene = self.scenes.get(key)
        if self.current_scene:
            self.current_scene.on_enter()
        else:
            print(f"[ERROR] Scene '{key}' not found!")

    def handle_event(self, event):
        if not self.current_scene:
            return
        next_scene_key = self.current_scene.handle_event(event)
        if next_scene_key:
            self.change_scene(next_scene_key)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self):
        if self.current_scene:
            self.current_scene.draw(self.screen)