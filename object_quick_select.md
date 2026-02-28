# Quick Object Select — Blender Addon

A keyboard-driven object selector for Blender 3.1+. No mouse needed — open a search widget, type to filter, and select objects entirely from the keyboard.

---

## Installation

1. Download `object_quick_select.py`
2. In Blender, go to **Edit → Preferences → Add-ons → Install**
3. Select the file and enable the addon

---

## Opening the Widget

Press **Alt+F** in the 3D Viewport.

A centered search box appears with the full object list shown immediately in a dropdown below it.

---

## Keyboard Reference

| Key | Action |
|---|---|
| **Type letters** | Filter the list live; matching portion highlights in cyan |
| **↑ / ↓** | Move through results |
| **Page Up / Down** | Jump by a full page |
| **Tab** | Cycle to the next match without selecting |
| **Enter** | Select highlighted object (deselects others first) |
| **Shift+Enter** | Add highlighted object to existing selection |
| **Ctrl+Enter** | Select **all** objects in the current filtered list |
| **Ctrl+Shift+Enter** | Add **all** filtered objects to existing selection |
| **Backspace** | Delete last character |
| **Ctrl+Backspace** | Clear the entire search query |
| **Esc** | Cancel and close without selecting |

---

## Features

- **Live filtering** — the list updates as you type; matched characters are highlighted in blue
- **Object type hints** — each row shows the object type (Mesh, Light, Camera…) on the right, dimmed
- **Count badge** — the search box always displays how many objects match the current filter (e.g. `5 objs`), so you know before committing
- **Select all filtered** — `Ctrl+Enter` grabs everything matching your query in one keystroke; the input border flashes green as confirmation
- **Scrollable list** — up to 12 rows visible at once; navigates smoothly with arrow keys or Page Up/Down

---

## Example Workflow

You have 80 objects in your scene and want to select everything prefixed `ZZ_`:

1. Press **Alt+F** to open the widget
2. Type `ZZ` — the list narrows to only matching objects; the badge shows e.g. `5 objs`
3. Press **Ctrl+Enter** — all 5 are selected instantly
