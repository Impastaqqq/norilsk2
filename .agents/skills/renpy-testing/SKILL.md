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

## 4. Running Tests via Command Line
Optimistically assume the SDK path environment is already configured. If any command fails, run `python manage.py verify` to check configuration diagnostics.

To run tests with automatic termination, use the manager runner utility `manage.py` located in the project root. It will execute the tests, stream outputs in real-time, and automatically close the Ren'Py process when execution completes or reaches a safety timeout (15 seconds):

```powershell
python manage.py test <testsuite_name>
```

Replace `<testsuite_name>` with your test suite identifier (e.g., `guild_service_tests`), or omit it (or use `global`) to run all tests:

```powershell
python manage.py test global
```

### Pre-execution Linting
Always run the `lint` command before and after creating new tests to catch syntax errors:
```powershell
python manage.py lint
```

---

## 5. Debugging & Gotchas

### Orphan Compiled Files (`.rpyc` / `.rpyc.bak`)
If a script file is moved or renamed, it leaves behind a compiled `.rpyc` file in the old location. 
* **The Problem:** Ren'Py will still load these orphan `.rpyc` files during initialization, silently executing the old code and overwriting active variables.
* **Resolution:** Clean all `.rpyc` files recursively from the terminal when experiencing unexpected or stale variable states:
  ```powershell
  Get-ChildItem -Path "game" -Filter *.rpyc -Recurse | Remove-Item
  ```

### Debug Prints
You can use standard python `print()` inside setup or testcase blocks to trace states. These prints will output directly to the terminal when executing tests via the Python interpreter.
