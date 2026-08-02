# game/scripts/scenes/day3/day3.rpy

label day3:
    # first boss fight
    # do the thingy finding the person and animation pop up title the behemoth cluster

    scene day3 d35 with dissolve
    with vpunch

    "You run away with Eva"

    scene day3 d36 with fade

    "soon you find yourself at the shore"

    "You find a piece of candy on the floor…"

    scene day3 d37 with fade

    "I remember this adam, it was your favorite"

    "You stare at it briefly before getting in the canoe with eva…"

    scene black with fade

    pause 1.5

    scene day3 D38 with fade

    pause 4.0

    scene black with fade

    pause 1.0

    scene day3 D310

    "You get across the river, and continue your journey…"

    scene black with fade

    pause 3.0

    scene day3 d312 with fade

    "It’s getting late soon you need to rest… "

    scene black with fade

    pause 1.0

    scene day3 D313 with fade

    pause 1.00
    play sound "audio/time.mp3" volume 0.5

    show clickradio with easeinbottom

    pause 100.00

    show window

    return
