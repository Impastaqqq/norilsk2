# game/scripts/screens/combat_screens.rpy

screen combat_main(combat_service):
    modal True
    default combat_log_adj = ui.adjustment()
    default last_log_len = 0

    # Continuous timer tick for QTE countdown & 1s hit overlay decay
    timer 0.1 repeat True action Function(combat_service.tick_timer, 0.1)

    # Auto-scroll log viewport when new entries are added
    if len(combat_service.log.entries) != last_log_len:
        $ last_log_len = len(combat_service.log.entries)
        $ combat_log_adj.change(999999)

    # 1. Background Scene
    add "images/combat/bg_combat.png" fit "cover"

    # 2. Enemy Full-Size Overlay Sprite
    add combat_service.enemy.enemy_sprite pos (-300, 300)

    # 3. Hit Overlay (1s duration on hit)
    if combat_service.show_hit_overlay:
        add combat_service.enemy.hit_overlay_sprite pos (-300, 300)

    # 4. Enemy Body Parts Status Indicator (Bottom Center)
    frame:
        pos (960, 1040)
        anchor (0.5, 1.0)
        background "#10121ad0"
        padding (20, 10)
        hbox:
            spacing 20
            text "[combat_service.enemy.name]" size 18 bold True color "#ffffff"
            for part in combat_service.enemy.body_parts:
                if part.is_broken:
                    text "[part.name]: [[BROKEN]]" color "#ff4444" size 16 outlines [(1, "#000000", 0, 0)]
                else:
                    text "[part.name]: [[INTACT]]" color "#44ff44" size 16 outlines [(1, "#000000", 0, 0)]

    # 5. Player HUD (Top Left)
    frame:
        pos (40, 40)
        background "#141722e0"
        padding (20, 20)
        xsize 380
        vbox:
            spacing 8
            text "PLAYER STATUS" size 20 bold True color "#ffffff"
            text "HP: [combat_service.player.hp] / [combat_service.player.max_hp]" size 16 color "#00ffcc"
            bar value combat_service.player.hp range combat_service.player.max_hp xsize 340 ysize 16
            text "Food Items: [combat_service.player.food_count]" size 15 color "#ffffaa"
            text "Weapon: [combat_service.player.equipped_weapon.name] ([combat_service.player.equipped_weapon.weapon_type])" size 15 color "#ffaa00"

    # 6. Action Panel (Bottom Left)
    frame:
        pos (40, 880)
        background "#141722e0"
        padding (20, 15)
        hbox:
            spacing 15
            textbutton "FIGHT (QTE)":
                action Function(combat_service.start_qte_phase)
                sensitive (not combat_service.qte_active and combat_service.enemy.current_hp > 0 and combat_service.player.hp > 0)
                padding (20, 12)
                background "#2b580c"
                hover_background "#3e7e11"
                insensitive_background "#1c2616"
                text_size 16 text_bold True text_color "#ffffff"

            button:
                action Function(combat_service.heal_player)
                sensitive (not combat_service.qte_active and combat_service.player.food_count > 0 and combat_service.player.hp < combat_service.player.max_hp)
                padding (20, 12)
                background "#1d4e89"
                hover_background "#286db7"
                insensitive_background "#162536"
                text "HEAL (+25 HP)" size 16 bold True color "#ffffff"

    # 7. Debug Panel (Top Right)
    frame:
        pos (1440, 40)
        background "#1a1c29e6"
        padding (20, 20)
        xsize 440
        vbox:
            spacing 12
            text "DEBUG TOOLS" size 20 bold True color "#ff5555" xalign 0.5

            text "WEAPON SELECTION" size 13 bold True color "#8899ac"
            hbox:
                spacing 10
                button:
                    action Function(combat_service.select_weapon, "Knife")
                    padding (16, 10)
                    background ("#3a506b" if combat_service.player.equipped_weapon.name == "Knife" else "#1c2541")
                    hover_background "#486581"
                    text "Knife (Arc)" size 14 color "#ffffff"

                button:
                    action Function(combat_service.select_weapon, "Hammer")
                    padding (16, 10)
                    background ("#3a506b" if combat_service.player.equipped_weapon.name == "Hammer" else "#1c2541")
                    hover_background "#486581"
                    text "Hammer (Square)" size 14 color "#ffffff"

            text "CONTROLS & LOG" size 13 bold True color "#8899ac"
            hbox:
                spacing 10
                button:
                    action Function(combat_service.restart_combat)
                    padding (16, 10)
                    background "#5c1d2e"
                    hover_background "#802840"
                    text "Restart Combat" size 14 color "#ffaaaa"

                button:
                    action Function(combat_service.toggle_log)
                    padding (16, 10)
                    background ("#2b4c7e" if combat_service.show_log else "#1b263b")
                    hover_background "#3e6ba8"
                    text ("Log: ON" if combat_service.show_log else "Log: OFF") size 14 color "#ffffff"

    # 8. Combat Log Display (Bottom Right)
    if combat_service.show_log:
        frame:
            pos (1320, 680)
            background "#0d0d12e0"
            padding (15, 15)
            xsize 560
            ysize 360
            vbox:
                spacing 5
                text "COMBAT LOG" size 18 bold True color "#aaaaaa"
                viewport id "log_vp":
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    yadjustment combat_log_adj
                    vbox:
                        spacing 4
                        for msg in combat_service.log.entries:
                            text "[msg]" size 14 color "#dddddd"

    # 9. Render QTE Overlay when active
    if combat_service.qte_active:
        use combat_tv_qte_overlay(combat_service)


