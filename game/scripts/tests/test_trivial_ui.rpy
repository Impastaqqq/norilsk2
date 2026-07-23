# game/scripts/tests/test_trivial_ui.rpy

screen test_trivial_screen():
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

label test_trivial_entry_label:
    show screen test_trivial_screen
    return

testsuite trivial_e2e_ui_tests:
    setup:
        python:
            from renpy.test.testsettings import _test
            _test.timeout = 15.0

    testcase test_trivial_click:
        $ renpy.call_in_new_context("test_trivial_entry_label")
        pause 0.2
        python:
            import sys
            import renpy.test.testfocus as testfocus
            import renpy.display.focus as focus_mod
            
            f_item = testfocus.find_focus("Test Button", False)
            print(f"[DIAGNOSTIC] find_focus('Test Button'): {f_item}", flush=True)
            print(f"[DIAGNOSTIC] focus_list length: {len(focus_mod.focus_list)}", flush=True)
            for idx, f in enumerate(focus_mod.focus_list):
                try:
                    w_text = f.widget._tts_all(False) if f.widget else "NoWidget"
                    print(f"[DIAGNOSTIC] focus[{idx}]: widget={f.widget}, text='{w_text}'", flush=True)
                except Exception as ex:
                    print(f"[DIAGNOSTIC] focus[{idx}] error: {ex}", flush=True)
            sys.stdout.flush()
        click "Test Button"
        pause 0.2
        $ renpy.hide_screen("test_trivial_screen")
