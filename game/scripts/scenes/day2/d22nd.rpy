# game/scripts/scenes/day2/d22nd.rpy

label d22nd:
    hide adamtalkhandsup

    show adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    "..."

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "Kid? You're by yourself?"

    a "Yes..."

    j "where is your group?"

    a "My father died around a month ago, I've been walking alone since"

    j "A month... How are you even alive? "

    a "My dad taught me how to survive and navigate this forest"

    j "I see... You can come out kid, we won't shoot."

    hide adamserious
    hide jakovserious

    scene d28 with dissolve

    show adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    "You walk out of the bush to the clearing where the camp was."

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    "Beside Jakov was a woman holding a shotgun pointing it slightly downwards."

    show verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    ve "He really is alone..."

    j "Put the gun down verdie"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    "Verdie puts the gun down and walks back to the campfire"

    hide verdieserious
    hide adamserious
    hide jakovserious

    scene d210 with fade

    "You stand by the fire and warm your hands"

    show adamserious with easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "I'm Jakov and she's Verdie"

    j "we're headed towards a colony that's a couple of days away, we were told it's one of the last government facilities that are still running"

    j "They have walls and a system that keeps the monsters out"

    j "Since you're alone you can come with us, you won't survive out here for long by yourself anyway"

    show adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "I'm Adam, and I'd like to join you"

    hide adamtalk
    show adamserious:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    j "Great, we're leaving in the morning, so you can sleep here for the night"

    j "But first, do you have any food? We've been out of food for a couple of days now."

    hide adamserious
    hide jakovserious

    menu d23rd:
        "Share food (-3 food)" if food >= 3:
            show adamtalk at easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            a "Here, I have some food"
            $ food -= 3
            hide adamtalk

            show jakovserious at appear_right:
                zoom 1.4
                xpos 0.65
                ypos 0.10
            j "Thank you kid, this is a lifesaver"
            hide jakovserious

            show verdietalk at appear_top:
                zoom 0.60
                xpos 0.35
                ypos -0.15
            ve "Yeah, thanks kid."
            hide verdietalk
            jump d24th

        "Keep food":
            show adamsad with easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            a "I don't have any food either..."
            hide adamsad

            show jakovserious at appear_right:
                zoom 1.4
                xpos 0.65
                ypos 0.10
            j "It's fine kid, we'll find some tomorrow"
            hide jakovserious

            show verdieserious at appear_top:
                zoom 0.60
                xpos 0.35
                ypos -0.15
            ve "Hopefully..."
            hide verdieserious
            jump d24th
