from analyze_color import analyze_image_file, get_first_image
from config import IMAGES_DIR


def main():
    print(f"Searching in: {IMAGES_DIR}")
    image_file = get_first_image()

    if image_file:
        print(f"Image found: {image_file.name}")
        print(f"Path: {image_file}")
        results = analyze_image_file(image_file)
        print(f"Green coverage: {results['green']:.2f}%")
        print(f"Deep green coverage: {results['deep_green']:.2f}%")
        print(f"Beige coverage: {results['beige']:.2f}%")
    else:
        print("No images found in the directory.")


if __name__ == "__main__":
    main()