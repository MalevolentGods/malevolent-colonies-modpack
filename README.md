# Malevolent Colonies

Malevolent Colonies 1.3 combines the [MC-TechColonies 1.12 release](https://www.curseforge.com/minecraft/modpacks/mc-techcolonies/files/8349997) with the existing Malevolent Colonies additions.

- Minecraft 1.21.1 and NeoForge 21.1.218.
- All 134 CurseForge mod file pins match MC-TechColonies 1.12.
- All 52 upstream override files are included unchanged, covering configuration and the `kpack` data pack with MineColonies/Oritech recipe adjustments.
- [FourTwenty](https://www.curseforge.com/minecraft/mc-mods/fourtwenty) 0.5.0 is pinned to [CurseForge file `9202215`](https://www.curseforge.com/minecraft/mc-mods/fourtwenty/files/9202215), project `1308168`. CurseForge downloads it automatically; its JAR is not bundled. Existing local configuration files absent from upstream, Cliffs blueprints, Vegan Craft recipes, and menu assets are retained.

This is a customized pack, so its complete contents differ from upstream. See `modlist.html` for the pinned mod list.

To import into CurseForge, create a ZIP with `manifest.json`, `modlist.html`, and the `overrides/` directory at its root, then select **Import** in the launcher. The launcher downloads the manifest's pinned mods.

The manifest contains 135 required CurseForge entries: 134 unchanged MC-TechColonies pins plus FourTwenty 0.5.0. No manually supplied mod JAR is needed. Keep FourTwenty pinned to its exact release file and avoid also placing a copy in `overrides/mods`.

The upstream source is `TechColonies-1.12.zip`, CurseForge project `365535`, file `8349997`, released July 1, 2026. Its SHA-256 is `8887c66fe403a6b576b1d9a001f9c4fdf7b1161cb6794f40877fd9caf78f90da`.

The 1.3 sync includes upstream gameplay settings for raids, weather, Overgrowth, food milestones, and corpse ownership. Manifest parity, upstream override bytes, preserved local files, and the export archive were checked. Minecraft launch and gameplay have not been validated for this combined pack.

Upstream includes an empty `overrides/global_packs/required_data/kpack/data/oritech/recipe/crafting/prompick.json` file. It is preserved exactly; its recipe-loading behavior remains unverified in-game. All other upstream JSON and TOML files passed syntax checks.

## GitHub releases

Pushing a version tag such as `v1.3` runs `.github/workflows/release.yml`. The workflow validates the manifest, builds `Malevolent-Colonies-v1.3.zip`, and publishes it on this repository's GitHub Releases page with generated release notes. The ZIP contains `manifest.json`, `modlist.html`, and `overrides/` at its root. It uses the automatic GitHub Actions token; no additional secret is required.

Before tagging, update `manifest.json`'s version and the documentation, commit the changes (including the workflow), and test packaging locally:

```sh
python3 scripts/package_modpack.py v1.3 /tmp/malevolent-colonies-release
```

The tag without its leading `v` must exactly match the manifest version. After committing the release changes, publish the matching tag:

```sh
git tag -a v1.3 -m "Malevolent Colonies 1.3"
git push origin v1.3
```

Tags containing a prerelease suffix, such as `v1.4-rc.1`, create GitHub prereleases. Rerunning a successful workflow replaces the ZIP on the existing release without rewriting its notes. Packaging validates the export structure and manifest; it does not launch Minecraft or verify CurseForge download availability.
