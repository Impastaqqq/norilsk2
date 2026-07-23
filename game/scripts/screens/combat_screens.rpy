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
