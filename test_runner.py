from PIL import Image
import cv2
from pathlib import Path

from analyze_color import analyze_image_batch, clean_mask, pct, make_color_mask, analyze_image_file, analyze_land_cover, get_first_image, get_image_files, save_mask_images
from config import IMAGES_DIR


def main():
    
    #block is commented out since it's primarily for debugging and inspecting individual image properties found in outside data folder (Complete_image.jped)
    
    image_file = Path("Complete_image.jpeg")
    
    if image_file.exists():
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
        grass, tree, sand, road = make_color_mask(bgr)
        print(f"Grass mask coverage: {pct(grass):.2f}%")
        print(f"Tree mask coverage: {pct(tree):.2f}%")
        print(f"Sand mask coverage: {pct(sand):.2f}%")
        print(f"Road mask coverage: {pct(road):.2f}%")
        save_mask_images(image_file, bgr, grass, tree, sand, road)

        #Clean mask test block
        print("\nReached mask test block")
        bgr = cv2.imread(str(image_file))
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        _, raw_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        

        cleaned = clean_mask(raw_mask, k=5)

        #pct test block
        print(f"Raw mask coverage: {pct(raw_mask):.2f}%")
        print(f"Cleaned mask coverage: {pct(cleaned):.2f}%")


    else:
        print("No image file found.")

    
    
    #block is commented out since it's primarily for debugging and inspecting individual image properties found in data folder
    #print(f"Searching in: {IMAGES_DIR}")
    # image_file = get_first_image()
    # image_files = get_image_files()

   
    # if image_file:
    #     with Image.open(image_file) as image:
    #         print(f"Image: {image_file.name}")
    #         print(f"Path: {image_file}") 
    #         print(f"Format: {image.format}")
    #         print(f"Size: {image.size}")
    #         print(f"Mode: {image.mode}")
    #         print("\n")

    #     #create mask test block
    #     print("\nReached color mask test block")
    #     bgr = cv2.imread(str(image_file))
    #     grass, tree, sand, road = make_color_mask(bgr)
    #     print(f"Grass mask coverage: {pct(grass):.2f}%")
    #     print(f"Tree mask coverage: {pct(tree):.2f}%")
    #     print(f"Sand mask coverage: {pct(sand):.2f}%")
    #     print(f"Road mask coverage: {pct(road):.2f}%")

        
    #     #clean mask test block
    #     print("\nReached mask test block")
    #     bgr = cv2.imread(str(image_file))
    #     gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    #     _, raw_mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    #     cleaned = clean_mask(raw_mask, k=5)

    #     #pct test block
    #     print(f"Raw mask coverage: {pct(raw_mask):.2f}%")
    #     print(f"Cleaned mask coverage: {pct(cleaned):.2f}%")
        
    #     #analyze land cover test block
    #     print("Reached land cover analysis test block")
    #     bgr = cv2.imread(str(image_file))
    #     results = analyze_land_cover(bgr, k=5)
    #     print(f"Grass coverage: {results['grass']:.2f}%")
    #     print(f"Tree coverage: {results['tree']:.2f}%")
    #     print(f"Sand coverage: {results['sand']:.2f}%")

    #     #analyze image file test block
    #     print("\nReached image file analysis test block")
    #     file_results = analyze_image_file(image_file, k=5)
    #     print(f"File grass coverage: {file_results['grass']:.2f}%")
    #     print(f"File tree coverage: {file_results['tree']:.2f}%")
    #     print(f"File sand coverage: {file_results['sand']:.2f}%")
    #     print(f"File road coverage: {file_results['road']:.2f}%")

    #     #analyze image batch test block
    #     batch_files = image_files
    #     print(f"\nReached batch analysis test block for {len(batch_files)} images")
    #     batch_results = analyze_image_batch(batch_files, k=5)

    #     preview_count = min(10, len(batch_results))
    #     for result in batch_results[:preview_count]:
    #         print(f"{result['image_path'].name} -> grass: {result['grass']:.2f}%, tree: {result['tree']:.2f}%, sand: {result['sand']:.2f}%, road: {result['road']:.2f}%")

    #     if len(batch_results) > preview_count:
    #         print(f"... ({len(batch_results) - preview_count} more images analyzed)")

    #     avg_grass = sum(result["grass"] for result in batch_results) / len(batch_results)
    #     avg_tree = sum(result["tree"] for result in batch_results) / len(batch_results)
    #     avg_sand = sum(result["sand"] for result in batch_results) / len(batch_results)
    #     avg_road = sum(result["road"] for result in batch_results) / len(batch_results)

    #     print("Batch average coverage")
    #     print(f"Average grass coverage: {avg_grass:.2f}%")
    #     print(f"Average tree coverage: {avg_tree:.2f}%")
    #     print(f"Average sand coverage: {avg_sand:.2f}%")
    #     print(f"Average road coverage: {avg_road:.2f}%")
    # else:
    #     print("No images found in the directory.") 
        
if __name__ == "__main__":
    main()