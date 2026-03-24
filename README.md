This project builds a stitched aerial mosaic from overlapping drone images and performs basic land classification analysis. The system first combines multiple images into a single large mosaic, then estimates land coverage (such as trees and dirt) using color-based segmentation. 
Future phases will extend this to machine learning–based classification for improved accuracy.

Current status:
- `main.py` finds the first valid image in `data/` and prints color-coverage estimates.
- `test_runner.py` is the scratch file for testing lower-level functions while building the project.
- `analyze_color.py` contains the color segmentation pipeline for one image.
- `stitch.py` currently provides image discovery helpers; image stitching is not implemented yet.
