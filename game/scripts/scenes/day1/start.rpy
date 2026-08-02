# game/scripts/scenes/day1/start.rpy

label start:

    if config.developer:
        menu:
            "=== DEVELOPER MODE ROUTER (Visible in Dev Mode Only) ==="
            "Start Main Story (Day 1)":
                pass
            "Test Combat Prototype":
                jump combat_test_scene
            "Test Combat v2 Prototype":
                jump combat_test_scene2
            "Test Screen Prototype":
                jump test_tv_combat_scene

    scene black

    pause 1.0
    play sound "audio/rot.mp3" volume 0.5

    show sam
    #I am what happens when you try and carve God out of the wood of your own hunger"
    pause 5.0
    hide sam
    ####the animation and wtv
    scene black
    play sound "audio/walking intro.mp3" volume 1.0

    pause 1.0

    "day 1..."
    hide window

    scene day1 d12-3 with fade

    pause 1.0

    play music "night.mp3" volume 0.75 fadeout 1.0

    queue radio "samvoice.mp3" fadein 1.0 volume 0.10 loop

    play sound "audio/walkingwforest.mp3" volume 0.40

    "A group of scientists funded by the government were tasked to drill into the center of the earth."

    "While Digging they found nothing useful and nearly couldn’t complete the operation but eventually…"

    scene day1 d14 with fade

    "they hit something…"

    scene day1 d15 with fade

    "And something was released…"

    scene black with fade

    pause 1.0

    scene day1 d7 with dissolve

    "you were 12 when the apocalypse happened"

    "Your mother was a scientist who worked on the drilling project that started this all"

    scene black with fade

    pause 1.0

    "No scientist survived that project…"

    scene day1 d19 with fade

    "after it began your father traveled with you to teach you how to survive"

    "Around your eighteenth birthday, your father was caught off guard"

    scene black

    "he died..."

    scene day1 d111 with dissolve

    "The only thing he left was the knowledge he gave you and the radio he made"

    window hide

    scene day1 blank with dissolve

    play sound "time.mp3" volume 1.50
    show day1 tutorial with moveinleft:
        xpos 0.11
        ypos 0.00

    show radio with moveintop:
        xpos 0.30
        ypos 0.00

    pause 100.0

    scene black
    stop music fadeout 1.5

    "While walking you find a store to scavenge from, it seems to be over run with parts of the monster in it"

    "your running out of food so you'll need to check it out"

    play sound "audio/enterscav.mp3" volume 1.2 fadeout 1.0
    pause 7.0
    $ scav = 0
    jump scavenge1st
