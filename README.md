## Penrose Tiling Maker python script

### What is it?
This is a python script for generating Penrose P2 (kite and dart) tilings from user-supplied kite and dart images.

### What's in this repo?
- README.md: This file!
- kite_mask.png, dart_mask.png: Basic masks for kite and dart. Input files must be exactly the same aspect ratios.
- kite_mask.xcf, dart_mask.xcf: GIMP files of the kite and dart mask, for convenience.
- make_tiling.py: The script to run to generate a tiling.

### How do I use it?
For now, all of the constants are in the make_tiling file. Open the file, and edit the following constants:
- ITERATIONS: How many iterations to increase from the basic star. The number of tiles in the final image is an exponential function of this, so be careful!
- SCALING: How much to scale the input images. (For example, 0.25 scales down all tiles by a factor of 4.)
- KITE_IMAGE, DART_IMAGE: Input images for kite and dart.
- OUT_FILE: File name to print out to.

Then just run `python make_tiling.py`. (I might turn this into a proper CLI at some point, but this works well enough for now.)