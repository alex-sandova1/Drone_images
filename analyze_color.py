from pathlib import Path
import numpy as np
import cv2

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


def clean_mask(mask, k=5):
    kernel = np.ones((k, k), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def pct(mask):
    return 100.0 * np.count_nonzero(mask) / mask.size


def save_mask_images(image_file, bgr, grass, tree, sand, road, out_dir=Path("mask_outputs")):
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(image_file).stem

    cv2.imwrite(str(out_dir / f"{stem}_grass_mask.png"), grass)
    cv2.imwrite(str(out_dir / f"{stem}_tree_mask.png"), tree)
    cv2.imwrite(str(out_dir / f"{stem}_sand_mask.png"), sand)
    cv2.imwrite(str(out_dir / f"{stem}_road_mask.png"), road)

    overlay = np.zeros_like(bgr)
    overlay[grass > 0] = (0, 220, 0)      # green
    overlay[tree > 0]  = (0, 100, 0)      # dark green
    overlay[sand > 0]  = (170, 220, 240)  # beige
    overlay[road > 0]  = (120, 120, 120)  # gray

    blended = cv2.addWeighted(bgr, 0.6, overlay, 0.4, 0)

    cv2.imwrite(str(out_dir / f"{stem}_overlay.png"), overlay)
    cv2.imwrite(str(out_dir / f"{stem}_blended.png"), blended)

    print(f"Mask images saved to: {out_dir.resolve()}")


def make_color_mask(bgr):   #creates masks for grass, tree, and sand
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)  #turns image to HSV for easier color segmentation
    
    #Defines color parameters
    grass_low = np.array([35,40,40], dtype=np.uint8)
    grass_high = np.array([90,255,255], dtype=np.uint8)
    
    tree_low = np.array([35,80,25], dtype=np.uint8)
    tree_high = np.array([90,255,120], dtype=np.uint8)
    
    sand_low = np.array([15,20,100], dtype=np.uint8)
    sand_high = np.array([35,160,255], dtype=np.uint8)
    
    road_low = np.array([0,0,55], dtype=np.uint8)
    road_high = np.array([179,70,140], dtype=np.uint8)
    
    #creates masks
    grass = cv2.inRange(hsv, grass_low, grass_high)
    tree = cv2.inRange(hsv, tree_low, tree_high)
    sand = cv2.inRange(hsv, sand_low, sand_high)
    road = cv2.inRange(hsv, road_low, road_high)
    return grass, tree, sand, road


def analyze_land_cover(bgr, k=5):   #pipeline function 
    if bgr is None or bgr.size == 0:
        raise ValueError("Input image is empty or could not be read.")

    grass, tree, sand, road = make_color_mask(bgr)
    grass = clean_mask(grass, k=k)
    tree = clean_mask(tree, k=k)
    sand = clean_mask(sand, k=k)
    road = clean_mask(road, k=k)
    
    return {
        "grass": pct(grass),
        "tree": pct(tree),
        "sand": pct(sand),
        "road": pct(road),
    }


def analyze_image_file(image_path, k=5):
    image_path = Path(image_path)
    bgr = cv2.imread(str(image_path))

    if bgr is None:
        raise ValueError(f"Unable to read image file: {image_path}")

    return analyze_land_cover(bgr, k=k)


def analyze_image_batch(image_paths, k=5):
    results = []

    for image_path in image_paths:
        image_path = Path(image_path)
        coverage = analyze_image_file(image_path, k=k)
        results.append({
            "image_path": image_path,
            **coverage,
        })

    return results

