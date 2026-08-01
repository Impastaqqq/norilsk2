---
name: renpy-development
description: Guidelines for running, testing, warping, and debugging a Ren'Py project. Use when executing the game, troubleshooting compiler or runtime errors, or inspecting logs.
---

# Ren'Py Development & Debugging Skill

Use this skill when launching, testing, warping, or troubleshooting a Ren'Py game.

## Configuration Context

Optimistically assume that the path environment is already configured. If commands fail, run `python manage.py verify` to check configuration diagnostics.

*   **Project Runner:** `manage.py` orchestrates all CLI commands.
*   **Local Configuration:** SDK path is defined in `.env` at the project root (`RENPY_SDK_PATH`).

---

## 1. Game State Entity Design (Save, Load & Rollback)

All custom Python classes that represent dynamic game state (e.g., `Player`, `Character`, `Inventory`, `QuestTracker`, `TimeSystem`) must be designed to support Ren'Py's built-in save/load and rollback systems.

### A. Subclass `renpy.store.object`
To enable Ren'Py to monitor and record attribute mutations (e.g., `character.level += 1`), classes defined in `init python:` blocks must inherit from `renpy.store.object` and invoke `super().__init__()` in their constructors:

```python
init python:
    class Character(renpy.store.object):
        def __init__(self, char_id: str, name: str) -> None:
            super().__init__()
            self.id = char_id
            self.name = name
            self.level = 1
```

### B. Use the `default` Statement for Initialization
State-holding variables and repositories must be declared at the script level using the `default` keyword, **never** via python assignments inside `init python:` blocks:

```renpy
# Correct: Registered for save files and rollback tracking
default player = Player("Hero")
default character_repository = CharacterRepository()

# Incorrect: Treated as static/init data; will NOT be saved
init python:
    player = Player("Hero")
```

### C. Mutating Collections Safely
When modifying lists or dictionaries in default variables, modify existing collection instances in-place or reassign them cleanly to ensure rollback records changes:
```python
# In-place mutations on default lists/dicts are tracked:
$ player.inventory.append(item)
$ character_repository.members[char_id] = character
```

### D. Wrapping Dynamic Initializations
Because `default` variables are initialized when starting or loading a game (not at `init` time), referring to them directly in `init` blocks (e.g., for registering event handlers or time listeners) will fail with `NameError`/`AttributeError`. 
Always wrap calls to dynamic objects inside a parameterless helper function:

```python
# Correct wrapper method:
init 2 python:
    def trigger_daily_update():
        time_system.daily_update()  # Resolves time_system at runtime when triggered
        
    game_lifecycle_service.register_new_day_listener(trigger_daily_update, priority=50)
```

---

## 2. Developer Interactive Debugging Tools

During engine execution, utilize Ren'Py's built-in developer shortcuts:

- **`Shift+D` Developer Menu:** Access variable viewers, displayable inspectors, image location tools, and screen diagnostics.
- **`Shift+O` Interactive Console:** Open live Python console to inspect state, test function calls, or evaluate expressions directly.
- **`Shift+R` Reload:** Instantly reload `.rpy` scripts without restarting the game client.
- **Diagnostic Logging (`renpy.log`):** Use `renpy.log("Message")` to append diagnostic output directly to `log.txt` in the game directory.

---

## 3. Launching and Running Commands via `manage.py`

Use `manage.py` for CLI orchestration:

### Run the Game
```powershell
python manage.py run
```

### Warp to Script Lines
Skip directly to a specific script file and line number:
```powershell
python manage.py warp "game/scripts/scenes/hub_scene.rpy:45"
```

### Run Static Analysis & Asset Integrity Checks
```powershell
python manage.py check
```

### Run Ren'Py Linting
```powershell
python manage.py lint
```

### Run Automated Tests
```powershell
python manage.py test global -s
```

### Clean Orphaned `.rpyc` Compiled Files
When renaming or moving `.rpy` script files, clean compiled `.rpyc` files to prevent stale script definitions from persisting:
```powershell
python manage.py clean -v
```

### Verify Local SDK Configuration
```powershell
python manage.py verify
```
