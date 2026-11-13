# FM27 Refined Skin

A starting point for refining the default Football Manager 27 interface.
Visual changes live in `custom.uss`, after the generated native variables.

## Appearance

- Management pages use a solid `#16181D` canvas and `#1E2129` cards.
- Ordinary cards use 8px corners and a 1px white border at 8% opacity.
  Tactical status outlines and native selection/focus states keep their meaning.
- Player, staff, and manager portrait frames use rounded rectangular corners:
  3-4px for small thumbnails, 6px for medium thumbnails, and 8px for larger
  portraits. Native image sizes and cropping are retained; unrelated circular
  controls and status indicators keep their original shapes.
- Top navigation, secondary navigation, and management page shells use a 10px
  outer gutter through `--refined-content-inset`. The two navigation bars share
  a single 10px gap. Shells and their grids stretch into the remaining space,
  with auto widths to account for the margins. Tool/site and Inbox safe areas
  add no second horizontal or bottom inset. Internal card padding and native
  grid placement stay native. Exact alignment still needs an in-game check at
  the active resolution and UI scale.
- The secondary navigation texture is hidden. Navigation keeps the game's
  automatic colours and foreground contrast rules. Its bound gradients remain:
  a solid primary/secondary pair from the managed team is **not implemented**.
  The native secondary bar may change with the viewed club or competition.
- Main-menu and live/half-time/full-time match surfaces keep native palette
  values. Content images, club badges, icons, and tactical pitches are retained.

Only background image paint on management `Card-frame` elements is suppressed;
the complete interface is never targeted with a universal image-removal rule.
The full-window scene background is left intact for the match renderer.

## Visual verification

The stylesheet still requires an in-game check after **Reload Skin**. Static
checks and an installation to a temporary folder do not verify Unity rendering.

1. Visit Portal, Squad, Inbox, Recruitment, and Tactics. Check solid page surfaces,
   visible player photos/logos, ordinary card borders, and rounded rectangular
   portrait frames in player/staff lists, profiles, and the manager menu.
2. Compare content left/right/bottom edges with the top menu at your resolution
   and UI scale. Native grid-generated spacing may need further adjustment.
3. Open your club, another club, a player, and a competition. Check navigation
   text/icons on both light and dark team colours, and the unemployed state.
4. Check hover, selected, disabled, and keyboard focus states. In Tactics, verify
   pending/changed instruction outlines remain distinct from ordinary cards.
5. Enter a match and inspect highlights, the between-highlights dashboard,
   half-time/full-time reports, and the main menu after leaving the save.

No in-game rendering, click-through, or navigation contrast result has been
recorded yet. Reload Skin and capture the affected pages before treating this
visual pass as verified.

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
