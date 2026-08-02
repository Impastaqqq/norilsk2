# game/scripts/scenes/day2/d26th.rpy

label d26th:
    scene d211 with dissolve

    show day2 adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show day2 jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "Let's move, we don't want to stay here for too long"

    hide adamserious
    hide jakovserious

    scene d212 with fade

    "You walk down the river towards the boat house"

    show day2 adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show day2 jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "Keep your eyes open, the monsters could be anywhere..."

    show day2 verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    ve "I see the boat house, it's just ahead"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    hide adamserious
    hide jakovserious
    hide verdieserious

    scene day2 d214 with dissolve

    "You arrive at the boat house, it's run down and covered in vines"

    show day2 adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "Let's check inside"

    hide adamtalk
    show day2 adamserious:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show day2 jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "Be careful kid, there could be traps"

    hide adamserious
    hide jakovserious

    scene day2 d215 with fade

    "You enter the boat house and search for anything useful"

    show day2 adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show day2 jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "I found a canoe, but it has a big hole in the bottom..."

    j "We'll need some tools and wood to fix it"

    show day2 verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    ve "There's a hardware store nearby, we might find what we need there"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    j "Okay, we'll head there. Adam, you stay here and keep watch, we'll be back soon"

    show day2 adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "Okay, I'll stay here"

    hide adamtalk
    show day2 adamsad:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    j "If anything happens, use the radio to call us"

    j "We'll make it quick"

    hide adamsad
    hide jakovserious

    scene black with fade

    "Jakov and Verdie leave the boat house"

    show day2 adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "I hope they'll be safe..."

    hide adamtalk
    show day2 adamsad:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    "You sit down on a wooden crate and wait"

    "The boat house is quiet, only the sound of the river..."

    "After a while, you hear a noise outside..."

    hide adamsad

    menu d27th:
        "Investigate":
            show day2 adamserious with easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            "You slowly walk to the door and look outside"
            "You see a dog, it looks hungry and scared"
            hide adamserious
            jump d28th

        "Hide":
            show day2 adamsad with easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            "You hide behind some wooden crates"
            "The noise gets closer, then you hear a soft whimper"
            "You look out and see a dog"
            hide adamsad
            jump d28th
