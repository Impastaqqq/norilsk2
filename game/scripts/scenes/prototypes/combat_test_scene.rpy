# game/scripts/scenes/prototypes/combat_test_scene.rpy

default combat_service = CombatService()

label combat_test_scene:
    scene black

    python:
        combat_service.start_combat()

    call screen combat_main(combat_service)
    return
