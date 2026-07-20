# The script of the game goes in this file.

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
    "sam1"
    pause 0.3
    "sam2"
    pause 0.3
    "sam3"
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
    "attack1"
    pause 0.3
    "attack2"
    pause 0.3
    "attack3"
    pause 0.3
    repeat



# The game starts here.
label start:

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

    scene d12-3 with fade

    

    pause 1.0

    play music "night.mp3" volume 0.75 fadeout 1.0

    queue radio "samvoice.mp3" fadein 1.0 volume 0.10 loop

    play sound "audio/walkingwforest.mp3" volume 0.40

    "A group of scientists funded by the government were tasked to drill into the center of the earth."

    "While Digging they found nothing useful and nearly couldn’t complete the operation but eventually…"

    

    scene d14 with fade 

    "they hit something…"

    scene d15 with fade

    "And something was released…"

    scene black with fade

    pause 1.0

    scene d7 with dissolve

    "you were 12 when the apocalypse happened"

    "Your mother was a scientist who worked on the drilling project that started this all"

    scene black with fade

    pause 1.0

    "No scientist survived that project…"

    scene d19 with fade

    "after it began your father traveled with you to teach you how to survive"

    "Around your eighteenth birthday, your father was caught off guard"

    scene black

    "he died..."

    scene d111 with dissolve

    "The only thing he left was the knowledge he gave you and the radio he made"

    window hide 

    scene blank with dissolve

    
    play sound "time.mp3" volume 1.50
    show tutorial with moveinleft:
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
            



            
            
            

label finaldeath1st:
        $ renpy.movie_cutscene("images/death1.webm")

        scene black with fade

        mm "I'm sorry honey..."

        mm "It's time you rest, your trip ends here"
        $ scav = 0

        return

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
                    ##################### make werid noise 
                    "there's more than just animal meat"
                    jump beforeleft
            
        
            "left shelf(+1 AWARENESS)":
            
            #get food

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
                        
                    ##########################################################################################
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

    
                
                    


                    ####################################################################################


            
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
        

    
        
  















    ## scav
label afterscav:
        stop music fadeout 1.5
        stop sound fadeout 1.5
        show d112-13 with fade


        "You walk out of the gas station and start to make your way back onto the road but then… (have the radio playing loudly)"

        

        scene black with fade

        show attack1st with fade
        play sound "firstfightsam.mp3" volume 0.1 


        

        "на теья напали!"

        pause 10.00

        hide attack1st
        play sound "audio/run.mp3" volume 1.2 fadeout 1.0

        pause 2.0

        scene d115 with dissolve
        
                

        "You run away and make it back on the path"

        scene black with fade
        play sound "forestfire.mp3" volume 0.50 fadeout 1.0
        pause 1.5
        play music "tellme.mp3" volume 1.0 fadeout 1.0



        "It’s getting late you're going to have to camp out"

        scene d118 with fade

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

        $ scav == 0

        
        jump scavday2




label scavday2:
    scene black with fade

    "You’ve walked all morning. In the evening, you hit another store and decide to take the chance to loot it."

    if scav >= 11:
            jump finaldeath1st

        #MAKE TRAPS THAT HURT YOU !!!!
        # MAKE THE TIME LESS FURTHER ON!!
        #LESS FOOD!! LATER ON 
        
    "you will be given the option to explore a couple of rooms"

    "It's just like before goodluck!"

    #############################################################make traps that hurt you time less further on less food 





        

        
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






        ###################################################################################################hammerermemrerererer
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
            $ scav +=1

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
            ############################################ edit this for the scikle its set for hammer rn 
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


                



    
       


      







    






