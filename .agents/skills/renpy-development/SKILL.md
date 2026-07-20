---
name: renpy-development
description: Guidelines for running, testing, warping, and debugging a Ren'Py project. Use when executing the game, troubleshooting compiler or runtime errors, or inspecting logs.
---

# Ren'Py Development & Debugging Skill

Use this skill when launching, testing, warping, or troubleshooting the Ren'Py game.

## Configuration Context

Optimistically assume that the path environment is already configured. If commands fail, run `python manage.py verify` to check configuration diagnostics.

*   **Project Runner:** `manage.py` is used to orchestrate all CLI commands.
*   **Local Configuration:** SDK path is defined in `.env` at the project root.

---

## 1. Game State Entity Design (Save, Load & Rollback)

All custom Python classes that represent dynamic game state (e.g., Player, GuildCharacter, InventoryItem, TimeSystem, AuctionItem, etc.) must be designed to support Ren'Py's built-in save/load and rollback systems.

### A. Subclass `renpy.store.object`
To enable Ren'Py to monitor and record attribute mutations (e.g., `character.level += 1`), classes defined in `init python:` blocks must inherit from `renpy.store.object` and invoke `super().__init__()` in their constructors:

```python
init python:
    class GuildCharacter(renpy.store.object):
        def __init__(self, char_id):
            super().__init__()
            self.id = char_id
            self.level = 1
```

### B. Use the `default` Statement for Initialization
State-holding variables and repositories must be declared at the script level using the `default` keyword, **never** via python assignments inside `init python:` blocks:

```renpy
# Correct: Registered for save files and rollback
default player = Player("Hero")
default guild_repository = GuildRepository()

# Incorrect: Treated as static/init data; will NOT be saved
init python:
    player = Player("Hero")
```

### C. Wrapping Dynamic Initializations
Because `default` variables are initialized when starting or loading a game (not at `init` time), referring to them directly in `init` blocks (e.g., for registering event handlers or time listeners) will fail with `NameError`/`AttributeError`. 
Always wrap calls to dynamic objects inside a parameterless helper function:

```python
# Correct wrapper method:
init 2 python:
    def trigger_auction_update():
        auction_house.daily_update()  # Resolves auction_house at runtime
        
    game_lifecycle_service.register_new_day_listener(trigger_auction_update, priority=50)
```

---

## 2. Launching and Running Commands

Optimistically assume the SDK path environment is already configured. If any command fails, run `python manage.py verify` to identify issues.

### Run the Game
```powershell
python manage.py run
```

### Warp to Script Lines
```powershell
python manage.py warp "game/scripts/scenes/hub_scene.rpy:<line>"
```
