from pathlib import Path
from config import IMAGES_DIR, VALID_EXT

def get_first_image(folder=IMAGES_DIR):
    folder_path = Path(folder)

    if not folder_path.exists() or not folder_path.is_dir():
        return None

    for p in sorted(folder_path.rglob("*")):
        if p.is_file() and p.suffix.lower() in VALID_EXT:
            return p
    return None