# game/scripts/scenes/day2/scavday2.rpy

label scavday2:
    scene black with fade

    "You’ve walked all morning. In the evening, you hit another store and decide to take the chance to loot it."

    if scav >= 11:
        jump finaldeath1st

    "you will be given the option to explore a couple of rooms"

    "It's just like before goodluck!"

    #front room
    $ bottomshelfright = 0
    $ middleofdesk = 0

    # backroom
    $ bottomshelfleftcabinet = 0
    $ bottomshelfrightcabinet = 0

    menu fir2:
        "exit store":
            play sound "audio/leavescav.mp3" volume 1.2 fadeout 1.0
            pause 3.0
            jump day2

        "front room":
            $ scav += 2
            "you turn on the lights!(+2 awareness)"
            window hide
            play sound "audio/lightswitch.mp3" volume 1.2 fadeout 1.0
            pause 1.0
            scene frontroomd2 with fade
            pause 2.0
            scene black with fade
            show text "you have [scav] awareness." at top
            jump beforefront

        "backroom":
            $ scav += 2
            "you turn on the lights!(+2 awareness)"
            play sound "audio/lightswitch.mp3" volume 1.2 fadeout 1.0
            window hide
            pause 1.0
            scene backroomd2 with fade
            pause 2.0
            scene black with fade
            show text "you have [scav] awareness." at top
            jump beforeback

    menu beforefront:
        "turn lights on again +2 awareness":
            window hide
            $ scav += 2
            scene frontroomd2 with fade
            pause 2.0
            scene black with fade
            jump beforefront

        "search":
            jump front

        "leave":
            show text "you have [scav] awareness." at top
            jump fir2

    menu front:
        "Top shelf middle (+1 AWARENESS)":
            $ scav += 1
            "nothing here"
            jump beforefront

        "Bottom shelf right (+1 AWARENESS)":
            $ scav += 1
            if bottomshelfright == 0:
                "you got food"
                $ bottomshelfright += 1
                $ food += 1
                jump beforefront
            elif bottomshelfright == 1:
                "nothing left"
                jump beforefront

        "Bottom shelf left (+1 AWARENESS)":
            $ scav += 1
            "you reach out..."
            "you almost touch the tendril but stop before you get it's attention"
            "while backing away from it you drop something..."
            "-1 food"
            $ food -= 1
            jump beforefront

        "Left under bottom shelf (+1 AWARENESS)":
            "hammer"
            $ scav += 1
            jump beforefront

        "Middle of desk(+1 AWARENESS)":
            $ scav += 1
            if middleofdesk == 0:
                "you got food"
                $ middleofdesk += 1
                $ food += 1
            elif middleofdesk == 1:
                "nothing left"
            jump beforefront

    menu beforeback:
        "leave":
            show text "you have [scav] awareness." at top

        "turn lights on again(+2 awareness)":
            "MEOW"

        "search":
            jump back

    menu back:
        "Bottom shelf left cabinet":
            $ scav += 1
            if bottomshelfleftcabinet == 0:
                "you found food"
                $ food += 1
                $ bottomshelfleftcabinet += 1
            elif bottomshelfleftcabinet == 1:
                "nothing left"
            jump beforeback

        "Top shelf left cabinet":
            $ scav += 1
            "nope"
            jump beforeback

        "Bottom shelf right cabinet":
            $ scav += 1
            if bottomshelfrightcabinet == 0:
                "you got food"
                $ food += 1
                $ bottomshelfrightcabinet += 1
            elif bottomshelfrightcabinet == 1:
                "nothing left"
            jump beforeback

        "Middle shelf right cabinet":
            $ scav += 1
            "MEOW"

        "On skull":
            $ scav += 1
            if weapon == 0:
                $ weapon += 3
                show hammerfound at appear_top:
                    zoom 1.0
                    xpos 0.86
                    ypos 1.00
                pause 20.0
                hide hammerfound with fade
            elif weapon == 3:
                "you already have a weapon do you want to keep it or change it"
                menu weaponchoose3:
                    "keep your weapon":
                        jump beforeback
                    "take new weapon":
                        show hammerfound at appear_top:
                            zoom 1.0
                            xpos 0.86
                            ypos 1.00
                        pause 20.0
                        hide hammerfound with fade
            elif weapon == 1:
                "you already have a weapon do you want to keep it or change it"
                jump weaponchoose3
            elif weapon == 2:
                "you already have a weapon do you want to keep it or change it"
                jump weaponchoose3
            elif weapon == 4:
                "you already have a weapon do you want to keep it or change it"
                jump weaponchoose3
            jump beforeback
