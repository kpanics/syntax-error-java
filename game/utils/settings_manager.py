import os
import json

SETTINGS_DIR = os.path.expanduser("~/.syntax_error_java")
SETTINGS_PATH = os.path.join(SETTINGS_DIR, "settings.json")

DEFAULT_SETTINGS = {
    "master_volume": 0.7,
    "fullscreen": False
}

def load_settings() -> dict:
    if not os.path.exists(SETTINGS_PATH):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()

def write_settings(data: dict) -> None:
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_setting(key: str, value) -> None:
    data = load_settings()
    data[key] = value
    write_settings(data)