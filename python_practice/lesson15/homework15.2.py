import json
import logging
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

BASE = ("https://raw.githubusercontent.com/dntpanix/automation_qa/main/"
        "ideas_for_test/work_with_json/")
FILES = [
    "localizations_en.json",
    "localizations_ru.json",
    "login.json",
    "swagger.json",
]

log_file = Path(__file__).parent / "json_koruts.log"

logger = logging.getLogger("json_validator")
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(handler)


def validate(name):
    try:
        with urlopen(BASE + name) as resp:
            text = resp.read().decode("utf-8")
    except URLError as e:
        logger.error("%s: не вдалося завантажити файл (%s)", name, e)
        return False

    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        logger.error("%s: невалідний JSON: %s (рядок %d, стовпець %d)",
                     name, e.msg, e.lineno, e.colno)
        return False
    return True


for name in FILES:
    ok = validate(name)
    print(f"{name}: {'валідний' if ok else 'НЕвалідний (json_koruts.log)'}")