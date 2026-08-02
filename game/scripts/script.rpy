# game/scripts/script.rpy

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


transform appear_right:
    xalign .85 yalign 1.0
    alpha 0 xoffset 30
    easein .5 alpha 1.0 xoffset 0

transform appear_top:
    xalign .85 yalign 1.0
    alpha 0 yoffset 30
    easein .5 alpha 1.0 yoffset 0


define mm = Character("m", color="#85075f")
 
define m = Character("man", color="#589fcf")
define j = Character("Jakov", color="#694619")
define ve = Character("Verdie", color="#196958")

define a = Character("You", color="#9c0068d0")
define g = Character("girl", color="#0beb70f3")

init python:
    renpy.music.register_channel('radio',"music")

image sam:
    "day1 sam1"
    pause 0.3
    "day1 sam2"
    pause 0.3
    "day1 sam3"
    pause 0.3
    repeat

image sleep1st:
    "start1"
    pause 0.3
    "start2"
    pause 0.3
    "start3"
    pause 0.3
    repeat

image attack1st:
    "day1 attack1"
    pause 0.3
    "day1 attack2"
    pause 0.3
    "day1 attack3"
    pause 0.3
    repeat
