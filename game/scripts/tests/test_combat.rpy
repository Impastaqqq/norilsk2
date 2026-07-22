# game/scripts/tests/test_combat.rpy

testsuite combat_service_tests:
    setup:
        python:
            # Verify class inheritance for save/load/rollback support
            assert issubclass(WeaponData, renpy.store.object), "WeaponData must subclass renpy.store.object"
            assert issubclass(EnemyData, renpy.store.object), "EnemyData must subclass renpy.store.object"
            assert issubclass(QTETarget, renpy.store.object), "QTETarget must subclass renpy.store.object"
            assert issubclass(CombatService, renpy.store.object), "CombatService must subclass renpy.store.object"

    testcase test_qte_positioning_knife_arc:
        python:
            points = generate_knife_arc(center_x=960, center_y=540, length=600, curvature=0.4, num_points=5, randomize_shape=False)
            assert len(points) == 5, f"Expected 5 points, got {len(points)}"
            # Center point (index 2) should have higher elevation (smaller Y) than endpoints
            start_y = points[0][1]
            mid_y = points[2][1]
            assert mid_y < start_y, f"Arc peak Y ({mid_y}) should be smaller than start Y ({start_y})"

    testcase test_qte_positioning_hammer_square:
        python:
            points = generate_hammer_square(center_x=960, center_y=540, size=300, num_points=4, randomize_shape=False)
            assert len(points) == 4, f"Expected 4 points, got {len(points)}"
            # Verify top-left corner
            assert points[0] == (810, 390), f"Expected top-left corner (810, 390), got {points[0]}"
            # Verify bottom-right corner
            assert points[2] == (1110, 690), f"Expected bottom-right corner (1110, 690), got {points[2]}"

    testcase test_target_opacity_change_on_hit:
        python:
            target = QTETarget(target_id=1, x=100, y=100, sprite="images/combat/qte_knife.png")
            assert target.opacity == 1.0, "Initial target opacity should be 1.0"
            assert not target.is_clicked, "Initial target should not be clicked"

            target.mark_hit()
            assert target.opacity == 0.5, f"Target opacity on hit should be 0.5, got {target.opacity}"
            assert target.is_clicked, "Target should be marked clicked"

    testcase test_knife_slashing_all_or_nothing_damage:
        python:
            service = CombatService()
            service.start_combat(create_weapon_from_db("Knife"))
            service.start_qte_phase()

            # Scenario A: Miss 1 target in Stage 1
            assert service.current_stage == 1, "Should start at Stage 1"
            assert len(service.current_targets) == 5, f"Stage 1 should have 5 arc QTE items, got {len(service.current_targets)}"
            # Click 4 targets out of 5 in Stage 1
            for target in service.current_targets[:-1]:
                service.click_target(target.target_id)
            service.evaluate_qte_result()

            # Missed combo should result in 0 damage and NO hit overlay
            assert service.enemy.current_hp == 50, f"Expected 50 HP on missed combo, got {service.enemy.current_hp}"
            assert not service.show_hit_overlay, "Hit overlay should NOT show on missed attack (0 damage)"

            # Scenario B: 100% hits across both Stage 1 (5 targets) and Stage 2 (5 targets)
            service.start_combat(create_weapon_from_db("Knife"))
            service.start_qte_phase()

            # Stage 1 (5 items)
            for target in list(service.current_targets):
                service.click_target(target.target_id)

            # Auto-advanced to Stage 2
            assert service.current_stage == 2, f"Expected Stage 2, got {service.current_stage}"
            assert len(service.current_targets) == 5, f"Stage 2 should have 5 arc QTE items, got {len(service.current_targets)}"
            # Stage 2 (5 items)
            for target in list(service.current_targets):
                service.click_target(target.target_id)

            # 100% combo across all stages should deal 20 damage -> 30 HP remaining and show hit overlay
            assert service.enemy.current_hp == 30, f"Expected 30 HP on 100% knife combo, got {service.enemy.current_hp}"
            assert service.show_hit_overlay, "Hit overlay SHOULD show on successful damage attack"

    testcase test_hammer_blunt_damage_and_stun:
        python:
            service = CombatService()
            service.start_combat(create_weapon_from_db("Hammer"))
            service.start_qte_phase()

            # Stage 1 (4 items)
            for target in list(service.current_targets):
                service.click_target(target.target_id)

            # Stage 2 (4 items)
            assert service.current_stage == 2, f"Expected Stage 2, got {service.current_stage}"
            for target in list(service.current_targets):
                service.click_target(target.target_id)

            # 100% hit on Hammer applies stun which causes enemy turn skip (Player HP remains 100)
            assert service.player.hp == 100, f"Player should take 0 damage due to stun skip, got HP {service.player.hp}"
            assert any("STUN APPLIED!" in msg for msg in service.log.entries), "Log should record STUN APPLIED!"
            assert any("ENEMY STUNNED" in msg for msg in service.log.entries), "Log should record ENEMY STUNNED turn skip"
            # Enemy HP should be reduced by base roll (12-18)
            assert service.enemy.current_hp < 50, f"Enemy HP should be reduced from 50, got {service.enemy.current_hp}"

    testcase test_enemy_body_part_destruction:
        python:
            service = CombatService()
            service.start_combat(create_weapon_from_db("Knife"))

            top_tendril = service.enemy.body_parts[0]
            assert not top_tendril.is_broken, "Top tendril should start unbroken"

            # Directly reduce enemy HP to 25 (threshold for Top Tendril)
            service.enemy.current_hp = 25
            service._evaluate_body_parts()

            assert top_tendril.is_broken, "Top tendril should be broken at 25 HP remaining"

    testcase test_enemies_database_dictionary:
        python:
            # Verify database dictionary entries
            assert EnemyType.SMALL_TENDRIL in ENEMIES_DB, "SMALL_TENDRIL must exist in ENEMIES_DB"
            assert EnemyType.BEHEMOTH in ENEMIES_DB, "BEHEMOTH must exist in ENEMIES_DB"

            # Create Behemoth from DB factory
            behemoth = create_enemy_from_db(EnemyType.BEHEMOTH)
            assert behemoth.name == "Behemoth", f"Expected name Behemoth, got {behemoth.name}"
            assert behemoth.max_hp == 200, f"Expected 200 HP for Behemoth, got {behemoth.max_hp}"
            assert len(behemoth.body_parts) == 4, f"Expected 4 body parts for Behemoth, got {len(behemoth.body_parts)}"

    testcase test_weapons_database_dictionary:
        python:
            assert "Knife" in WEAPONS_DB, "Knife must exist in WEAPONS_DB"
            assert "Chainsaw" in WEAPONS_DB, "Chainsaw must exist in WEAPONS_DB"

            chainsaw = create_weapon_from_db("Chainsaw")
            assert chainsaw.name == "Chainsaw", f"Expected Chainsaw name, got {chainsaw.name}"
            assert chainsaw.weapon_type == WeaponType.SLASHING, f"Expected SLASHING type, got {chainsaw.weapon_type}"
            assert chainsaw.min_damage == 50, f"Expected 50 min damage, got {chainsaw.min_damage}"

    testcase test_combat_screen_ui_flow:
        python:
            # 1. Combat Start: Instantiate CombatService & start combat
            service = CombatService()
            knife = create_weapon_from_db("Knife")
            service.start_combat(knife)

            # Show screen and verify combat start state
            renpy.show_screen("combat_main", combat_service=service)
            assert service.enemy.current_hp == 50, f"Expected initial enemy HP to be 50, got {service.enemy.current_hp}"
            assert not service.qte_active, "QTE should initially be inactive"

            # 2. Start QTE Phase (Simulating 'FIGHT (QTE)' action button click)
            service.start_qte_phase()
            assert service.qte_active, "QTE phase should be active after pressing FIGHT"
            assert service.current_stage == 1, f"Expected Stage 1, got {service.current_stage}"

            # 3. Press all QTE events across all stages (Stage 1 & Stage 2)
            while service.qte_active and service.current_stage <= service.total_stages:
                targets = list(service.current_targets)
                assert len(targets) > 0, "Current targets list should not be empty during QTE phase"
                for target in targets:
                    service.click_target(target.target_id)

            # 4. Damage Dealt verification
            assert not service.qte_active, "QTE phase should finish after pressing all target buttons"
            assert service.enemy.current_hp < 50, f"Enemy HP should decrease after successful QTE combo, got {service.enemy.current_hp}"
            assert service.enemy.current_hp == 30, f"Expected 30 HP remaining (20 damage dealt), got {service.enemy.current_hp}"
            assert service.show_hit_overlay, "Hit overlay should be active on enemy after taking damage"

            # Clean up screen state
            renpy.hide_screen("combat_main")


testsuite combat_e2e_ui_tests:
    testcase test_e2e_combat_button_clicks:
        # 1. Start Combat & Render Screen
        $ test_service = CombatService()
        $ test_service.start_combat(create_weapon_from_db("Knife"))
        $ renpy.show_screen("combat_main", combat_service=test_service)
        pause 0.2

        # 2. Imitate User Action: Click "FIGHT (QTE)" screen button by matching rendered UI text
        click "FIGHT (QTE)"
        pause 0.2
        $ assert test_service.qte_active, "QTE should be active after clicking FIGHT (QTE) button"

        # 3. Imitate User Actions: Click QTE target buttons
        python:
            while test_service.qte_active and test_service.current_stage <= test_service.total_stages:
                targets = list(test_service.current_targets)
                for target in targets:
                    test_service.click_target(target.target_id)

        pause 0.2

        # 4. Assert Damage Dealt & UI state after E2E UI clicks
        $ assert not test_service.qte_active, "QTE should finish"
        $ assert test_service.enemy.current_hp == 30, f"Expected 30 HP remaining, got {test_service.enemy.current_hp}"
        $ assert test_service.show_hit_overlay, "Hit overlay should be active"

        $ renpy.hide_screen("combat_main")






