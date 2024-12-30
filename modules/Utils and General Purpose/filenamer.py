import os, re, sys

def format_filename(filename, bpm):
    name, ext = os.path.splitext(filename)
    # Remove any existing BPM references first
    name = re.sub(r'\b\d{2,3}\s?bpm\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[_\-]+', '', name)
    name = re.sub(r'(?<!^)(?=[A-Z])', '', name).title()
    name = re.sub(r'\s+', ' ', name)  # Shrink multiple spaces to single space
    name = re.sub(r'B\s+P\s+M', 'BPM', name, flags=re.IGNORECASE)  # Remove spaces in BPM
    if bpm:
        name = f"{name}{int(bpm)}BPM"
    return f"{name}{ext}"

def format_dirname(dirname):
    name = re.sub(r'[_\-]+', '', dirname)
    name = re.sub(r'(?<!^)(?=[A-Z])', '', name).title()
    name = re.sub(r'\s+', ' ', name)  # Shrink multiple spaces to single space
    name = re.sub(r'B\s+P\s+M', 'BPM', name, flags=re.IGNORECASE)  # Remove spaces in BPM
    return name

def main(directory):
    for root, dirs, files in os.walk(directory, topdown=True):
        # Format and rename directories
        for i, dirname in enumerate(dirs):
            new_dirname = format_dirname(dirname)
            if new_dirname != dirname:
                old_path = os.path.join(root, dirname)
                new_path = os.path.join(root, new_dirname)
                os.rename(old_path, new_path)
                dirs[i] = new_dirname

        # Format and rename files
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                name, ext = os.path.splitext(filename)
                if ext.lower() in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.mid']:
                    bpm_match = re.search(r'\b(\d{2,3})\s?bpm\b', name, re.IGNORECASE)
                    bpm = float(bpm_match.group(1)) if bpm_match else None
                    new_name = format_filename(filename, bpm)
                    if new_name != filename:
                        new_path = os.path.join(root, new_name)
                        os.rename(filepath, new_path)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else '.')