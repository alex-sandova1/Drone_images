from PIL import Image
import cv2
from pathlib import Path

from analyze_color import analyze_image_batch, clean_mask, pct, make_color_mask, analyze_image_file, analyze_land_cover
from config import IMAGES_DIR
from stitch import get_first_image, get_image_files, save_stitched_image, stitch_first_n_images


def main():
    print(f"Searching in: {IMAGES_DIR}")
    image_file = get_first_image()
    image_files = get_image_files()
    stitch_output_dir = Path(__file__).resolve().parent / "stitch_images_test"

    if image_file:
        with Image.open(image_file) as image:
            print(f"Image: {image_file.name}")
            print(f"Path: {image_file}")
            print(f"Format: {image.format}")
            print(f"Size: {image.size}")
            print(f"Mode: {image.mode}")
            print("\n")

        #create mask test block
        print("\nReached color mask test block")
        bgr = cv2.imread(str(image_file))
        green, deep_green, beige = make_color_mask(bgr)
        print(f"Green mask coverage: {pct(green):.2f}%")
        print(f"Deep green mask coverage: {pct(deep_green):.2f}%")
        print(f"Beige mask coverage: {pct(beige):.2f}%")
        
        #clean mask test block
        print("\nReached mask test block")
        bgr = cv2.imread(str(image_file))
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        _, raw_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

        cleaned = clean_mask(raw_mask, k=5)

        #pct test block
        print(f"Raw mask coverage: {pct(raw_mask):.2f}%")
        print(f"Cleaned mask coverage: {pct(cleaned):.2f}%")
        
        #analyze land cover test block
        print("Reached land cover analysis test block")
        bgr = cv2.imread(str(image_file))
        results = analyze_land_cover(bgr, k=5)
        print(f"Green coverage: {results['green']:.2f}%")
        print(f"Deep green coverage: {results['deep_green']:.2f}%")
        print(f"Beige coverage: {results['beige']:.2f}%")

        #analyze image file test block
        print("\nReached image file analysis test block")
        file_results = analyze_image_file(image_file, k=5)
        print(f"File green coverage: {file_results['green']:.2f}%")
        print(f"File deep green coverage: {file_results['deep_green']:.2f}%")
        print(f"File beige coverage: {file_results['beige']:.2f}%")

        #analyze image batch test block
        batch_files = image_files[:5]
        print(f"\nReached batch analysis test block for {len(batch_files)} images")
        batch_results = analyze_image_batch(batch_files, k=5)

        for result in batch_results:
            print(f"{result['image_path'].name} -> green: {result['green']:.2f}%, deep green: {result['deep_green']:.2f}%, beige: {result['beige']:.2f}%")

        avg_green = sum(result["green"] for result in batch_results) / len(batch_results)
        avg_deep_green = sum(result["deep_green"] for result in batch_results) / len(batch_results)
        avg_beige = sum(result["beige"] for result in batch_results) / len(batch_results)

        print("Batch average coverage")
        print(f"Average green coverage: {avg_green:.2f}%")
        print(f"Average deep green coverage: {avg_deep_green:.2f}%")
        print(f"Average beige coverage: {avg_beige:.2f}%")

        print("\nReached stitching test block")
        stitched_files, stitched_bgr, stitch_method = stitch_first_n_images(n=5)
        stitched_path = save_stitched_image(stitched_bgr, stitch_output_dir)
        print(f"Stitch method used: {stitch_method}")
        print("Stitched files:")
        for image_path in stitched_files:
            print(f"- {image_path.name}")
        print(f"Stitched output saved to: {stitched_path}")
    else:
        print("No images found in the directory.")


if __name__ == "__main__":
    main()