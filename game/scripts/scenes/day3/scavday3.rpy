# game/scripts/scenes/day3/scavday3.rpy

label scavday3:
    scene day3 d31 with fade
    "You soon meet with a roadblock."

    "There’s a river that you won't be able to swim across and it doesn’t seem like it’ll be easy to walk around it."

    scene d32 with dissolve
    "You step out to look around"

    scene day3 d33 with fade

    "There’s a store along the shore for you to scavenge! ### maybe use this bg for the candy scene"
    scene black with fade
    pause 1.5

    jump behemoth
