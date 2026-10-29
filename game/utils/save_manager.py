import os
import json

SAVE_DIR = os.path.expanduser("~/.syntax_error_java")
SAVE_PATH = os.path.join(SAVE_DIR, "save.json")

DEFAULT_SAVE = {
    "completed_levels": [],
    "current_level": "prologue_01",
    "chapter_progress": {
        "ch1": 0, "ch2": 0, "ch3": 0, "ch4": 0, "ch5": 0, "ch6": 0
    },
    "python_view_unlocked": False,
    "hints_used": {},
    "achievements": []
}


def load_save() -> dict:
    if not os.path.exists(SAVE_PATH):
        return DEFAULT_SAVE.copy()
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in DEFAULT_SAVE.items():
            data.setdefault(k, v)
        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SAVE.copy()


def write_save(data: dict) -> None:
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def complete_level(level_id: str, hints_used: int):
    save = load_save()

    # Добавляем в пройденные, если еще нет
    if level_id not in save["completed_levels"]:
        save["completed_levels"].append(level_id)

        # Инкрементируем прогресс главы
        chapter_id = level_id.split("_")[0]
        if chapter_id in save["chapter_progress"]:
            save["chapter_progress"][chapter_id] += 1

    save["hints_used"][level_id] = hints_used

    if hints_used == 0:
        ach = f"no_hints_{level_id}"
        if ach not in save["achievements"]:
            save["achievements"].append(ach)

    write_save(save)