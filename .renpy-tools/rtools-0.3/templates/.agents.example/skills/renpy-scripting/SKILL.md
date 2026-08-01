---
name: renpy-scripting
description: Guidelines and syntax rules for writing, editing, and formatting Ren'Py script (.rpy) files. Use when adding dialogue, character definitions, choice menus, variables, or game logic.
---

# Ren'Py Scripting Skill

Use this skill when writing or refactoring Ren'Py script (`.rpy`) files and embedded Python code. It ensures compliance with Ren'Py 8.x (Python 3) execution standards, save/rollback mechanics, and clean code architecture.

## Guidelines & Best Practices

### 1. Variables: `define` vs `default`
- **Use `define`** for constant, read-only objects or configuration that do not change during gameplay:
  ```renpy
  define e = Character("Eileen", color="#c8ffc8")
  define config.name = "My Visual Novel"
  define persistent.unlocked_gallery = False
  ```
- **Use `default`** for state variables that change during gameplay and must be saved in save files and tracked by rollback:
  ```renpy
  default intelligence = 10
  default met_eileen = False
  default player = Player("Hero")
  ```
- **CRITICAL:** Never initialize state-holding variables inside `init python:` blocks or top-level python assignments. Variables declared in `init python:` are treated as static constants and will **not** be saved in save files or restored during rollback.

### 2. Python 3 Integration & OOP Best Practices
Ren'Py 8.x runs natively on Python 3. Follow modern Python standard practices:

- **Type Hints:** Use Python type annotations across models, services, and helper functions:
  ```python
  init python:
      from typing import Optional, List, Dict

      def calculate_damage(attacker_power: int, defender_armor: int) -> int:
          return max(1, attacker_power - defender_armor)
  ```
- **Properties (`@property`):** Use properties for calculated state to eliminate redundant state duplication:
  ```python
  init python:
      class Player(renpy.store.object):
          def __init__(self, name: str, base_atk: int) -> None:
              super().__init__()
              self.name = name
              self.base_atk = base_atk
              self.equipment_bonus = 0

          @property
          def total_attack(self) -> int:
              return self.base_atk + self.equipment_bonus
  ```
- **Dataclasses Caution:** Standard `@dataclass` decorators do not automatically inherit from `renpy.store.object`. If using dataclasses for state, explicitly inherit from `renpy.store.object` or ensure custom `__setattr__` behavior.

### 3. Dialogue & Script Flow
- Always use defined character objects rather than raw strings:
  ```renpy
  # Recommended:
  e "Hello, traveler!"

  # Avoid:
  "Eileen" "Hello, traveler!"
  ```
- Dialogue lines and narration are wrapped in double quotes.
- Use string interpolation with bracket notation `[variable]` or `[object.attribute]`:
  ```renpy
  e "Welcome, [player.name]! You currently have [player.gold] gold."
  ```

### 4. Choice Menus & Branching
- Indent choice menus using 4 spaces per nesting level.
- Provide descriptive narrative prompts or labels inside menu blocks:
  ```renpy
  menu:
      "What should you do next?"

      "Explore the ancient ruins":
          jump explore_ruins

      "Return to the tavern":
          jump return_tavern
  ```

### 5. Screen Language & UI Presentation
- **No Side-Effects in Screens:** Ren'Py screens are evaluated repeatedly during mouse movement and interaction frames. **Never** mutate state or call logic functions directly in the screen body (e.g. `$ player.gold += 10`).
- **Use Screen Actions:** Perform all state mutations, navigation, or function calls via Screen Actions:
  ```renpy
  screen inventory_item(item):
      textbutton "Use [item.name]":
          action Function(inventory_service.use_item, item)
  ```
- **Modularize Screens with `use`:** Break complex user interfaces into smaller, reusable screen components:
  ```renpy
  screen main_hud():
      use player_stats_bar(player=player)
      use minimap_widget
  ```

### 6. Image Display & Transitions
- Use `scene` to reset background state.
- Use `show` / `hide` to manage sprites.
- Combine display statements with `with` transitions (`fade`, `dissolve`, `moveinright`):
  ```renpy
  scene bg tavern with fade
  show eileen happy at right with dissolve
  ```

### 7. Static Data & Dictionaries Separation
- **Place Static Data in `game/scripts/dictionaries/` or `game/data/`:** Store static item definitions, base stats, text templates, task tables, and loot probabilities in dedicated database `.rpy` or `.py` modules (e.g. `items_db.rpy`, `quest_db.rpy`).
- **Avoid Inline Configuration:** Keep logic services, screens, and labels free of inline configuration constants by loading them from static dictionaries.

## References & Documentation
- [Ren'Py Language Basics](https://www.renpy.org/doc/html/language_basics.html)
- [Defining Characters & Dialogue](https://www.renpy.org/doc/html/dialogue.html#defining-characters)
- [Displaying Images & Transitions](https://www.renpy.org/doc/html/displaying_images.html)
- [Choice Menus](https://www.renpy.org/doc/html/menus.html)
- [Python Integration in Ren'Py](https://www.renpy.org/doc/html/python.html)
- [Ren'Py 8.x Screen Language Reference](https://www.renpy.org/doc/html/screens.html)
