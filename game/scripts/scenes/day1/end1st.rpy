# game/scripts/scenes/day1/end1st.rpy

label end1st:
    pause
    window hide
    $ renpy.movie_cutscene("images/death1.webm")
    show black with fade

    window show
    mm "I'm sorry Adam"
    "..."
    "the more you die the more it can sense your there!"
    $ scav = 0
    "instead of starting off at 0 awareness you will start off with 2"
    $ scav += 2
    "dont forget to not exceed 10 or youll die again and itll add 2 more!"
    jump scavenge1st
