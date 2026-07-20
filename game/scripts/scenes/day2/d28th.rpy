# game/scripts/scenes/day2/d28th.rpy

label d28th:
    scene d215 with fade

    show adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "Hey there... Come here..."

    hide adamtalk
    show adamserious:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    "The dog slowly walks towards you, sniffing your hand"

    show adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "You're friendly, aren't you?"

    hide adamtalk
    show adamserious:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    "You pet the dog, it wags its tail"

    "Jakov and Verdie return carrying some wood and tools"

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "We got the stuff... Who's your friend?"

    show adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "I don't know, it just walked in"

    hide adamtalk
    show adamserious:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    ve "It has a collar... Eva?"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    j "We don't have time for this, we need to fix the canoe"

    j "verdie, help me with the wood"

    hide adamserious
    hide jakovserious
    hide verdieserious

    scene d215 with fade

    "Jakov and Verdie start repairing the canoe"

    "You help them as much as you can"

    "After a couple of hours, the canoe is fixed"

    show adamtalk at easeinbottom:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    a "It looks good as new!"

    hide adamtalk
    show adamserious:
        zoom 0.85
        xpos 0.10
        ypos 0.00

    show jakovserious at appear_right:
        zoom 1.4
        xpos 0.65
        ypos 0.10

    j "Yes, it should hold... But it's already late, we'll have to cross tomorrow"

    j " let's camp here for the night"

    show verdietalk at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    ve "I'll set up the camp"

    hide verdietalk
    show verdieserious at appear_top:
        zoom 0.60
        xpos 0.35
        ypos -0.15

    j " but don't forget to watch out for dangerous people there's a lot of assholes in the world…"

    hide jakovserious
    hide adamsad
    hide verdietalk

    scene black with fade

    "You continue your journey"

    scene d216 with fade

    pause 1.0

    scene d217 with fade

    pause 1.5

    scene d2177 with fade

    "You check it out"

    scene black with dissolve

    "arf arf!"

    scene d218 with fade

    "You walk up to the dog and it comes near you…"

    "It has a collar with the name Eva on it…"

    "You feed the dog a piece of the food you have…"

    "You walk away and it follows"

    scene black with fade

    "You’ve been walking for a while now it’s time for you to set up for the night…"

    scene d222 with fade

    "While you sit down you pet the dog and look up at the sky"

    "The sky is a lot prettier when you have company…"

    scene d223 with fade

    pause 3.0

    "its time to sleep adam..."

    # radio time

    scene d222 with fade

    pause 1.00

    show clickradio with easeinbottom

    pause 100.00

    show sleep1st with fade

    pause 7.00
