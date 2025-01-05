# <p style="color:yellow">Public Python Package</p>


A comprehensive collection of Python utilities to boost productivity and streamline workflow.

---

#### Table of Contents

- [Public Python Package](#public-python-package)
      - [Table of Contents](#table-of-contents)
  - [Projects](#projects)
    - [Inventory System](#inventory-system)
    - [Folder Structure Generator (`folders.py`)](#folder-structure-generator-folderspy)
    - [Rainbow Metadata Generator (`nfo.py`)](#rainbow-metadata-generator-nfopy)
    - [Directory Metadata Manager (`nfo2.py`)](#directory-metadata-manager-nfo2py)
    - [File and Directory Renamer (`filenamer.py`)](#file-and-directory-renamer-filenamerpy)
    - [VS Code Snippet Generator](#vs-code-snippet-generator)
    - [Python File Combiner](#python-file-combiner)

---

## Projects

### Inventory System

A Pygame-based inventory management tool featuring a multi-tabbed grid structure for organizing items like weapons and consumables.

![Inventory System](<inv.PNG>)

- **Features**: Item stacking, drag-and-drop, hotbar slots, and responsive UI.
- **Requirements**: Python 3.x, Pygame, Pygame GUI
- **Usage**: Run using `python inventory.py`
- **Controls**: Use 'I' to toggle inventory and keys '1-4' to switch tabs.

---

### Folder Structure Generator (`folders.py`)

Automatically constructs a nested folder structure labeled "SoundKit," complete with `.nfo` placeholders.

![SoundKit Structure](<soundkit.PNG>)

- **Usage**: Execute `python folders.py` to create the structure.
- **Features**: Generates directories like Drums, Synths, and Documentation with informative `.nfo` files.

---

### Rainbow Metadata Generator (`nfo.py`)

Generates `.nfo` files with metadata using a rainbow gradient for directories and audio files.

![Rainbow Metadata](<nfo.PNG>)

- **Usage**: Run `python nfo.py <path_to_root_directory> [--generate-icons]`
- **Features**: Supports multiple audio formats, validates existing metadata, and conditions the use of a rainbow color scheme.

---

### Directory Metadata Manager (`nfo2.py`)

Creates `.nfo` files for directories using rainbow gradient coloring to ensure each directory is uniquely tagged.

- **Usage**: `python nfo2.py <path_to_root_directory>`
- **Features**: Generates metadata for subdirectories to enhance organization.

---

### File and Directory Renamer (`filenamer.py`)

Normalizes audio-related filenames and directory names by cleaning and standardizing.

- **Usage**: Use with `python filenamer.py <directory_path>`
- **Features**: Cleans unnecessary filename elements, applies title casing, and supports audio file renaming.

---

### VS Code Snippet Generator

Transforms Python code into VSCode snippets for efficient code reuse.

- **Features**: Automatic JSON snippet creation, seamless VSCode integration, and multi-version support.
- **Usage**: `python snippet_generator.py <input_file.py> <output_snippets.json>`
- **Applications**: Facilitates rapid prototyping and team standardization through reusable code templates.

---

### Python File Combiner

A script to merge multiple Python files into a single file for coherent analysis or distribution.

- **Features**: Batch processing, annotated file structure, and preventive recursion.
- **Usage**: `python combine_python_files.py <target_directory> <output_combined.py>`
- **Applications**: Ideal for project archiving and code compilation needs.

---

Stay tuned for more Python utilities and enhancements to be added.
