---
name: renpy-scripting
description: Guidelines and syntax rules for writing, editing, and formatting Ren'Py script (.rpy) files. Use when adding dialogue, character definitions, choice menus, variables, or game logic.
---

# Ren'Py Scripting Skill

Use this skill when writing or refactoring Ren'Py script (`.rpy`) files. It ensures that the game code complies with Ren'Py's execution model and syntax best practices.

## Guidelines & Best Practices

### 1. Variables: `define` vs `default`
- **Use `define`** for constant objects that do not change during gameplay (e.g., character declarations, transitions, audio tracks).
  ```renpy
  define e = Character("Eileen", color="#c8ffc8")
  define persistent.unlocked_gallery = False
  ```
- **Use `default`** for variables whose values change during gameplay and need to be saved in save files (e.g., stats, choice flags, progress tracking).
  ```renpy
  default intelligence = 10
  default met_eileen = False
  ```
- **Never initialize variables** with python blocks at init time if they are meant to change during gameplay, as this breaks the save/load system.

### 2. Dialogue & Characters
- Always use the defined character variable rather than raw strings for speaking characters.
  ```renpy
  # Good:
  e "Hello, player!"
  # Bad:
  "Eileen" "Hello, player!"
  ```
- Dialogue lines should be wrapped in double quotes. Narration (lines with no character name) also goes in double quotes.

### 3. Choice Menus
- Indent choice menus correctly using 4 spaces.
- Always include an optional menu label or narrative line if needed.
- Each choice block should lead to a `jump` or execute quick logic and continue.
  ```renpy
  menu:
      "Go to the forest":
          jump forest_start
      "Go to the town":
          jump town_start
  ```

### 4. Image Display
- Use `scene` to clear the screen and set a background.
- Use `show` to display a character sprite.
- Use `hide` to remove a character sprite.
- Use `with` to apply transitions (e.g., `fade`, `dissolve`).
  ```renpy
  scene bg room with fade
  show eileen happy at right with dissolve
  ```

### 5. Python Integration (Python 3 / Ren'Py 8.x)
- **Python 3 Compatibility:** Because we are on Ren'Py 8.5.3, all Python blocks run in Python 3. Do not use legacy Python 2 syntax.
  - Print statement is a function: `print("Message")` instead of `print "Message"`.
  - Division `/` returns a float (true division); use `//` for integer floor division.
  - Unicode strings are standard (no need for `u"string"` prefixes).
- Use a single-line python statement starting with `$` for quick operations.
  ```renpy
  $ player_gold += 50
  ```
- Use a multi-line `python:` block for more complex logic.
  ```renpy
  python:
      if player_gold >= 100:
          can_buy = True
      else:
          can_buy = False
  ```

## References & Documentation
- [Ren'Py Language Basics](https://www.renpy.org/doc/html/language_basics.html)
- [Defining Characters & Dialogue](https://www.renpy.org/doc/html/dialogue.html#defining-characters)
- [Displaying Images & Transitions](https://www.renpy.org/doc/html/displaying_images.html)
- [Choice Menus](https://www.renpy.org/doc/html/menus.html)
- [Python Integration in Ren'Py](https://www.renpy.org/doc/html/python.html)
- [Ren'Py 8.x Screen Language Reference](https://www.renpy.org/doc/html/screens.html)


