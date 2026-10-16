#!/usr/bin/env python3
"""Validate a release tag and build a CurseForge import archive."""

import argparse
import json
from pathlib import Path
import re
import zipfile


def package(tag, output_dir):
    """Package the repository's import files without changing their contents."""
    root = Path(__file__).resolve().parents[1]
    if not re.fullmatch(r"v[0-9]+(?:\.[0-9]+)+(?:-[0-9A-Za-z.-]+)?", tag):
        raise ValueError("Use a version tag such as v1.3, v1.3.1, or v1.4-rc.1")

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if manifest["version"] != tag[1:]:
        raise ValueError(
            f"Tag {tag} does not match manifest version {manifest['version']}"
        )
    if manifest.get("manifestType") != "minecraftModpack" or manifest.get("manifestVersion") != 1:
        raise ValueError("Expected a CurseForge minecraftModpack manifest version 1")
    if manifest.get("overrides") != "overrides":
        raise ValueError("The manifest must use the overrides/ directory")

    projects = set()
    for entry in manifest["files"]:
        for key in ("projectID", "fileID"):
            if type(entry[key]) is not int or entry[key] <= 0:
                raise ValueError(f"Invalid {key}: {entry[key]!r}")
        if entry["projectID"] in projects:
            raise ValueError(f"Duplicate project ID: {entry['projectID']}")
        if type(entry.get("required")) is not bool:
            raise ValueError("Each mod must have a boolean required field")
        projects.add(entry["projectID"])

    overrides = root / "overrides"
    if not overrides.is_dir():
        raise ValueError("Missing overrides/ directory")
    files = [root / "manifest.json", root / "modlist.html"]
    files.extend(sorted(path for path in overrides.rglob("*") if path.is_file()))
    for path in files:
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Expected a regular file: {path.relative_to(root)}")

    output_dir = Path(output_dir).resolve()
    if output_dir == overrides or overrides in output_dir.parents:
        raise ValueError("Write release archives outside overrides/")
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"Malevolent-Colonies-{tag}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as exported:
        for path in files:
            exported.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as exported:
        if exported.testzip() is not None:
            raise ValueError("Archive integrity check failed")
    print(f"Created {archive} ({len(files)} files, {len(projects)} mod pins)")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="Release tag matching manifest.json, e.g. v1.3")
    parser.add_argument("output_dir", help="Directory for the generated ZIP")
    args = parser.parse_args()
    try:
        package(args.tag, args.output_dir)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