screen combat_tv_qte_overlay(combat_service):
    modal True

    # QTE Timer Bar (Top of Screen)
    vbox:
        pos (960, 30)
        anchor (0.5, 0.0)
        spacing 6
        text "Timer: [combat_service.qte_time_remaining:.1f]s | Stage [combat_service.current_stage]/[combat_service.total_stages]" size 20 bold True color "#ff5555" xalign 0.5 outlines [(1, "#000000", 0, 0)]
        bar value combat_service.qte_time_remaining range combat_service.player.equipped_weapon.time_limit xsize 600 ysize 14 xalign 0.5

    # Render QTE Target Buttons at calculated dynamic positions
    for target in combat_service.current_targets:
        imagebutton:
            idle Transform(target.sprite, alpha=target.opacity)
            hover Transform(target.sprite, alpha=target.opacity)
            pos (target.x, target.y)
            anchor (0.5, 0.5)
            action Function(combat_service.click_target, target.target_id)
            sensitive (not target.is_clicked)


# Animated tendril small enemy sprite
image tendril_small_idle:
    "images/combat/enemies/tendril_small/small_fullhp.png"
    pause 0.2
    "images/combat/enemies/tendril_small/small_fullhp2.png"
    pause 0.2
    "images/combat/enemies/tendril_small/small_fullhp3.png"
    pause 0.2
    repeat


# ATL transform for UI control panel rolling from below the screen
transform action_panel_roll_up:
    subpixel True
    yanchor 1.0
    xanchor 0.5
    on show:
        pos (960, 1800)
        easein 0.6 pos (960, 1080)
    on replace:
        easein 0.5 pos (960, 1080)

# ATL transform for UI control panel rolling down completely behind screen
transform action_panel_roll_down:
    subpixel True
    yanchor 1.0
    xanchor 0.5
    easein 0.5 pos (960, 1800)


# ATL transform for player health panel rolling down from top of screen
transform health_panel_roll_down:
    subpixel True
    yanchor 0.0
    xanchor 0.0
    on show:
        pos (120, -400)
        easein 0.6 pos (120, 0)
    on replace:
        easein 0.5 pos (120, 0)

# ATL transform for player health panel rolling up completely behind screen
transform health_panel_roll_up:
    subpixel True
    yanchor 0.0
    xanchor 0.0
    easein 0.5 pos (120, -400)


