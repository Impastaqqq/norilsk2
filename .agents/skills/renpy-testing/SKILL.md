---
name: renpy-testing
description: Guidelines and setup for creating, executing, and debugging automated unit tests and verification in Ren'Py.
---

# Skill: Ren'Py Testing and Verification

## Overview
This skill covers the standard operating procedure for creating, structuring, running, and debugging automated tests in this Ren'Py project.

---

## 1. Test File Structure and Location
- **Location:** All logic tests must reside in `game/scripts/tests/`. Ren'Py automatically scans this directory when running test commands.
- **Naming:** Files must be named `test_<service_name>.rpy`.
- **Structure:** Use the `testsuite` and `testcase` statements.
  - A `testsuite` groups related test cases.
  - A `testcase` contains the logic blocks for specific scenarios.
  
```renpy
testsuite service_name_tests:
    setup:
        # Runs before the testsuite starts
        python:
            # Set up mocks or verify imports
            pass

    testcase test_feature_name:
        # Single-line python commands
        $ player = player_repository.get_player()
        $ player.money = 500
        
        # Test assertion
        assert eval("player.money == 500")
```

---

## 2. Writing Test Assertions
- **Syntax:** When using `assert` inside a `testcase`, wrap the condition in `eval("...")`.
- **Example:**
  - `assert eval("variable == expected_value")`
- **State Isolation:** Always reset relevant model state (e.g., `guild_repository`, `player.inventory`, `time_system`) at the beginning of each `testcase` to ensure test isolation.

---

## 3. Entity Save, Load & Rollback Testing

When validating that custom state-holding entities support Ren'Py's rollback and save systems, apply the following testing strategies:

### A. Structural Verification (Inheritance)
Verify that all game state classes correctly inherit from `renpy.store.object`:
```python
    testcase test_structural_inheritance:
        python:
            assert issubclass(Player, renpy.store.object), "Player must subclass renpy.store.object"
            assert issubclass(GuildCharacter, renpy.store.object), "GuildCharacter must subclass renpy.store.object"
```

### B. Serialization (Save/Load) Verification
Use Python's built-in `pickle` module to verify that entities serialize and deserialize cleanly without throwing errors, preserving all mutated attributes. This mirrors Ren'Py's internal saving behavior:
```python
    testcase test_serialization_integrity:
        python:
            import pickle
            
            p = Player("Test", 100)
            data = pickle.dumps(p)
            loaded = pickle.loads(data)
            
            assert loaded.name == "Test"
            assert loaded.money == 100
```

### C. Behavioral Rollback Verification (Simulation)
To programmatically test that the rollback mechanism works, you can call `renpy.checkpoint()` and `renpy.rollback()`. To prevent infinite execution loops during rollback, use a phase sentinel object subclassing `NoRollback`:

```python
init python:
    class RollbackSentinel(NoRollback):
        def __init__(self):
            self.phase = "init"

default test_sentinel = RollbackSentinel()
default test_character = GuildCharacter("Alora")

label test_rollback_behavior:
    if test_sentinel.phase == "init":
        $ test_character.level = 10
        $ renpy.checkpoint()  # Establish checkpoint
        
        $ test_character.level = 20
        $ test_sentinel.phase = "mutated"
        $ renpy.rollback()    # Roll back state and execution pointer
        
    elif test_sentinel.phase == "mutated":
        assert test_character.level == 10, "Rollback failed: level did not revert"
        $ test_sentinel.phase = "init"  # Reset
```

---

## 4. End-to-End (E2E) UI Testing

Ren'Py includes a built-in GUI Test Automation engine (`renpy.test`) that imitates real user interactions (mouse clicks, timer delays, and screen actions) against live rendered screen displayables.

### A. Screen Lifecycle & Focus List Rebuilding (`$ renpy.restart_interaction()`)
* **Mounting Screens:** Use `$ renpy.show_screen("screen_name", **kwargs)` or `action Show(...)` to mount screens into the display list for testing.
* **CRITICAL - Rebuilding Focus List:** Always call `$ renpy.restart_interaction()` immediately after `$ renpy.show_screen(...)`. 
  - *Why:* In headless Linux Xvfb CI containers (and background menu loops), `$ renpy.show_screen()` queues screen dirty states, but `focus_list` remains populated with previous screen targets until an interaction cycle occurs. `$ renpy.restart_interaction()` forces Ren'Py's display engine to rebuild `focus_list` on frame 1, allowing `click "Text"` and `find_focus()` to resolve target hitboxes instantly.
