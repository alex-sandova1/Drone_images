from pathlib import Path
from datetime import datetime
import cv2

from config import IMAGES_DIR, VALID_EXT


def get_image_files(folder=IMAGES_DIR):     #returns list of image files in the directory, sorted by name, and filtered by valid extensions
    folder_path = Path(folder)

    if not folder_path.exists() or not folder_path.is_dir():
        return []

    return [
        path for path in sorted(folder_path.rglob("*"))
        if path.is_file() and path.suffix.lower() in VALID_EXT
    ]


def get_first_image(folder=IMAGES_DIR):     #returns the first image file in the directory, or None if no images are found
    image_files = get_image_files(folder)
    return image_files[0] if image_files else None


def load_images(image_paths):
    images = []

    for image_path in image_paths:
        image_path = Path(image_path)
        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(f"Unable to read image file: {image_path}")

        images.append(image)

    return images


def make_concat_preview(images):
    if not images:
        raise ValueError("No images provided for preview composition.")

    min_height = min(image.shape[0] for image in images)
    resized = [
        cv2.resize(
            image,
            (int(image.shape[1] * (min_height / image.shape[0])), min_height),
            interpolation=cv2.INTER_AREA,
        )
        for image in images
    ]

    return cv2.hconcat(resized)


def stitch_images(image_paths):
    images = load_images(image_paths)

    if len(images) < 2:
        raise ValueError("At least 2 images are required to stitch.")

    attempts = [
        ("panorama-full", cv2.Stitcher_PANORAMA, 1.0),
        ("scans-full", cv2.Stitcher_SCANS, 1.0),
        ("panorama-half", cv2.Stitcher_PANORAMA, 0.5),
        ("scans-half", cv2.Stitcher_SCANS, 0.5),
    ]

    error_details = []

    for label, mode, scale in attempts:
        if scale < 1.0:
            resized = [
                cv2.resize(
                    image,
                    None,
                    fx=scale,
                    fy=scale,
                    interpolation=cv2.INTER_AREA,
                )
                for image in images
            ]
        else:
            resized = images

        stitcher = cv2.Stitcher_create(mode)
        status, stitched = stitcher.stitch(resized)

        if status == cv2.Stitcher_OK:
            return stitched, label

        error_details.append(f"{label}:{status}")

    fallback = make_concat_preview(images)
    return fallback, f"concat-fallback ({', '.join(error_details)})"


def stitch_first_n_images(folder=IMAGES_DIR, n=5):
    image_files = get_image_files(folder)
    selected_files = image_files[:n]

    if len(selected_files) < 2:
        raise ValueError("Need at least 2 valid images to stitch.")

    stitched, method = stitch_images(selected_files)
    return selected_files, stitched, method


def save_stitched_image(stitched_bgr, output_dir, prefix="stitched_progress"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"{prefix}_{timestamp}.jpg"

    ok = cv2.imwrite(str(output_path), stitched_bgr)
    if not ok:
        raise RuntimeError(f"Failed to save stitched image: {output_path}")

    return output_path