# Combat Scene Prototype v2 Design & Architecture

## 1. Overview & Purpose
Combat Scene Prototype v2 is the next iteration of the Norilsk 2 combat interface. It merges the structured model and service architecture from `combat_test_scene.rpy` (`CombatService`, `PlayerCombatState`, `EnemyData`) with the rich visual design, ATL roll-in animations, custom UI control panels, and upcoming GLSL film grain shaders from `test_tv_combat_scene.rpy`.

---

## 2. Scene Flow & Script Entry
- **Scene File**: `game/scripts/scenes/prototypes/combat_test_scene.rpy`
- **Label**: `combat_test_scene2`
- **Start-up Sequence**:
  1. `scene black`: Clears previous screen displayables.
  2. `pause 0.5`: Enforces a brief 0.5-second black screen delay.
  3. `python: combat_service.start_combat()`: Initializes player state, equips default weapon, and spawns enemy data.
  4. `call screen combat_main_v2(combat_service)`: Renders the active combat UI overlay.

---

## 3. Visual Layer Hierarchy & Component Specifications

The screen displayables in `screen combat_main_v2` are ordered strictly from back to front:

```
[Layer 1] Background Image (bg_combat.png)
  └── [Layer 2] Animated Enemy Sprite (tendril_small_idle at screen center)
        ├── [Layer 3] Player Health Panel (health_screen.png rolling down from top left)
        └── [Layer 4] UI Control Panel (action_select_screen.png rolling up from bottom center)
              ├── Weapon Toggle Button (knife1.png / hammer1.png at top-left of panel)
              ├── Fight Button (fight_*.png on left side of panel)
              └── Heal Button (heal_*.png on right side of panel)
```

### Layer 1: Background
- **Asset**: `images/combat/bg_combat.png`
- **Properties**: `fit "cover"` (fills full 16:9 canvas).

### Layer 2: Animated Enemy Sprite
- **ATL Displayable**: `image tendril_small_idle`
- **Animation Sequence**: Cycles through 3 frames at `0.2s` intervals:
  - `images/combat/enemies/tendril_small/small_fullhp.png`
  - `images/combat/enemies/tendril_small/small_fullhp2.png`
  - `images/combat/enemies/tendril_small/small_fullhp3.png`
- **Positioning**: Rendered at screen center: `align (0.5, 0.5)`.

### Layer 3: Player Health Panel (Top-Left Roll-Down)
- **Base Asset**: `images/combat/ui/health_screen.png`
- **ATL Transform (`health_panel_roll_down`)**:
  - Starts offscreen top: `pos (120, -200)`
  - Slides down over 0.6s with `easein` to rest at `pos (120, 0)` (flushed against the top of the screen).
- **Numeric Health Text Overlay**:
  - Expression: `[active_hp]` (pulls from `combat_service.player.hp` or fallback variable `player_hp`).
  - Style: Green text (`color "#22e004"`), `size 42`, `bold True`, black outline `outlines [(1, "#000000", 0, 0)]`.
  - Manual Offset Adjustments: `align (0.5, 0.5)`, `xoffset -25`, `yoffset 20`.

### Layer 4: UI Control Panel (Bottom Roll-Up)
- **Base Asset**: `images/combat/ui/action_select_screen.png`
- **ATL Transform (`action_panel_roll_up`)**:
  - Starts offscreen bottom: `pos (960, 1250)` with `yanchor 1.0`, `xanchor 0.5`.
  - Slides up over 0.6s with `easein` to rest at `pos (960, 1080)`.

---

## 4. Interactive UI Controls & Button Layout

All control panel buttons are hosted inside the `fixed` container of `action_select_screen.png`.

### A. Weapon Toggle Button (Top-Left of Panel)
- **Assets**:
  - Knife: `images/combat/weapons/knife1.png`
  - Hammer: `images/combat/weapons/hammer1.png`
- **Position**: `pos (220, 110)`, `anchor (0.5, 0.5)`.
- **Interactivity & Hover**: Apply hover zoom `hover Transform(weapon_icon, align=(0.5, 0.5), zoom=1.15)`.
- **Action**: On click, toggles between `"Knife"` and `"Hammer"`. Executes `combat_service.select_weapon(next_weapon)` if `combat_service` is active, or `SetScreenVariable("current_weapon", next_weapon)` as a standalone fallback.

### B. Fight Button (Left Action)
- **Assets**:
  - Idle: `images/combat/ui/fight_idle.png`
  - Hover: `images/combat/ui/fight_hover.png`
  - Clicked/Selected: `images/combat/ui/fight_click.png`
- **Position & Layout**: Inside an `hbox` (`align (0.5, 0.5)`, `spacing 40`) with manual offsets:
  - `xoffset -80`
  - `yoffset 100`
