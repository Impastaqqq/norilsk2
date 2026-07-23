# game/scripts/tests/test_trivial_ui.rpy

screen test_trivial_screen():
    tag test_trivial_screen
    modal True
    add "#000d"
    default test_state = "initial"

    frame:
        xalign 0.5
        yalign 0.5
        padding (30, 30)
        background "#121824f2"
        vbox:
            spacing 10
            textbutton "Test Button":
                action SetScreenVariable("test_state", "clicked")
                text_size 20
                text_bold True
                text_color "#ffffff"

testsuite trivial_e2e_ui_tests:
    setup:
        python:
            pass

    testcase test_trivial_click:
        $ renpy.show_screen("test_trivial_screen")
        pause 0.2
        click "Test Button"
        pause 0.2
        $ renpy.hide_screen("test_trivial_screen")