# ATL transform for TV scene container resting offscreen before first fight
transform tv_offscreen:
    subpixel True
    pos (0, -1080)


# ATL transform for TV scene container rolling down from top of screen
transform tv_roll_down:
    subpixel True
    pos (0, -1080)
    pause 0.2
    easein 0.6 pos (0, 0)


# ATL transform for TV scene container rolling up completely behind upper screen border
transform tv_roll_up:
    subpixel True
    easein 0.5 pos (0, -1080)


screen combat_main_v2(combat_service=None):
    modal True
    default current_weapon = "Knife"
    default player_hp = 100
    default player_max_hp = 100
    default fight_mode = False
    default tv_started = False

    # Timer tick for QTE countdown & hit overlay decay
    if combat_service is not None and (combat_service.qte_active or combat_service.show_hit_overlay):
        timer 0.1 repeat True action Function(combat_service.tick_timer, 0.1)

    $ active_hp = combat_service.player.hp if combat_service is not None else player_hp
    $ active_max_hp = combat_service.player.max_hp if combat_service is not None else player_max_hp
    $ active_weapon_name = combat_service.player.equipped_weapon.name if combat_service is not None else current_weapon
    $ weapon_icon = "images/combat/weapons/knife1.png" if "Knife" in active_weapon_name else "images/combat/weapons/hammer1.png"
    $ next_weapon = "Hammer" if "Knife" in active_weapon_name else "Knife"

    # Automatic TV screen roll-up when QTE phase completes
    if combat_service is not None and fight_mode and not combat_service.qte_active:
        $ fight_mode = False

    # 1. Base Clean Background Combat Image (Full 1920x1080 screen)
    add "images/combat/bg_combat.png":
        fit "cover"

    # 2. Base Clean Animated Enemy Sprite (Middle of screen)
    add "tendril_small_idle":
        align (0.5, 0.5)

    # 3. Unified TV Fight Mode Container (Distortion Lens, Border Frame & QTE Overlay roll down together)
    fixed:
        at (tv_roll_down if fight_mode else (tv_roll_up if tv_started else tv_offscreen))

        # Distorted TV Screen Lens & Noise Filter
        fixed:
            pos (100, 100)
            xsize 1720
            ysize 980
            clipping True

            # Distorted Background Image inside TV lens
            add "images/combat/bg_combat.png":
                pos (-100, -100)
                fit "cover"
                at film_grain(strength=1.50, speed=45.0, size=4.0, distortion=1.80)

            # Distorted Enemy Sprite inside TV lens
            add "tendril_small_idle":
                align (0.5, 0.5)
                at film_grain(strength=1.50, speed=45.0, size=4.0, distortion=1.80)

            # Enemy Hit Flash Overlay inside TV screen
            if combat_service is not None and combat_service.show_hit_overlay:
                add combat_service.enemy.hit_overlay_sprite:
                    align (0.5, 0.5)

        # TV Screen Border Overlay
        add "images/combat/tv_borderv2.png":
            xsize 1920
            ysize 1080
            fit "fill"

        # Interactive QTE Targets & Bottom-Left Countdown Numbers
        fixed:
            pos (0, 0)

            # Active interactive QTE targets in weapon-specific positioning
            if combat_service is not None and combat_service.qte_active and combat_service.current_targets:
                for target in combat_service.current_targets:
                    imagebutton:
                        idle Transform(target.sprite, alpha=target.opacity)
                        hover Transform(target.sprite, alpha=target.opacity)
                        pos (target.x, target.y)
                        anchor (0.5, 0.5)
                        action Function(combat_service.click_target, target.target_id)
                        sensitive (not target.is_clicked)
            else:
                $ fallback_weapon_type = "ARC" if "Knife" in active_weapon_name else "SQUARE"
                $ fallback_sprite = "images/combat/qte_knife.png" if "Knife" in active_weapon_name else "images/combat/qte_hammer.png"
                $ fallback_positions = generate_qte_positions(layout_type=fallback_weapon_type, num_points=(5 if fallback_weapon_type == "ARC" else 4), pattern_params=({"length": 650, "curvature": 0.45, "center_x": 960, "center_y": 540} if fallback_weapon_type == "ARC" else {"size": 360, "center_x": 960, "center_y": 540}), randomize_shape=False)
                for (tx, ty) in fallback_positions:
                    add fallback_sprite:
                        pos (tx, ty)
                        anchor (0.5, 0.5)

            # Live stage countdown number and live time countdown (10->0) rolling down with TV screen at bottom-left
            $ display_stage = combat_service.current_stage if (combat_service is not None and combat_service.qte_active) else 1
            $ display_time = int(round(combat_service.qte_time_remaining)) if (combat_service is not None and combat_service.qte_active) else 10
            hbox:
                pos (220, 880)
                anchor (0.0, 1.0)
                spacing 50
                text "[display_stage]" size 36 bold True color "#ffffff" outlines [(2, "#000000", 0, 0)]
                text "[display_time]" size 36 bold True color "#ff5555" outlines [(2, "#000000", 0, 0)]

    # 7. Player Health Panel (rolls down on enter, rolls up behind screen on fight)
    fixed:
        at (health_panel_roll_up if fight_mode else health_panel_roll_down)
        fit_first True
        pos (40, 0)
        anchor (0.0, 0.0)

        # Health Screen Base Asset
        add "images/combat/ui/health_screen.png"

        # Numeric Player Health Overlay
        text "[active_hp]" size 42 bold True color "#22e004" outlines [(1, "#000000", 0, 0)] align (0.5, 0.5) xoffset -25 yoffset 20

    # 8. UI Control Panel (rolls up on enter, rolls down behind screen on fight)
    fixed:
        at (action_panel_roll_down if fight_mode else action_panel_roll_up)
        fit_first True
        pos (960, 1080)
        anchor (0.5, 1.0)

        # Control Panel Base Asset
        add "images/combat/ui/action_select_screen.png"

        # Weapon Toggle Button (Top Left of UI Control Panel)
        imagebutton:
            idle Transform(weapon_icon, align=(0.5, 0.5))
            hover Transform(weapon_icon, align=(0.5, 0.5), zoom=1.15)
            pos (220, 110)
            anchor (0.5, 0.5)
            action If(combat_service is not None, Function(combat_service.select_weapon, next_weapon), SetScreenVariable("current_weapon", next_weapon))

        # Action Buttons Overlay (Fight on left, Heal on right)
        hbox:
            align (0.5, 0.5)
            spacing 40

            imagebutton:
                idle "images/combat/ui/fight_idle.png"
                hover "images/combat/ui/fight_hover.png"
                selected_idle "images/combat/ui/fight_click.png"
                selected_hover "images/combat/ui/fight_click.png"
                xoffset -80
                yoffset 100
                action [
                    SetScreenVariable("fight_mode", True),
                    SetScreenVariable("tv_started", True),
                    If(combat_service is not None, Function(combat_service.start_qte_phase), NullAction())
                ]

            imagebutton:
                idle "images/combat/ui/heal_idle.png"
                hover "images/combat/ui/heal_hover.png"
                selected_idle "images/combat/ui/heal_clicked.png"
                selected_hover "images/combat/ui/heal_clicked.png"
                at Transform(zoom=0.9)
                xoffset 60
                yoffset 100
                action If(combat_service is not None, Function(combat_service.heal_player), NullAction())

    # 9. Prototype Debug UI Reset Button (Visible in fight mode)
    if fight_mode:
        textbutton "RESET UI":
            align (0.98, 0.02)
            action SetScreenVariable("fight_mode", False)
            text_color "#ff8888"
            text_size 14
            text_outlines [(1, "#000000", 0, 0)]






