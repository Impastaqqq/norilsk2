# game/scripts/scenes/day2/d24th.rpy

label d24th:
    scene d210 with fade

    "The night goes on and you talk to Jakov and Verdie"

    show adamsad with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "So your father... How did he die?"

    a "He was caught off guard by a monster... It was too fast for him to react"

    j "I'm sorry for your loss kid, it's hard to lose someone in this world..."

    j "But you're strong, you survived a month by yourself"

    show verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    ve "He's right, you're doing great kid"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    j "Tomorrow we'll have to cross a bridge, it's a bit dangerous but it's the only way to the colony"

    j "So get some rest, we'll need all the energy we can get"

    hide adamsad
    hide jakovserious
    hide verdieserious

    scene black with fade

    "You lie down by the fire and close your eyes"

    "You feel a bit safer now that you're not alone..."

    scene sleep1st with dissolve
    play sound "audio/sleep1st.mp3" volume 0.7

    pause 7.00

    scene black with fade

    "The next morning..."

    scene d211 with dissolve

    "You wake up and see Jakov packing up the camp"

    show adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "Morning kid, you ready to go?"

    a "Yes, I'm ready"

    j "Good, Verdie is checking the path ahead, she'll be back soon"

    hide adamserious
    hide jakovserious

    show verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    "Verdie runs back to the camp looking worried"

    ve "Jakov, we have a problem"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "What is it?"

    show verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15
    ve "The bridge... It's blocked by a group of bandits, they're demanding food or weapons to let anyone pass"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    j "Damn it... We don't have enough to give them..."

    j "Verdie, how many of them are there?"

    show verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15
    ve "Three, they all have weapons"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    j "We can't fight them... It's too risky"

    show adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "Maybe we can sneak past them?"

    j "No, the bridge is too open, they'll see us"

    j "We'll have to find another way... But that will take days..."

    hide adamserious
    hide jakovserious
    hide verdieserious

    menu d25th:
        "Offer to negotiate":
            show adamtalk at easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            a "Maybe I can talk to them? They might not see a kid as a threat"
            hide adamtalk
            show adamserious:
                zoom 0.85
                xpos 0.10
                ypos 0.00

            show jakovserious at appear_right:
                zoom 1.4
                xpos 0.65
                ypos 0.10
            j "It's too dangerous kid, I can't let you do that"
            hide adamserious
            hide jakovserious
            jump d26th

        "Look for a boat":
            show adamtalk at easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            a "Is there a boat nearby? We could cross the river"
            hide adamtalk
            show adamserious:
                zoom 0.85
                xpos 0.10
                ypos 0.00

            show jakovserious at appear_right:
                zoom 1.4
                xpos 0.65
                ypos 0.10
            j "There might be a canoe at the old boat house down the river, but it's probably broken"
            j "Still, it's better than fighting them. Let's check it out"
            hide adamserious
            hide jakovserious
            jump d26th
