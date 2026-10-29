import json
import os

LEVELS_DIR = os.path.join("data", "levels")
INDEX_PATH = os.path.join("data", "levels_index.json")


def load_index() -> dict:
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_level_data(level_id: str) -> dict:
    file_path = os.path.join(LEVELS_DIR, f"{level_id}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_next_level(current_level_id: str) -> str | None:
    index = load_index()
    for chapter_id, chapter_data in index["chapters"].items():
        levels = chapter_data["levels"]
        if current_level_id in levels:
            current_idx = levels.index(current_level_id)
            if current_idx + 1 < len(levels):
                return levels[current_idx + 1]
    return None


def is_level_unlocked(level_id: str, save_data: dict) -> bool:
    chapter_id = level_id.split("_")[0]
    if chapter_id == "ch1":
        return True

    index = load_index()
    req = index["chapters"].get(chapter_id, {}).get("unlock_requirement")
    if not req:
        return True

    prev_chapter = req["chapter"]
    min_req = req["min_completed_levels"]

    current_progress = save_data.get("chapter_progress", {}).get(prev_chapter, 0)
    return current_progress >= min_req