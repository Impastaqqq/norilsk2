# game/scripts/scenes/day1/finaldeath1st.rpy

label finaldeath1st:
    $ renpy.movie_cutscene("images/day1/death1.webm")

    scene black with fade

    mm "I'm sorry honey..."

    mm "It's time you rest, your trip ends here"
    $ scav = 0

    return
