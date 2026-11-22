#!/usr/bin/env python3

from pathlib import Path

# Change this to the directory containing the Family Historian output.
ROOT = Path("genealogy")

# Find all files whose names start with an underscore.
files = [
    path for path in ROOT.rglob("*")
    if path.is_file() and path.name.startswith("_")
]

# Build a mapping of old filenames to new filenames.
renames = {}

for path in files:
    new_name = "fh-" + path.name[1:]
    new_path = path.with_name(new_name)

    if new_path.exists():
        print(f"Skipping rename: {path} -> {new_path} (destination exists)")
        continue

    renames[path.name] = new_name

# Rename the files.
for path in files:
    if path.name not in renames:
        continue

    new_path = path.with_name(renames[path.name])
    print(f"Renaming: {path} -> {new_path}")
    path.rename(new_path)

# Update references in HTML files.
for path in ROOT.rglob("*.html"):
    content = path.read_text(encoding="utf-8")

    original = content

    for old_name, new_name in renames.items():
        content = content.replace(old_name, new_name)

    if content != original:
        print(f"Updating references in: {path}")
        path.write_text(content, encoding="utf-8")

print("Family Historian HTML processing complete.")
