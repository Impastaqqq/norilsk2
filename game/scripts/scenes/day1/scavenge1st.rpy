# game/scripts/scenes/day1/scavenge1st.rpy

label scavenge1st:

    if scav >= 11:
        jump finaldeath1st

    play music "scav2.mp3" volume 0.20 fadein 8.0 fadeout 1.5

    play sound "scav.mp3" volume 0.20 fadein 8.0 fadeout 1.5 loop

    "you will be given the option to explore a couple of rooms"

    "but becareful the rooms are infested with tendrils!"

    "you can only turn the lights on for a second when you walk into the room!"

    "turning on lights and some other actions add to the monsters awareness"

    "if the awareness becomes more than 10 you will die!!"

    "the name of the game is to spot where the food is in the rooms when you turn on the lights"

    "after the lights turn off you'll get to choose from a couple of different spots that either have food a weapon or have nothing"

    "REMEBER DRINKS ARE NOT FOOD"
    "it's sort of like a timed wheres waldo mini game where you have a limited amount of guesses of where food or weapons are"

    $ food = 0

    #LEFT ROOM
    #middle
    $ secondshelf = 0
    $ topleft = 0
    # left bottom

    $ lmiddleleftopt = 0
    $ underbottomleftshelf = 0
    #right bottom left

    $ weapon = 0

    #MIDDLE ROOM

    #RIGHT ROOM

    $ trashcan = 0
    $ high = 0

    menu fir:
        "exit store":
            play sound "audio/leavescav.mp3" volume 1.2 fadeout 1.0
            pause 3.0
            jump afterscav

        "right":
            play sound "audio/opendoor.mp3" volume 1.2 fadeout 1.0
            pause 2.5
            $ scav += 2

            "you turn on the lights!(+2 awareness)"
            window hide
            play sound "audio/lightswitch.mp3" volume 1.2 fadeout 1.0
            pause 1.0

            scene rightbg with dissolve

            pause 2.0

            scene rightbgblack with fade

            show text "you have [scav] awareness." at top

            jump beforeright

        "middle room":
            play sound "audio/opendoor.mp3" volume 1.2 fadeout 1.0
            pause 2.5
            $ scav += 2

            "you turn on the lights!(+2 awareness)"
            window hide
            play sound "audio/lightswitch.mp3" volume 1.2 fadeout 1.0
            pause 1.0

            scene middlebg with fade

            pause 2.0
            scene middlebgblack with fade
            show text "you have [scav] awareness." at top
            jump beforemiddle

        "left":
            play sound "audio/opendoor.mp3" volume 1.2 fadeout 1.0
            pause 2.5
            $ scav += 2

            "you turn on the lights!(+2 awareness)"
            window hide
            play sound "audio/lightswitch.mp3" volume 1.2 fadeout 1.0
            pause 1.0

            scene leftbg with fade
            pause 2.0

            scene leftbgblack with fade

            show text "you have [scav] awareness." at top
            jump beforeleft

    menu beforeleft:
        "leave":
            play sound "audio/leave.mp3" volume 1.2 fadeout 1.0
            pause 2.5
            scene black with fade

            if scav >= 11:
                jump end1st
            else:
                show text "you have [scav] awareness." at top
                jump fir

        "search":
            if scav >= 11:
                jump end1st
            hide text
            jump leftroom

    menu leftroom:
        "right of room(+1 AWARENESS)":
            $ scav += 1
            "NOTHING HERE"
            jump beforeleft

        "center of room(+1 AWARENESS)":
            $ scav += 1
            "there's more than just animal meat"
            jump beforeleft

        "left shelf(+1 AWARENESS)":
            $ scav += 1
            if underbottomleftshelf == 0:
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "you got food"
                $ underbottomleftshelf += 1
                $ food += 1
            elif underbottomleftshelf == 1:
                "NOTHING HERE"
                pass
            jump beforeleft

        "bottom left corner(+1 AWARENESS)":
            $ scav += 1
            if lmiddleleftopt == 0:
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "you got food"
                $ lmiddleleftopt += 1
                $ food += 1
            elif lmiddleleftopt == 1:
                "nothing left"
                pass
            jump beforeleft

        "on top icemachine(+1 AWARENESS)":
            $ scav += 1
            "nothin"
            jump beforeleft

    menu beforemiddle:
        "leave":
            play sound "audio/leave.mp3" volume 1.2 fadeout 1.0
            pause 2.5
            scene black with fade

            if scav >= 11:
                jump end1st
            else:
                show text "you have [scav] awareness." at top
                jump fir

        "search":
            if scav >= 11:
                jump end1st
            else:
                jump middleroom

    menu middleroom:
        "TOP LEFT(+1 AWARENESS)":
            $ scav += 1
            if topleft == 0:
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "food yay"
                $ topleft += 1
                $ food += 1
            elif topleft == 1:
                "Nothing left"
                pass
            jump beforemiddle

        "second shelf to the right(+1 AWARENESS)":
            $ scav += 1
            "NOTHING HERE"
            jump beforemiddle

        "second shelf to left(+1 AWARENESS)":
            $ scav += 1
            if secondshelf == 0:
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "you got food"
                $ secondshelf += 1
                $ food += 1
            elif secondshelf == 1:
                "nothing left"
                pass
            jump beforemiddle

        "on the floor to the left(+1 awareness)":
            $ scav += 1
            if weapon == 0:
                $ weapon += 4
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "you picked up a hammer"
                show hammerfound at appear_top:
                    zoom 1.0
                    xpos 0.86
                    ypos 1.00
                pause 20.0
                hide hammerfound with fade
                jump beforemiddle
            elif weapon == 4:
                "nothing left"
                jump beforemiddle
            elif weapon == 1:
                "you have a knife already do you want to keep it?"
                jump hammerorknife

        "bottom left(+1 AWARENESS)":
            $ scav += 1
            "nothing"
            jump beforemiddle

    menu beforeright:
        "leave":
            play sound "audio/leave.mp3" volume 1.2 fadeout 1.0
            pause 2.5
            scene black with fade

            if scav >= 11:
                jump end1st
            else:
                show text "you have [scav] awareness." at top
                jump fir

        "search":
            if scav >= 11:
                jump end1st
            else:
                jump rightroom

    menu rightroom:
        "on wall in middle(+1 AWARENESS)":
            if weapon == 1:
                "nothing left"
                jump beforeright
            elif weapon == 0:
                $ weapon += 1
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "you pick up the knife"
                show knifefound at appear_top:
                    zoom 1.0
                    xpos 0.86
                    ypos 1.00
                pause 20.0
                hide knifefound with fade
                jump beforeright
            elif weapon == 4:
                "you have a hammer already do you want to keep it"
                jump knifeorhammer

        "highest shelf to the left(+1 AWARENESS)":
            $ scav += 1
            if high == 0:
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "you got food"
                $ high += 1
                $ food += 1
            elif high == 1:
                "nothing left"
            jump beforeright

        "bottom shelf to right(+1 AWARENESS)":
            $ scav += 1
            "NOTHING HERE"
            jump beforeright

        "next to trashcan (in corner)(+1 AWARENESS)":
            $ scav += 1
            if trashcan == 0:
                play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
                pause 1.0
                "yaya food"
                $ trashcan += 1
                $ food += 1
            elif trashcan == 1:
                "nothing"
                pass
            jump beforeright

        "high shelf to right(+1 AWARENESS)":
            $ scav += 1
            " no"
            jump beforeright

    menu knifeorhammer:
        "take the knife":
            $ scav += 1
            $ weapon = 1
            show knifefound at appear_top:
                zoom 1.0
                xpos 0.86
                ypos 1.00
            pause 20.0
            hide knifefound with fade
            jump beforeright

        "keep the hammer":
            jump beforeright

    menu hammerorknife:
        "keep knife":
            play sound "audio/pickup.mp3" volume 1.2 fadeout 1.0
            pause 1.0
            $ weapon = 1
            jump beforemiddle

        "take hammer":
            $ weapon = 4
            show hammerfound at appear_top:
                zoom 1.0
                xpos 0.86
                ypos 1.00
            pause 20.0
            hide hammerfound with fade
            jump beforemiddle
