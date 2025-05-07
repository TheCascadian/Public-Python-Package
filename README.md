# Public Python Package

A comprehensive collection of Python utilities to boost productivity and streamline workflow.

---

### Table of Contents

- [Overview](#overview)
  - [Inventory System](#inventory-system)
  - [Folder Structure Generator (`folders.py`)](#folder-structure-generator-folderspy)
  - [Rainbow Metadata Generator (`nfo.py`)](#rainbow-metadata-generator-nfopy)
  - [Directory Metadata Manager (`nfo2.py`)](#directory-metadata-manager-nfo2py)
  - [File and Directory Renamer (`filenamer.py`)](#file-and-directory-renamer-filenamerpy)
  - [VS Code Snippet Generator](#vs-code-snippet-generator)
  - [Python File Combiner](#python-file-combiner)

---

## Overview

### Inventory System

A fully interactive inventory management interface powered by Pygame. Built for extensibility, this system supports modular item types, a responsive UI, and drag-and-drop interaction.

![Inventory System](<inv.PNG>)

- Tabbed categorization (Weapons, Armor, Consumables, Materials)
- Drag-to-hotbar functionality with tooltip integration
- Real-time debug toggling and dynamic resolution support
- Controls: `I` toggles inventory, `1-4` switch tabs

---

### Folder Structure Generator (`folders.py`)

Instantly scaffold complex directory trees for sound design, sample packs, or modular projects. Includes intelligent placeholder `.nfo` and `.png` generation to maintain structure integrity.

![SoundKit Structure](<soundkit.PNG>)

- Recursively generates labeled subdirectories for Drums, Bass, Synths, Vocals, and more
- Each folder includes metadata placeholders for improved asset documentation
- Ideal for producers, sound engineers, or asset-heavy projects

---

### Rainbow Metadata Generator (`nfo.py`)

Enhance your audio directories with vibrant, auto-generated `.nfo` metadata using a consistent rainbow gradient scheme.

![Rainbow Metadata](<nfo.PNG>)

- Validates and updates metadata for audio files and folders
- Supports `.wav`, `.mp3`, `.flac`, `.mid`, and other common formats
- Command-line usage: `python nfo.py <target_dir> [--generate-icons]`

---

### Directory Metadata Manager (`nfo2.py`)

Streamlines bulk tagging of folder hierarchies. Applies the same gradient logic from `nfo.py` to top-level directories for rapid organization.

- Traverse a root directory and apply structured `.nfo` metadata
- Avoids duplication by checking existing files for compliance
- Ideal for maintaining large, nested sample libraries

---

### File and Directory Renamer (`filenamer.py`)

Standardize naming conventions for large batches of audio files and folders. Cleans, formats, and appends BPM info with zero manual input.

- Auto-formats `CamelCase`, `snake_case`, or cluttered filenames into readable, consistent titles
- Parses embedded BPM and reinserts in standardized format
- Supports `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, and `.mid`

---

### VS Code Snippet Generator

Convert any Python script into a valid Visual Studio Code snippet file for rapid reuse and team-wide standardization.

- Extracts Python blocks and serializes to `.json` snippet format
- Useful for internal libraries, templates, or educational modules
- Run via: `python snippet_generator.py <input.py> <output.json>`

---

### Python File Combiner

Aggregate an entire codebase into a single file for archival, distribution, or inline documentation.

- Preserves file boundaries with annotated comments
- Prevents recursive inclusion and excludes unwanted artifacts
- Command-line: `python combine_python_files.py <source_dir> <output.py>`

---

This toolkit is designed for builders who want maximum efficiency with minimal complexity. More modules and enhancements will be added to expand its capabilities and streamline even more layers of your workflow.
