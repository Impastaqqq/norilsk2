# game/scripts/scenes/prototypes/test_tv_combat_scene.rpy

default tv_grain_enabled = True
default tv_grain_strength = 0.15
default tv_grain_speed = 15.0
default tv_grain_size = 2.0
default tv_grain_distortion = 0.10

screen test_tv_combat_screen():
    modal True

    # Layer 1: Background Combat Image with Film Grain Shader
    if tv_grain_enabled:
        add "images/combat/bg_combat.png":
            fit "cover"
            at film_grain(strength=tv_grain_strength, speed=tv_grain_speed, size=tv_grain_size, distortion=tv_grain_distortion)
    else:
        add "images/combat/bg_combat.png":
            fit "cover"

    # Layer 2: TV Screen Border Overlay
    add "images/combat/tv_border_2.png":
        xsize 1920
        ysize 1080
        fit "fill"

    # Overlay Control Panel for Shader Debugging
    frame:
        align (0.02, 0.02)
        background "#181b24cc"
        padding (20, 15)
        xsize 450

        vbox:
            spacing 10

            text "TV Combat Scene Prototype" size 22 bold True color "#ffffff"

            hbox:
                spacing 15
                text "Film Grain Shader:" color "#cccccc" size 16 yalign 0.5
                if tv_grain_enabled:
                    textbutton "ENABLED" action SetVariable("tv_grain_enabled", False):
                        text_color "#00ffcc"
                        text_bold True
                else:
                    textbutton "DISABLED" action SetVariable("tv_grain_enabled", True):
                        text_color "#ff5555"
                        text_bold True

            if tv_grain_enabled:
                vbox:
                    spacing 2
                    hbox:
                        text "Grain Strength: " color "#cccccc" size 14
                        text "[tv_grain_strength:.2f]" color "#00ffcc" size 14 bold True
                    bar:
                        value VariableValue("tv_grain_strength", range=1.00, step=0.02)
                        xsize 410

                vbox:
                    spacing 2
                    hbox:
                        text "Grain Size (Coarseness): " color "#cccccc" size 14
                        text "[tv_grain_size:.1f]px" color "#00ffcc" size 14 bold True
                    bar:
                        value VariableValue("tv_grain_size", range=10.0, step=0.5)
                        xsize 410

                vbox:
                    spacing 2
                    hbox:
                        text "Image Distortion (Warp): " color "#cccccc" size 14
                        text "[tv_grain_distortion:.2f]" color "#00ffcc" size 14 bold True
                    bar:
                        value VariableValue("tv_grain_distortion", range=1.00, step=0.02)
                        xsize 410

                vbox:
                    spacing 2
                    hbox:
                        text "Grain Speed: " color "#cccccc" size 14
                        text "[tv_grain_speed:.1f]" color "#00ffcc" size 14 bold True
                    bar:
                        value VariableValue("tv_grain_speed", range=60.0, step=1.0)
                        xsize 410

            hbox:
                spacing 20
                textbutton "Reset Defaults":
                    action [
                        SetVariable("tv_grain_enabled", True),
                        SetVariable("tv_grain_strength", 0.15),
                        SetVariable("tv_grain_speed", 15.0),
                        SetVariable("tv_grain_size", 2.0),
                        SetVariable("tv_grain_distortion", 0.10)
                    ]
                textbutton "Return":
                    action Return()


label test_tv_combat_scene:
    $ store.tv_grain_enabled = True
    $ store.tv_grain_strength = 0.15
    $ store.tv_grain_speed = 15.0
    $ store.tv_grain_size = 2.0
    $ store.tv_grain_distortion = 0.10

    call screen test_tv_combat_screen
    return
