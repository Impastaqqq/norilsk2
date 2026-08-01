# test_film_grain.rpy

default grain_demo_enabled = True
default grain_demo_strength = 0.08
default grain_demo_speed = 15.0

screen test_film_grain_screen():
    modal True
    add "#12141a"

    vbox:
        align (0.5, 0.5)
        spacing 20
        xsize 960

        text "Film Grain GLSL Shader Demo" size 30 bold True color "#ffffff" xalign 0.5

        # Preview Container with Film Grain Transform applied
        frame:
            xalign 0.5
            xsize 800
            ysize 400
            background "#1e222d"
            padding (0, 0)

            # Background color gradient box
            add Frame(Solid("#2b3245"), xsize=800, ysize=400)

            # Sample decorative visual elements
            vbox:
                align (0.5, 0.5)
                spacing 10
                text "PROCEDURAL FILM GRAIN PREVIEW" size 24 bold True color "#00ffcc" xalign 0.5
                text "Real-time GPU GLSL Fragment Noise" size 16 color "#a0aab8" xalign 0.5

            if grain_demo_enabled:
                # Apply film grain shader to overlay
                add Frame(Solid("#ffffff"), xsize=800, ysize=400) alpha 0.001 at film_grain(strength=grain_demo_strength, speed=grain_demo_speed)

        # Control Panel
        frame:
            xalign 0.5
            xsize 800
            background "#181b24"
            padding (25, 20)

            vbox:
                spacing 15

                hbox:
                    spacing 20
                    text "Shader Status:" color "#ffffff" size 18 bold True yalign 0.5
                    if grain_demo_enabled:
                        textbutton "ENABLED" action SetVariable("grain_demo_enabled", False):
                            text_color "#00ffcc"
                            text_bold True
                    else:
                        textbutton "DISABLED" action SetVariable("grain_demo_enabled", True):
                            text_color "#ff5555"
                            text_bold True

                null height 5

                # Grain Strength Control
                vbox:
                    spacing 5
                    hbox:
                        text "Grain Strength: " color "#cccccc" size 16
                        text "[grain_demo_strength:.2f]" color "#00ffcc" size 16 bold True
                    bar:
                        value VariableValue("grain_demo_strength", range=0.30, step=0.01)
                        xsize 750

                # Grain Speed Control
                vbox:
                    spacing 5
                    hbox:
                        text "Grain Speed: " color "#cccccc" size 16
                        text "[grain_demo_speed:.1f]" color "#00ffcc" size 16 bold True
                    bar:
                        value VariableValue("grain_demo_speed", range=60.0, step=1.0)
                        xsize 750

        # Action Buttons
        hbox:
            xalign 0.5
            spacing 30
            textbutton "Reset Defaults":
                action [SetVariable("grain_demo_enabled", True), SetVariable("grain_demo_strength", 0.08), SetVariable("grain_demo_speed", 15.0)]
            textbutton "Return":
                action Return()


label test_film_grain_start:
    $ store.grain_demo_enabled = True
    $ store.grain_demo_strength = 0.08
    $ store.grain_demo_speed = 15.0
    scene bg room with fade
    call screen test_film_grain_screen
    return