label day2:
    #scavegnegegege

    scene black with fade

    "You continue your journey."

    scene d23 with dissolve 

    pause 1.0

    scene d24 with dissolve

    "You see smoke coming from a clearing and decide to investigate."

    "You turn your radio low"

    scene d25 with fade

    "While you sneak behind a rock to check who it is…"

    scene d27

    show jakovangry with moveinbottom:
        zoom 1.4
        xpos 0.10
        ypos 0.10
    with hpunch

    m "WHOEVER’S OUT THERE I HOPE YOU KNOW WE’RE BOTH ARMED!!"
    
    hide jakovangry

    menu d21st:
        "Don't worry I’m harmless I’m just passing by":

            show adamtalkhandsup with easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
            
            a "Don't worry I’m harmless I’m just passing by"
            
            jump d22nd


        "I'm just a kid don't shoot me!":
            show adamtalkhandsup with easeinbottom:
                zoom 0.85
                xpos 0.10
                ypos 0.00
             
            a "I'm just a kid don't shoot me!"
            jump d22nd

    label d22nd:
        hide adamtalkhandsup
        show jakovtalk at appear_right:
            zoom 1.4
            xpos 0.40
            ypos 0.86
    
        m "come out and let me see you."
        hide jakovtalk 

        "You can tell the man has been drinking…"

        show jakovtalk with moveinbottom:
            zoom 1.4
            xpos 0.10
            ypos 0.10

        m "you’re alone?"

        hide jakovtalk

        menu d23rd:

            "yes...":

                show adamtalkhandsup with easeinbottom:
                    zoom 0.85
                    xpos 0.10
                    ypos 0.00

                a "yes..."
                jump d24th
                

            "my father died recently so it's just me…":
                show adamtalkhandsup with easeinbottom:
                    zoom 0.85
                    xpos 0.10
                    ypos 0.00
                
               

                a "my father died recently so it's just me…"
                
                jump d24th
            



    label d24th:
        hide adamtalkhandsup
        show verdietalk at appear_top:
            zoom 1.4
            xpos 0.40
            ypos 0.85

        g "leave him alone Dad he looks my age he’s probably terrified out here."
        hide verdietalk 

        hide verdietalk

        "you can't see the mans eyes but you can feel his eyeroll"

        show verdietalk with moveinbottom:
            zoom 1.4
            xpos 0.10
            ypos 0.10

        g "sit with us we mean no harm to you…"

        hide verdietalk

        scene d215 with dissolve

        

        show jakovtalk with moveinbottom:
            zoom 1.4
            xpos 0.10
            ypos 0.10
    m "where are you coming from?"
    show jakovtalk at left with move:
        xpos 0.05
        ypos 0.90

    show adamtalk with easeinbottom:
        zoom 0.85
        xpos 0.55
        ypos 0.05

    a "I used to live with my father somewhere in the eastern mountains."

    hide jakovtalk 

    show jakovserious with moveinbottom:
        zoom 1.4
        xpos 0.10
        ypos 0.10

    m "why are you here? It's safe where you came from."

    hide jakovserious
    hide adamtalk 

    menu d25th:
        "I'm trying to find my dad's friend…":
            show jakovserious with dissolve:
                zoom 1.4
                xpos 0.10
                ypos 0.10

            show adamtalk at appear_top:
                zoom 0.85
                xpos 0.90
                ypos 0.80
            a "I'm trying to find my dad's friend…"

        "I’m just traveling…":
            show jakovserious:
                zoom 1.4
                xpos 0.10
                ypos 0.10

            show adamtalk at appear_top:
                zoom 0.85
                xpos 0.90
                ypos 0.80
                
            a " I’m just traveling…"
            jump d26th

    label d26th:
        hide jakovserious
        show jakovlook with easeinbottom:
            zoom 1.4
            xpos 0.10
            ypos 0.10
        m "be careful going west we were just attacked by a cluster of those fucking weird tentacle things."

        hide jakovlook
        show jakovangry at appear_top:
            zoom 1.4
            xpos 0.37
            ypos 0.84
        m "I'm so sick of this world lately you can't get a break anymore."
        hide jakovangry

        show jakovlook:
            zoom 1.4
            xpos 0.10
            ypos 0.10

        hide jakovlook
    
        show jakovangry:
            zoom 1.4
            xpos 0.10
            ypos 0.10
        
        m "that weird alien shit then the bandits, and theres cultists roaming around snatching motherfuckers…"

        
        with hpunch
        m "we can't get a break the world had to fucking end just when our lives were getting normal!"
        show jakovangry with move:
            xpos 0.10
            ypos 1.30

        show verdiemad with moveinbottom:
            zoom 1.4
            xpos 0.10
            ypos 0.10

        g "Daughter stop cursing so much…"
        show verdiemad with move:
            xpos 0.26
            ypos 0.10

        show jakovangry at appear_top:
            zoom 1.4
            xpos 0.30
            ypos 0.84

        m "sorry..."
        hide verdiemad
        

        show verdietalk:
            zoom 1.4
            xpos 0.26
            ypos 0.10

        g "sooo what's your name?"

        hide adamtalk


        show adamsad at appear_top:
            zoom 0.85
            xpos 0.90
            ypos 0.80

 

        #   zoom 0.85
        #    xpos 0.56
        #  ypos 0.00
        a "adam."

        show verdietalk at appear_top:
            zoom 1.4
            xpos 0.52
            ypos 0.83



        g " it's nice to meet you Adam I'm so glad to see someone my age for once…! ;)  (is this stupid)"

        hide jakovangry

        show jakovserious:
            zoom 1.4
            xpos 0.03
            ypos 0.09



        m "are you sick of looking at me already?"

        hide jakovserious

        
        show jakovtalk:
            zoom 1.4
            xpos 0.03
            ypos 0.09

        hide verdietalk


        show verdiemad:
            zoom 1.4
            xpos 0.26
            ypos 0.10


        g "don't say that Dad you know what I mean!"

        hide verdiemad

        show verdietalk:
            zoom 1.4
            xpos 0.26
            ypos 0.10

        ve "my name’s verdie, and my dad is Jakov. We used to live near Moscow."  

        hide adamsad

        show adamquestion:
            zoom 0.85
            xpos 0.55
            ypos 0.00



        a "How did you escape?"

        hide adamquestion

        show adamtalk:
            zoom 0.85
            xpos 0.55
            ypos 0.00


        show jakovtalk at appear_top:
            zoom 1.4
            xpos 0.30
            ypos 0.84

        

        

        j "we heard something happened over the news at a freaky research plant, I didn't trust for a second that they would be in control of the situation so I got her and we got the hell out of there"

        hide jakovtalk
        show jakovlook:
            zoom 1.4
            xpos 0.03
            ypos 0.09

        j "I can't believe they tried to downplay it"
        hide jakovlook
        show jakovserious:
            zoom 1.4
            xpos 0.03
            ypos 0.09

        j "if we were there for one more day..."
        hide verdietalk
        show verdiemad:
            zoom 1.4
            xpos 0.26
            ypos 0.10


        ve "let's not think about it"

        show jakovtalk:
            zoom 1.4
            xpos 0.03
            ypos 0.09

        hide jakovserious

        
        j "but hey it's gratifying being able to steal shit without anyone saying anything anymore."
        hide jakovtalk

        show jakovangry:
            zoom 1.4
            xpos 0.03
            ypos 0.09

        j "what I would do to tear up the old office building I used to work at!"

        j "that fuck shit monster already got to it before I could…"

        hide verdiemad

        show verdiemad at appear_top:
            zoom 1.4
            xpos 0.52
            ypos 0.87
        with hpunch

        

        ve "DAD!"

        hide jakovangry

        show jakovlook at appear_top:
            zoom 1.4
            xpos 0.30
            ypos 0.84

        j "SORRY SORRY"

        

        show verdietalk:
            zoom 1.4
            xpos 0.26
            ypos 0.10

        ve " I'm sorry you have to hear my dad rambling…"
        hide adamtalk

        show adamsad with dissolve:
            zoom 0.85
            xpos 0.55
            ypos 0.00

        "it's nice getting a chance to talk to someone…"
        hide jakovlook

        show jakovsick at appear_top:
            zoom 1.4
            xpos 0.30
            ypos 0.84

        j "AMEN!"

        hide jakovlook
        hide verdiemad

        show jakovsick with move:
            xpos 0.30
            ypos 1.84

        show adamsad with move:
            xpos 0.55
            ypos 1.30

        show verdietalk with move:
            xpos 0.26
            ypos 1.30



        "You're sad, you know you have to tread on with your journey,"

        "Plus you don't know the next chance you'll get to meet another girl…..."

        "you get up"

        scene d214 with fade

        show adamtalk with moveinbottom:
            zoom 0.85
            xpos 0.55
            ypos 0.00

        show verdiemad with moveinbottom:
            zoom 1.4
            xpos 0.26
            ypos 0.10

        show jakovtalk with moveinbottom:
            zoom 1.4
            xpos 0.03
            ypos 0.09

        
        hide adamtalk

        show adamsad at appear_top:
            zoom 0.85
            xpos 0.90
            ypos 0.80

        a "I better be going now I still need to travel as much as I can."

        hide verdiemad

        show verdietalk:
            zoom 1.4
            xpos 0.26
            ypos 0.10
        
        ve "awwwww"
        hide jakovtalk

        show jakovserious:
            zoom 1.4
            xpos 0.03
            ypos 0.09

        j "it was nice talking to you Good luck out there kid…"

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


        #the third day !!!!!!

    label scavday3:
        scene d31 with fade
        "You soon meet with a roadblock."

        "There’s a river that you won't be able to swim across and it doesn’t seem like it’ll be easy to walk around it."
        ##meow
        scene d32 with dissolve
        "You step out to look around"

        scene d33 with fade 

        "There’s a store along the shore for you to scavenge! ### maybe use this bg for the candy scene"
        scene black with fade 
        pause 1.5
        ############ scav but you need to find the canoe pieces 
        jump behemoth

        label behemoth:

            scene black with hpunch
            

            "Right when you leave you hear a rumbling coming from the earth…"

            "The trees shake and something comes out from the woods…."
            jump day3



    label day3:
        
        ##### first boss fight 
        # do the thingy finding the person and animation pop up title the behemoth cluster 

        scene d35 with dissolve
        with vpunch 

        "You run away with Eva"

        scene d36 with fade

        "soon you find yourself at the shore"

        "You find a piece of candy on the floor…"

        scene d37 with fade

        "I remember this adam, it was your favorite" # not sure about this is the effective writing .,,, maybe part of it is its a part of adam in his head that he seperates from himelf like how vinn does with her brother 

        "You stare at it briefly before getting in the canoe with eva…"

        scene black with fade 

        pause 1.5

        scene d38 with fade

        pause 4.0

        scene black with fade

        pause 1.0

        scene d310

        "You get across the river, and continue your journey…"

        scene black with fade

        pause 3.0

        scene d312 with fade 

        "It’s getting late soon you need to rest… "

        scene black with fade

        pause 1.0

        scene d313 with fade

        pause 1.00
        play sound "audio/time.mp3" volume 0.5
            

        show clickradio with easeinbottom

        pause 100.00
        ##### RADIO PART 



        ########################Show slide show of Adam moving in the boat on the river




        








    













            


        






        




        

                




    ############################################################################################### add more where its two epole talking to eachother you can lgiht it up or wtv 











    show window 





    return
