import os
from pathlib import Path

def create_placeholder_file(file_path, content="Placeholder"):
    """
    Creates a placeholder file with the given content.
    If the file already exists, it skips creation.
    """
    if not file_path.exists():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")

def generate_soundkit_structure(base_path):
    """
    Generates a comprehensive sound kit folder structure with placeholder .nfo and .png files.
    """
    # Define the folder structure as a nested dictionary
    soundkit_structure = {
        "Drums": {
            "BassDrum": {},
            "Snare": {},
            "Toms": {
                "HighTom": {},
                "MidTom": {},
                "LowTom": {}
            },
            "Cymbals": {
                "HiHat": {},
                "Crash": {},
                "Ride": {}
            },
            "Accessories": {
                "Stands": {},
                "Pedals": {}
            }
        },
        "Bass": {
            "ElectricBass": {},
            "AcousticBass": {}
        },
        "Synths": {
            "AnalogSynth": {},
            "DigitalSynth": {}
        },
        "Guitars": {
            "ElectricGuitar": {},
            "AcousticGuitar": {}
        },
        "Vocals": {
            "LeadVocals": {},
            "BackingVocals": {}
        },
        "Effects": {
            "Reverbs": {},
            "Delays": {},
            "OtherEffects": {}
        },
        "Misc": {
            "Loops": {},
            "OneShots": {}
        },
        "Documentation": {
            "README": {}
        }
    }

    def create_structure(current_path, structure):
        for folder, subfolders in structure.items():
            folder_path = current_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {folder_path}")

            # Create placeholder .nfo and .png files in each folder, except for Documentation
            if folder != "Documentation":
                nfo_file = folder_path / f"{folder}.nfo"
                png_file = folder_path / f"{folder}.png"

                create_placeholder_file(nfo_file, content=f"{folder} information")

            # Special handling for Documentation
            else:
                # Create README.nfo and README.png in Documentation
                readme_nfo = folder_path / "README.nfo"
                readme_png = folder_path / "README.png"

                create_placeholder_file(readme_nfo, content="SoundKit Documentation")

            # Recursively create subfolders
            if isinstance(subfolders, dict):
                create_structure(folder_path, subfolders)

    create_structure(base_path, soundkit_structure)

if __name__ == "__main__":
    # Define the base path for the sound kit
    # For example, create it in the current working directory
    base_soundkit_path = Path.cwd() / "SoundKit"

    # Create the base sound kit directory
    base_soundkit_path.mkdir(parents=True, exist_ok=True)
    print(f"Created base directory: {base_soundkit_path}")

    # Generate the folder structure
    generate_soundkit_structure(base_soundkit_path)

    print("SoundKit folder structure generation complete.")
