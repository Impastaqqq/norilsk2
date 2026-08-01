---
trigger: always_on
---

---
description: Guidelines for developing Ren'Py projects with structured Python OOP architecture.
---

# Ren'Py Development Rules

## Core Principles
1. **Always Verify First:** Before starting any task, read [project-guide.md](file:///.agents/rules/project-guide.md) and any relevant skill files under `.agents/skills/` to ensure compliance with project standards.
2. **Systematic Development:**
   - **Static Analysis & Asset Integrity:** Run `python manage.py check` to catch asset path case mismatches and save/rollback variable state issues.
   - **Linting:** Run `python manage.py lint` to catch Ren'Py syntax, image, and label errors.
   - **Automated Tests:** Logic and model-based changes must be accompanied by automated tests (`python manage.py test global -s`).
   - **Warping:** Use the `warp` command to test specific scenes instead of replaying the entire game.
3. **Coding Standards:**
   - Follow the **Ren'Py & Python OOP Architecture Guide** outlined at the end of this document.
   - Keep game logic in Python models/services and UI/visuals in Ren'Py screens.
   - Use Python 3 syntax.
   - Always use type hints.
   - **File Headers:** Start every file with a comment containing the filename (e.g., `# hub_scene.rpy` or `# player_service.py`) to prevent loss of context during automated edits and bypass line-loss bugs in certain AI extensions (e.g., extensions like "Continue" consistently lose the first line on edit; adding a leading comment is a simple safe buffer and can be safely removed if not needed).
4. **Communication:** Provide a high-level plan and wait for user approval before modifying files.

## Workflow
- **Plan:** Outline the change and files affected.
- **Implement:** Write code following the project's style.
- **Test & Validate:**
  - Run `python manage.py check`.
  - Run `python manage.py lint`.
  - Execute automated tests (`python manage.py test global -s`).
  - Warp to the modified area to verify visual consistency.

---

## Workspace Skills
This workspace uses specialized agent skills configured under `.agents/skills/`. The AI assistant automatically detects and applies them during code generation:
1. **[renpy-scripting](file:///.agents/skills/renpy-scripting/SKILL.md)**: Guides correct Ren'Py script coding standards, Python 3 syntax, and screen language.
2. **[renpy-assets](file:///.agents/skills/renpy-assets/SKILL.md)**: Standardizes visual asset resolution (16:9, 4K supersampling), audio formats, and file naming.
3. **[renpy-development](file:///.agents/skills/renpy-development/SKILL.md)**: Guides debugging, state entity design (save/load/rollback), and CLI management commands.
4. **[renpy-testing](file:///.agents/skills/renpy-testing/SKILL.md)**: Guides automated test design, E2E UI testing, and CI headless verification.

---

## Interaction & Development Guidelines

### 1. Planning Posture
* **Outline First:** The agent must **never** start editing code files or executing commands immediately. Every task must begin with a concise, high-level overview of the planned changes, dependencies, and file locations.
* **Await Approval:** If the task is complex or deviates from established systems, the agent must wait for the user to review the outline.

### 2. Ren'Py & Python OOP Architecture Guide
To maintain clean separation of concerns and leverage Python 3 in Ren'Py 8.x:

* **Domain Models (State & Entities):**
  - Define pure Python data classes or state models in dedicated Python files (e.g., `game/models/`).
  - Mutable state-holding classes defined in `init python:` blocks must inherit from `renpy.store.object` (or `NoRollback` for transient session data) so Ren'Py records mutations for saves and rollbacks.
  - Instantiate global model instances at script level using `default` (e.g., `default player = Player("Hero")`).

* **Repositories & State Containers:**
  - Encapsulate data access and collection lookup logic inside repository classes (e.g., `CharacterRepository`, `InventoryManager`).
  - Declare state containers at script level via `default` to ensure state changes (additions, removals, updates) persist cleanly across saves and rollbacks.

* **Services & Business Logic:**
  - Place core gameplay algorithms, calculations, and state transformations inside dedicated service modules/classes (e.g., `game/services/combat_service.py`).
  - Keep services visual-agnostic: services perform state transitions and return results without directly triggering visual transitions, `renpy.show()`, or screen calls.

* **Controllers (Script Flow):**
  - Ren'Py labels (`label scene_name:`) act as scene controllers. They handle narrative progression, invoke service methods to process player choices, evaluate conditions, and branch to subsequent labels.

* **Views (Screens & Presentation):**
  - Ren'Py screens (`screen name:`) represent the presentation layer. They bind directly to model attributes or service state and trigger actions using Screen Actions (e.g., `action Function(service.do_action)`).
  - Avoid inline state mutation inside screen block evaluations; perform mutations strictly inside action callbacks or Python service methods.