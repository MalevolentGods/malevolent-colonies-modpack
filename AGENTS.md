# Repository Guidelines

## Project Structure

This repository is a CurseForge modpack export, not a Java mod source tree.

- `manifest.json` defines Minecraft, NeoForge, pack metadata, and pinned CurseForge project/file IDs.
- `modlist.html` lists those pins and bundled mods; keep it synchronized with the manifest.
- `overrides/config/` contains mod configuration.
- `overrides/global_packs/required_data/` contains upstream `kpack` adjustments and local Vegan Craft recipes.
- `overrides/blueprints/` contains Cliffs structures; `overrides/packmenu/` contains menu assets.
- `overrides/mods/` holds bundled JARs, currently Four Twenty.
- `README.md` records upstream provenance, local additions, import instructions, and validation limits.

There are no source compilation tasks, test directories, or automated test frameworks configured.

## Development and Validation Commands

Run commands from the repository root:

```sh
python3 -m json.tool manifest.json > /dev/null
zip -r /tmp/malevolent-colonies-review.zip manifest.json modlist.html overrides
unzip -t /tmp/malevolent-colonies-review.zip
```

These commands check manifest syntax, create an importable export, and verify archive integrity. Use a fresh ZIP destination each time; updating an existing ZIP can retain deleted entries. Import the archive into a separate CurseForge profile to launch and test it.

## Formatting and Naming

Use two-space indentation in `manifest.json`. Preserve existing formatting in JSON, JSON5, TOML, and upstream files; no formatter or linter is configured. Preserve resource namespaces, blueprint paths, filenames, and registry identifiers. Name bundled mods with their released version, such as `fourtwenty-0.5.0.jar`, and avoid duplicate versions.

## Testing Guidelines

Check unique project IDs, pinned-file links, loader compatibility, and archive root layout. For upstream synchronizations, compare manifest pins and override bytes against the downloaded release; preserve unrelated local additions.

Validate changed JSON and TOML with appropriate parsers. The upstream `kpack/data/oritech/recipe/crafting/prompick.json` is intentionally retained empty; document this exception rather than silently repairing it.

Test affected recipes, colony behavior, and menus in a disposable world. Report static checks separately from successful launch and gameplay checks; no coverage threshold is configured.

## Commits and Pull Requests

History uses short Conventional Commit messages, including `chore: bump version of fourtwenty mod` and `feat: bump version of fourtwenty`. Follow that pattern and keep changes focused.

PRs should describe changed mods/configuration, upstream release links, preserved customizations, and validation results. Link relevant issues and include screenshots for visible menu or blueprint changes. Update pack version and documentation when preparing a release. Preserve existing staged and uncommitted work.
