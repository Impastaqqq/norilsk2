# game/scripts/scenes/day2/day2.rpy

label day2:
    scene black with fade

    "You continue your journey."

    scene day2 d23 with dissolve

    pause 1.0

    scene day2 d24 with dissolve

    "You see smoke coming from a clearing and decide to investigate."

    "You turn your radio low"

    scene day2 d25 with fade

    "While you sneak behind a rock to check who it is…"

    scene day2 d27

    show day2 jakovangry with moveinbottom:
        zoom 1.4
        xpos 0.10
        ypos 0.10
    with hpunch

    m "WHOEVER’S OUT THERE I HOPE YOU KNOW WE’RE BOTH ARMED!!"

    hide jakovangry

    menu d21st:
        "Don't worry I’m harmless I’m just passing by":
            show day2 adamtalkhandsup with easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            a "Don't worry I’m harmless I’m just passing by"
            jump d22nd

        "I'm just a kid don't shoot me!":
            show day2 adamtalkhandsup with easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            a "I'm just a kid don't shoot me!"
            jump d22nd
