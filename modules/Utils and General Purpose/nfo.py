import os
from pathlib import Path
import colorsys
import argparse

# Define supported audio file extensions
AUDIO_EXTENSIONS = {'.wav', '.mp3', '.flac', '.aiff', '.aac', '.ogg', '.wma', '.mid', '.midi', '.fst'}

# Template for .nfo files
NFO_TEMPLATE = """Color={color}
IconIndex=33
HeightOfs=5
SortGroup=8
Tip={name}
----------------
 

// Kit template by ProphetPNW 
ig - @ProphetPNW
sc - @prophetpnw
"""

def get_rainbow_color(position, total_positions):
    """
    Generates a color from the rainbow spectrum based on the position.
    """
    if total_positions == 1:
        hue = 0  # Default to red if only one position
    else:
        hue = (position / total_positions) * 360  # Spread hues evenly across positions

    # Convert hue to RGB
    h = hue / 360  # Normalize hue to [0,1] for colorsys
    s = 1.0        # Full saturation
    v = 1.0        # Full brightness
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r_hex = int(r * 255)
    g_hex = int(g * 255)
    b_hex = int(b * 255)
    return f"${r_hex:02X}{g_hex:02X}{b_hex:02X}"

def generate_nfo_content(color_hex, name):
    """
    Generates the content for the .nfo file based on the template.
    """
    return NFO_TEMPLATE.format(color=color_hex, name=name)

def parse_existing_nfo(nfo_path):
    """
    Parses an existing .nfo file to extract its key-value pairs.
    """
    metadata = {}
    try:
        with open(nfo_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    metadata[key.strip()] = value.strip()
        return metadata
    except Exception as e:
        print(f"Error reading {nfo_path}: {e}")
        return {}

def compare_metadata(existing_metadata, desired_metadata):
    """
    Compares existing metadata with desired metadata.
    """
    for key, value in desired_metadata.items():
        if key not in existing_metadata or existing_metadata[key] != value:
            return False
    return True

def create_or_validate_nfo(path, color_hex, is_folder, root_path):
    """
    Creates a new .nfo file or validates and updates an existing one.
    For folders, the .nfo file is placed in the root_path.
    """
    name = path.name
    desired_content = generate_nfo_content(color_hex, name)
    desired_metadata = {
        "Color": color_hex,
        "IconIndex": "33",
        "HeightOfs": "5",
        "SortGroup": "8",
        "Tip": f"PROPHET SOUNDKIT | {name}"
    }

    if is_folder:
        nfo_path = root_path / f"{path.name}.nfo"
    else:
        nfo_path = path.with_suffix('.nfo')
        
    if nfo_path.exists():
        existing_metadata = parse_existing_nfo(nfo_path)
        if compare_metadata(existing_metadata, desired_metadata):
            return
        else:
            print(f"Updating .nfo file: {nfo_path}")
    else:
        print(f"Creating .nfo file: {nfo_path}")

    try:
        with open(nfo_path, 'w', encoding='utf-8') as nfo_file:
            nfo_file.write(desired_content)
        print(f"Successfully wrote .nfo file: {nfo_path}")
    except Exception as e:
        print(f"Error writing .nfo for {path}: {e}")

def traverse_and_generate(root_path, enable_pillow=False):
    """
    Traverses the root_path directory and generates/validates .nfo files with a rainbow gradient.
    """
    if not root_path.exists() or not root_path.is_dir():
        print(f"The provided path does not exist or is not a directory: {root_path}")
        return

    # Gather all audio files and folders in traversal order
    all_items = []
    folders = []
    
    for item in root_path.rglob('*'):
        if item.is_file() and item.suffix.lower() in AUDIO_EXTENSIONS:
            all_items.append((item, False))
        elif item.is_dir() and not any(p.name.startswith('.') for p in item.parents):
            folders.append(item)
    
    # Sort folders by depth (deeper folders first) and add them to all_items
    folders.sort(key=lambda x: len(x.parts), reverse=True)
    for folder in folders:
        all_items.append((folder, True))

    total_items = len(all_items)

    if total_items == 0:
        print("No audio files or folders found in the provided directory.")
        return

    print(f"Found {total_items} items. Generating/Validating .nfo files with rainbow gradient...\n")

    for index, (item, is_folder) in enumerate(all_items):
        # Calculate color based on traversal order
        color_hex = get_rainbow_color(index, total_items)

        # Create or validate .nfo file
        create_or_validate_nfo(item, color_hex, is_folder, root_path)

    print("\nMetadata generation and validation complete.")

def main():
    """
    Main function to execute the script.
    """
    parser = argparse.ArgumentParser(description="Generate and validate .nfo files for each audio file and folder with a rainbow gradient.")
    parser.add_argument(
        "input_directory",
        type=str,
        help="Path to the root directory containing the audio files."
    )
    parser.add_argument(
        "--generate-icons",
        action="store_true",
        help="Enable generation of .png icon files with text labels using Pillow."
    )
    args = parser.parse_args()

    input_dir = Path(args.input_directory).resolve()
    traverse_and_generate(input_dir, enable_pillow=args.generate_icons)

if __name__ == "__main__":
    main()
