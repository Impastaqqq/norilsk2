# game/scripts/scenes/day1/afterscav.rpy

label afterscav:
    stop music fadeout 1.5
    stop sound fadeout 1.5
    show day1 d112-13 with fade

    "You walk out of the gas station and start to make your way back onto the road but then… (have the radio playing loudly)"

    scene black with fade

    show attack1st with fade
    play sound "firstfightsam.mp3" volume 0.1

    "на теья напали!"

    pause 10.00

    hide attack1st
    play sound "audio/run.mp3" volume 1.2 fadeout 1.0

    pause 2.0

    scene day1 d115 with dissolve

    "You run away and make it back on the path"

    scene black with fade
    play sound "forestfire.mp3" volume 0.50 fadeout 1.0
    pause 1.5
    play music "tellme.mp3" volume 1.0 fadeout 1.0

    "It’s getting late you're going to have to camp out"

    scene day1 d118 with fade

    pause 1.00
    play sound "audio/time.mp3" volume 0.5

    show clickradio with easeinbottom

    pause 100.00
    stop music fadeout 2.0

    scene black with fade

    show sleep1st with dissolve

    # maybe turn music off idk or something else
    play sound "audio/sleep1st.mp3" volume 0.7

    "Killed (40) ***** ***** *** **** *** (14)"
    pause 7.00

    scene black with fade

    "you can only understand part of it, you write it down in your note book"

    "maybe one day you can translate the whole language"

    scene black with fade

    stop sound
    stop music

    $ scav = 0

    jump scavday2
