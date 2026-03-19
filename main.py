from config import IMAGES_DIR
from stitch import get_first_image


def main():
    print(f"Searching in: {IMAGES_DIR}")
    image_file = get_first_image()

    if image_file:
        print(f"Image found: {image_file.name}")
        print(f"Path: {image_file}")
    else:
        print("No images found in the directory.")


if __name__ == "__main__":
    main()