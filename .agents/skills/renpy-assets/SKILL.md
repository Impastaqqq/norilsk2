---
name: renpy-assets
description: Guidelines for managing, naming, generating, and organizing visual and audio assets in a Ren'Py project. Use when creating images, background scenes, character sprites, or audio.
---

# Ren'Py Assets Skill

Use this skill when managing or generating assets for the Ren'Py project. It keeps visual style, aspect ratios, file organization, and naming conventions consistent.

## Guidelines & Best Practices

### 1. Image Resolution & Aspect Ratio
- Default game resolution is **1920x1080 (16:9)**.
- Ensure all generated background assets match this ratio.
- Character sprites should have vertical proportions and a transparent background (PNG format).

### 2. Naming Conventions & Placement
- Ren'Py automatically registers files in the `game/images/` directory.
- Use **lowercase, space-separated** filenames for automatic image tags.
  - File: `game/images/bg room.jpg` -> Code: `scene bg room`
  - File: `game/images/eileen happy.png` -> Code: `show eileen happy`
- Place backgrounds and character sprites under `game/images/`.
- Place audio files under `game/audio/`.

### 3. Generating Visual Assets
- When generating images using `generate_image`:
  - **Backgrounds:** Specify "16:9 aspect ratio, background scene" and detail the aesthetic style (e.g., "Warcraft-style 2.5D illustration", "anime digital painting style").
  - **Sprites:** Specify "isolated on a clean, solid background" (for easy transparency cropping) or request transparent background if supported, stating the character's pose, expression, and appearance.
- **Consistency:** Ensure subsequent generation prompts reference the established design style to maintain visual coherence.

### 4. Audio Formats
- Background Music (BGM): Use `.ogg` or `.opus` for loops and smaller file sizes.
- Sound Effects (SFX): Use `.wav` or `.ogg` for high-compatibility playback.

## References & Documentation
- [Images & Sprite Displaying Docs](https://www.renpy.org/doc/html/displaying_images.html)
- [Movie & Animation Assets Docs](https://www.renpy.org/doc/html/movie.html)
- [Audio & Music Playback Docs](https://www.renpy.org/doc/html/audio.html)

