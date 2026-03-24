from pathlib import Path
from config import IMAGES_DIR, VALID_EXT


def get_image_files(folder=IMAGES_DIR):
    folder_path = Path(folder)

    if not folder_path.exists() or not folder_path.is_dir():
        return []

    return [
        path for path in sorted(folder_path.rglob("*"))
        if path.is_file() and path.suffix.lower() in VALID_EXT
    ]


def get_first_image(folder=IMAGES_DIR):
    image_files = get_image_files(folder)
    return image_files[0] if image_files else None