* **Bypassing Menu Transition Delays:** At the start of an E2E testcase, execute `$ renpy.transition(None)` and `$ renpy.hide_screen("main_menu")` to cancel ongoing menu enter transitions (`config.enter_transition = dissolve`) that block focus recalculation.
* **Cleaning Up:** Always hide screens at the end of the testcase using `$ renpy.hide_screen("screen_name")`.
* **Frame Delays (`pause`):** Include `pause <seconds>` (e.g. `pause 0.2`) after mounting screens or triggering UI events.

### B. Simulating User Clicks & Assertions
* **`click "Text"`**: Scans rendered screen displayables matching text `"Text"`, calculates exact screen bounding boxes, and fires Pygame `MOUSEBUTTONDOWN`/`MOUSEBUTTONUP` events.
* **`$ assert condition`**: Evaluates Python state after screen event handlers process clicks.

### C. Example E2E UI Test Pattern
```renpy
    testcase test_e2e_combat_button_clicks:
        # 1. Clear background transitions and mount screen
        $ renpy.transition(None)
        $ renpy.hide_screen("main_menu")
        $ test_service = CombatService()
        $ test_service.start_combat(create_weapon_from_db("Knife"))
        $ renpy.show_screen("combat_main", combat_service=test_service)
        $ renpy.restart_interaction()
        pause 0.2

        # 2. Imitate User Action: Click screen button by matching rendered UI text
        click "FIGHT (QTE)"
        pause 0.2
        $ assert test_service.qte_active, "QTE should be active after clicking FIGHT button"

        # 3. Clean up screen
        $ renpy.hide_screen("combat_main")
```

### D. Suite Separation Naming Convention
* **Unit / Logic / Screen API TestSuites:** Name suites `<service>_tests` (e.g. `combat_service_tests`). These run in milliseconds both locally and in CI containers.
* **Spatial E2E UI TestSuites:** Name suites `<service>_e2e_ui_tests` (e.g. `combat_e2e_ui_tests`). Separate spatial `click "Text"` statements into these E2E suites so CI can exclude them if needed.

---

## 5. Running Tests & Automated CI Status

To run tests with automatic process termination, use the manager utility `manage.py` located in the project root:

```powershell
# Run a specific testsuite
python manage.py test <testsuite_name>

# Run ALL testsuites (Unit + E2E)
python manage.py test global

# Run ALL testsuites EXCEPT E2E spatial UI suites (Recommended for CI pipelines)
python manage.py test --exclude-e2e

# Query GitHub Actions CI workflow status (automatically fetches & dumps logs on failure)
python manage.py ci-status [--watch]
```

### Pre-execution Linting
Always run the `lint` command before and after creating new tests to catch syntax errors:
```powershell
python manage.py lint
```

---

## 6. Debugging & Gotchas

### Ren'Py TestSuite Discovery & Disabling Rule
* **Discovery Rule:** Ren'Py's test parser scans all `.rpy` files and registers any block starting with `testsuite <name>:`.
* **Gotcha:** Renaming a testsuite block (e.g. `disabled_combat_e2e_ui_tests:`) **does NOT skip or disable it**! Ren'Py executes all `testsuite` blocks regardless of name prefix.
* **Resolution:** To disable/skip a testsuite block, you **must comment it out** using `#`.

### Output Stream Flushing in TestCases
* Inside `python:` blocks in testcases, standard Python `print()` calls are block-buffered when stdout is piped inside subprocesses (e.g., `xvfb-run` or `manage.py test`).
* **Resolution:** Always use `print(..., flush=True)` or call `import sys; sys.stdout.flush()` inside testcase Python blocks to ensure diagnostic logs stream immediately to the console/CI runner.

### UTF-8 BOM Handling in Failure Diagnostics
* Ren'Py automatically writes `errors.txt` and `traceback.txt` to the project root with UTF-8 BOM (`\ufeff`) headers.
* **Resolution:** When reading these diagnostic files in Python tooling (`manage.py`), use `encoding="utf-8-sig"` and handle `UnicodeEncodeError` on Windows CLI environments.

### Orphan Compiled Files (`.rpyc` / `.rpyc.bak`)
If a script file is moved or renamed, it leaves behind a compiled `.rpyc` file in the old location. 
* **Resolution:** Clean all `.rpyc` files recursively from the terminal when experiencing unexpected or stale variable states:
  ```powershell
  python manage.py clean -v
  ```

### Headless CI Virtual Display & Graphic Environment (`Xvfb` + Mesa Software GL)
* Configure the graphic environment with Mesa DRI drivers, dummy audio, 1080p GLX server args, and branch pattern matching (`push.branches` / `pull_request.branches` including `n-*`) in `.github/workflows/ci.yml`.
* Configure `_test.timeout = 15.0` in the `setup:` block of spatial E2E UI testsuites to prevent slower shared CI container runners from exceeding Ren'Py's default 5.0s per-statement timeout.