- **Action**: `If(combat_service is not None, Function(combat_service.start_qte_phase), NullAction())`

### C. Heal Button (Right Action)
- **Assets**:
  - Idle: `images/combat/ui/heal_idle.png`
  - Hover: `images/combat/ui/heal_hover.png`
  - Clicked/Selected: `images/combat/ui/heal_clicked.png`
- **Scale & Layout**: Downscaled by 0.9 via `at Transform(zoom=0.9)` with manual offsets:
  - `xoffset 60`
  - `yoffset 100`
- **Action**: `If(combat_service is not None, Function(combat_service.heal_player), NullAction())`

---

## 5. Summary of Manual Fine-Tuning & Exact Coordinates Reference

For fast context resumption in future coding sessions, below is the exact coordinate table reflecting all manual position adjustments made during development:

| Element | Component Container | Pos / Alignment | Manual Offsets / Adjustments |
| :--- | :--- | :--- | :--- |
| **Health Panel Container** | Screen Root | `pos (40, 0)`, `anchor (0.0, 0.0)` | Roll-down on enter (`120, -400` -> `120, 0`), Roll-up on fight (`120, -400`) |
| **Health Text Number** | Health Panel | `align (0.5, 0.5)` | `xoffset -25`, `yoffset 20`, green `#22e004`, size 42 |
| **Control Panel Container** | Screen Root | `pos (960, 1080)`, `anchor (0.5, 1.0)` | Roll-up on enter (`960, 1800` -> `960, 1080`), Roll-down on fight (`960, 1800`) |
| **Weapon Toggle Button** | Control Panel | `pos (220, 110)`, `anchor (0.5, 0.5)` | Hover `zoom 1.15` |
| **Fight Button** | Control Panel HBox | `align (0.5, 0.5)` | `xoffset -80`, `yoffset 100` |
| **Heal Button** | Control Panel HBox | `align (0.5, 0.5)` | `at Transform(zoom=0.9)`, `xoffset 60`, `yoffset 100` |
| **Unified TV Container** | Screen Root | `pos (0, 0)` resting | Unified Roll-down `tv_roll_down`: `pos (0, -1080)` -> `pos (0, 0)` (`1920x1080`) |
| **TV Distortion Lens** | Unified TV Container | `pos (100, 100)` static | `xsize 1720, ysize 980`, `clipping True` |
| **TV Border Overlay** | Unified TV Container | `pos (0, 0)` static | `xsize 1920, ysize 1080` (`fit "fill"`) |
| **Static QTE & Countdown** | Unified TV Container | `pos (0, 0)` static | Static QTE sprites & bottom-left countdown `hbox pos (220, 880)` |

> [!TIP]
> **Distortion Offset Manual Adjustment Formula**:
> For horizontal offset `X` and top offset `Y`:
> - Inside unified container, inner lens container: `fixed pos (X, Y)` with `xsize (1920 - 2*X)` and `ysize (1080 - 2*Y)`
> - Inner background: `add "images/combat/bg_combat.png": pos (-X, -Y)`
> - Container roll transform: `tv_roll_down: pos (0, -1080) pause 0.2 easein 0.6 pos (0, 0)`

---

## 6. UI Transformation & TV Frame Roll-Down Sequence

When the player clicks the **Fight** button, `combat_main_v2` triggers a multi-stage UI transition:

1. **Health Panel Roll-Up (`health_panel_roll_up`)**:
   - Slides up completely off-screen from `pos (120, 0)` to `pos (120, -400)` over `0.5s` (`easein`).
2. **Control Panel Roll-Down (`action_panel_roll_down`)**:
   - Slides down completely behind the screen from `pos (960, 1080)` to `pos (960, 1800)` over `0.5s` (`easein`).
3. **Unified TV Scene Roll-Down (`tv_roll_down`)**:
   - Pauses `0.2s` for panels to clear, then rolls down the entire TV scene container (Distortion Lens, TV Border frame, static QTE targets, and countdown numbers) as a single unified container from `pos (0, -1080)` to `pos (0, 0)` over `0.6s` (`easein`).
   - Inside the container, heavy static noise versions of `bg_combat.png` (`pos (-100, -100)`) and `tendril_small_idle` (`align (0.5, 0.5)`) render with extreme noise and scanline distortion parameters: `film_grain(strength=1.50, speed=45.0, size=4.0, distortion=1.80)` clipped to the aperture bounds (`clipping True`).

---

## 7. Roadmap for Next Development Phase
When continuing in the next session, we will proceed with:
1. **QTE Target Overlay Integration**: Render weapon-specific QTE target overlays (`combat_tv_qte_overlay`) inside the active TV frame area.
2. **Damage & Enemy Feedback**: Connect hit flash overlays (`enemy_hit.gif`), body part damage tracking, and combat log updates when targets are hit or missed.

