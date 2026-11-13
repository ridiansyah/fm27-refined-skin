# FM27 Refined Skin

A starting point for refining the default Football Manager 27 interface.
The skin currently keeps the native appearance; visual changes belong in
`custom.uss`.

## Setup

Install Python 3 with venv support and keep a local copy of Football Manager 27.
The extraction script downloads UnityPy using pip, so it needs internet access.

On macOS, open a terminal in this repository and run:

```sh
./extract.sh
./install.sh
```

Extraction creates `variables.uss` and `reference/` from your own game files.
These generated files stay local and are excluded from Git.

The default game path is the macOS Steam installation. For another installation,
set the folder containing `ui-styles_assets_*.bundle`:

```sh
FM27_GAME_DIR="/path/to/StandaloneOSX" ./extract.sh
```

To choose another installation destination:

```sh
FM27_SKINS_DIR="/path/to/skins" ./install.sh
```

In Football Manager, select **FM27 Refined Skin** in Preferences and apply it.
After editing, run `./install.sh` again and use **Reload Skin** in the game.
The installation script copies only the four runtime files.

For Windows, run the Python extraction tools against your local game bundles,
then copy `skin.json`, `main.uss`, `variables.uss`, and `custom.uss` into
`Documents/Sports Interactive/Football Manager 27/skins/FM27 Refined Skin/`.
The shell scripts target macOS; Windows extraction has not been verified.

## Files

| Path | Purpose |
| --- | --- |
| `skin.json` | Loads `main.uss` |
| `main.uss` | Loads native variables, then personal overrides |
| `custom.uss` | Personal changes; never overwritten by extraction |
| `variables.uss` | Generated native variables; overwritten by extraction |
| `reference/` | Generated native stylesheets for selector lookup; not loaded |
| `tools/` | Scripts for extracting and preparing native styles |

Find selectors in `reference/AlwaysAppliedStyleSheet.uss`, then add only the
properties you want to change to `custom.uss`. Put variable overrides in a
`:root` block there. Keep edits out of generated files so extraction preserves
your work.

After a game update, run `./extract.sh`, then `./install.sh`, and reload the skin.
If a change stops working, check whether the game's selector has changed.

## Native assets

Generated styles come from your own installation and remain local. They are
not included in this repository. Image, font, and cursor assets that cannot be
represented as text keep their native game values. Variables overridden by
special game styles are commented out during extraction to preserve those
states.

Some player and club names use native rich text, which stylesheet overrides
cannot fully recolor. Unity reference source files in `tools/unityref/` retain
their original copyright and license notices.
