# game/scripts/tests/test_trivial_ui.rpy

screen test_trivial_screen():
    textbutton "Test Button" action Return()

testsuite trivial_e2e_ui_tests:
    setup:
        python:
            from renpy.test.testsettings import _test
            _test.timeout = 15.0

    testcase test_trivial_click:
        $ renpy.show_screen("test_trivial_screen")
        pause 0.2
        click "Test Button"
        pause 0.2
        $ renpy.hide_screen("test_trivial_screen")
