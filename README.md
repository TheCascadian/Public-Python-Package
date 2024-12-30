# Public Python Package

A collection of Python projects and utilities.

## Projects

### Inventory System

A simple inventory system built with Pygame that includes:

#### Features
- Grid-based inventory with multiple tabs (Weapons, Armor, Consumables, Materials)
- 10-slot hotbar
- Drag and drop functionality 
- Item stacking with quantity display
- Resizable window support
- Tab switching with number keys (1-4)
- Toggle inventory visibility with 'I' key

#### Requirements
- Python 3.x
- Pygame
- Pygame GUI

#### Usage
Run the inventory system:

python inventory.py

#### Controls
- I: Toggle inventory
- 1-4: Switch inventory tabs
- Left mouse: Drag and drop items
- Mouse hover: View item tooltips

#### Item Properties
Items have the following properties:
- Shape (circle, rectangle, triangle)
- Color
- Tooltip
- Quantity

#### Grid Layout
- Main Inventory: 8x5 grid
- Hotbar: 10 slots
- Each slot displays the item's shape and quantity

### Folder Structure Generator (folders.py)

Generates a comprehensive folder structure for a sound kit with placeholder .nfo and .png files.

#### Usage
Place the script in your working directory. Run the script directly:

python folders.py

This creates a SoundKit folder with a nested structure.

#### Features
- Generates the following directories: Drums, Bass, Synths, Guitars, Vocals, Effects, Misc, Documentation
- Adds placeholder .nfo files in each folder
- Includes a README.nfo file in the Documentation folder

### Rainbow Metadata Generator (nfo.py)

Generates or validates .nfo files for folders and audio files, using a rainbow gradient color scheme.

#### Usage
Execute the script:

python nfo.py <path_to_root_directory> [--generate-icons]

Replace <path_to_root_directory> with the directory path containing files or subdirectories.
Use --generate-icons to create .png files (requires Pillow).

#### Features
- Supports .wav, .mp3, .flac, .aiff, .aac, .ogg, .wma, .mid, .fst
- Validates existing .nfo files and updates metadata if mismatched
- Assigns unique colors to .nfo files based on a rainbow gradient

### Directory Metadata Manager (nfo2.py)

Generates .nfo files for subdirectories in a root directory with rainbow gradient coloring.

#### Usage
Run the script with the target directory:

python nfo2.py <path_to_root_directory>


#### Features
- Creates .nfo files with metadata for subdirectories
- Assigns rainbow gradient colors for uniqueness

### File and Directory Renamer (filenamer.py)

Standardizes and formats filenames and directory names.

#### Usage
Provide the target directory path:

python filenamer.py <directory_path>

#### Features
- Cleans up filenames:
  - Removes unnecessary spaces or underscores in "BPM"
  - Formats names in title case
- Renames directories and supported audio files (.mp3, .wav, .flac, .aac, .ogg, .mid)

### Future Additions
Stay tuned for more Python projects and utilities to be added to this package.
