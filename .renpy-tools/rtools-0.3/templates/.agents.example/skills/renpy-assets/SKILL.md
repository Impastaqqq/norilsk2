---
name: renpy-assets
description: Guidelines for managing, naming, generating, and organizing visual and audio assets in a Ren'Py project. Use when creating images, background scenes, character sprites, or audio.
---

# Ren'Py Assets Skill

Use this skill when managing, organizing, or generating assets for a Ren'Py project. It ensures visual style consistency, proper aspect ratios, optimal file compression, and standard naming conventions.

## Guidelines & Best Practices

### 1. Image Resolution & Aspect Ratio
- **Target Resolution:** Default target resolution is typically **2560x1440 (16:9)** or **1920x1080 (16:9)** (configured in [gui.rpy](file:///game/gui.rpy)).
- Ensure all generated background assets match the project's target aspect ratio.
- Character sprites should have vertical proportions and transparent backgrounds (PNG format or WebP with alpha).

### 2. High-Resolution & Oversized Assets (e.g., 4K backgrounds)
- **Sharpness Rendering:** Ren'Py renders directly at physical window resolution rather than downscaling to virtual resolution first. Oversized assets render with full native detail on 4K displays if fitted correctly.
- **Auto-Fitting Suffix:** Use the `@` scaling suffix to auto-scale an image's virtual size:
  - For 4K assets (`3840x2160`) in a 1440p game ($1.5\times$ scale baseline), name the file with a `@1.5` suffix (e.g., `bg room@1.5.webp`).
  - For 4K assets (`3840x2160`) in a 1080p game ($2.0\times$ scale baseline), use `@2.0` (e.g., `bg room@2.0.webp`).
- **Manual Displayable Transforms:** Fit assets manually in code if needed:
  ```renpy
  image bg room = Transform("images/bg/room.webp", zoom=0.6667)
  # Or inline in scene statement:
  show bg room:
      xysize (2560, 1440)
  ```
- **Memory & VRAM Management:** 4K assets require $2.25\times$ more VRAM/RAM than 1440p assets. Use oversized assets selectively for key background scenes to avoid exceeding `config.image_cache_size_mb` and causing transition stuttering.

### 3. Folder Structure & Naming Conventions
Organize files cleanly inside the `game/` folder:

```
game/
├── images/
│   ├── bg/           # Background images (e.g. bg room.webp)
│   ├── characters/   # Character sprites (e.g. eileen happy.png)
│   ├── cg/           # Event CGs and cutscenes
│   └── ui/           # Custom UI graphics
├── audio/
│   ├── music/        # BGM loops (.ogg, .opus)
│   ├── sfx/          # Sound effects (.wav, .ogg)
│   └── voice/        # Voice overs (.ogg, .opus)
└── gui/              # Ren'Py GUI customization assets
```

- Ren'Py automatically registers files under `game/images/`.
- Use **lowercase, space-separated** filenames for automatic image tag resolution:
  - File: `game/images/bg/room.webp` -> Code: `scene bg room`
  - File: `game/images/characters/eileen happy.png` -> Code: `show eileen happy`

### 4. ATL (Animation & Transformation Language) & Visual Effects
- Use ATL blocks for dynamic camera motion, panning, zooming, and sprite animations:
  ```renpy
  show eileen happy at right:
      alpha 0.0
      easein 0.5 alpha 1.0
  ```
- Use `matrixcolor` for color shifts (e.g. night filters, desaturation, sepia):
  ```renpy
  image bg room night = Transform("images/bg/room.webp", matrixcolor=TintMatrix("#405080") * BrightnessMatrix(-0.15))
  ```

### 5. Audio Formats & Channel Management
- **Background Music (BGM):** Use `.ogg` or `.opus` for seamless looping and small file sizes.
  ```renpy
  play music "audio/music/main_theme.ogg" fadein 1.0 loop
  ```
- **Sound Effects (SFX):** Use `.wav` or `.ogg` for low-latency playback.
  ```renpy
  play sound "audio/sfx/door_open.ogg"
  ```
- **Custom Audio Channels:** Register custom channels for layered audio (e.g. ambient weather, voice overlays):
  ```python
  init python:
      renpy.music.register_channel("ambient", mixer="sfx", loop=True)
  ```
  ```renpy
  play ambient "audio/sfx/rain.ogg" fadein 2.0
  ```

### 6. Generating Visual Assets
- When generating images using `generate_image`:
  - **Backgrounds:** Specify "16:9 aspect ratio, background scene" and describe lighting, atmospheric mood, and perspective.
  - **Sprites:** Request "isolated on a clean solid color or transparent background" with a clear pose, expression, and full/half-body framing.
- Maintain stylistic consistency across prompts (e.g. artistic medium, color temperature, linework style).

## References & Documentation
- [Displaying Images Documentation](https://www.renpy.org/doc/html/displaying_images.html)
- [Movie & Animation Assets Docs](https://www.renpy.org/doc/html/movie.html)
- [Audio & Music Playback Docs](https://www.renpy.org/doc/html/audio.html)
- [ATL (Animation & Transformation Language)](https://www.renpy.org/doc/html/atl.html)
- [Matrixcolor & Displayable Transforms](https://www.renpy.org/doc/html/matrixcolor.html)
