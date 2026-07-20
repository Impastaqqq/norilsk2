---
trigger: always_on
---

---
description: Guidelines for developing the "Norilsk" Ren'Py project.
---

# Ren'Py Development Rules

## Core Principles
1. **Always Verify First:** Before starting any task, read `norilsk-project-guide.md` and any relevant skill files (`.agents/skills/`) to ensure compliance with project standards.
2. **Systematic Development:**
   - **Linting:** Always run the `lint` command to catch syntax, image, and label errors before manual testing. Check `norilsk-project-guide.md` for renpy `lint` command.
   - **Automated Tests:** Logic and model-based changes must be accompanied by automated tests where possible.
   - **Warping:** Use the `warp` command to test specific scenes instead of replaying the entire game.
3. **Coding Standards:**
   - Follow the **OOP Architecture** outlined at the end of this document.
   - Keep game logic in Python models/services and UI/visuals in Ren'Py screens.
   - Use Python 3 syntax.
   - Always use type hints.
   - **File Headers:** Start every file with a comment containing the filename (e.g., `# hub_scene.rpy`) to prevent loss of the first line during automated edits.
4. **Communication:** Provide a high-level plan and wait for user approval before modifying files.

## Workflow
- **Plan:** Outline the change and files affected.
- **Implement:** Write code following the project's style.
- **Test:**
  - Run `lint`.
  - Execute automated tests for logic.
  - Warp to the modified area to verify visual consistency.

---

## Workspace Skills
This workspace uses specialized agent skills configured under `.agents/skills/`. The AI assistant automatically detects and applies them during code generation:
1. **`.agents/skills/renpy-scripting/SKILL.md`**: Guides correct Ren'Py script coding standards and Python 3 syntax.
2. **`.agents/skills/renpy-assets/SKILL.md`**: Standardizes asset formatting (16:9 images, audio formats) and AI generation guidelines.
3. **`.agents/skills/renpy-development/SKILL.md`**: Guides debugging and running the game engine from command line.
4. **`.agents/skills/renpy-testing/SKILL.md`**: Guides testing and running tests from command line.

---

## Interaction & Development Guidelines

### 1. Planning Posture
* **Outline First:** The agent must **never** start editing code files or executing commands immediately. Every task must begin with a concise, high-level overview of the planned changes, dependencies, and file locations.
* **Await Approval:** If the task is complex or deviates from established systems, the agent must wait for the user to review the outline.

### 2. OOP Architecture (Spring Boot & Java Analogy Guide)
To bridge the gap between Java/Spring conventions and Ren'Py Python execution:
* **Models (JPA Entities / POJOs):** Pure Python data classes or models should be created in separate Python files (e.g. `game/models/`). Initialize them using `default` at the top level of scripts.
* **Controllers & Services (Routing & Logic):** Ren'Py labels (`label scene_name:`) serve as controller endpoints directing the user flow, while Python methods in helper classes handle the logic layer.
* **Bean-like Singleton access:** All data declared via `default` is accessible globally within Ren'Py. Think of these variables as application-scoped Singletons managed by the Ren'Py runtime container.
* **Avoid tight coupling:** Do not execute visual transitions inside state classes. Let the script label (Controller) update the class (Model) and then call the display screens (View) to reflect changes.