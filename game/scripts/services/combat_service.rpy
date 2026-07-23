# game/scripts/services/combat_service.rpy

init -1 python:
    import random
    from typing import List, Optional

    class CombatService(renpy.store.object):
        def __init__(self):
            super().__init__()
            self.player: PlayerCombatState = PlayerCombatState(max_hp=100, food_count=3, weapon=create_weapon_from_db("Knife"))
            self.enemy: EnemyData = create_enemy_from_db(EnemyType.SMALL_TENDRIL)
            self.log: CombatLog = CombatLog()

            self.current_targets: List[QTETarget] = []
            self.completed_stage_targets: List[QTETarget] = []
            self.current_stage: int = 1
            self.total_stages: int = 1
            self.turn_number: int = 1
            self.qte_active: bool = False
            self.qte_time_remaining: float = 10.0

            self.show_hit_overlay: bool = False
            self.hit_overlay_timer: float = 0.0

            self.show_log: bool = True

        def start_combat(self, weapon: Optional[WeaponData] = None, enemy_type: str = EnemyType.SMALL_TENDRIL) -> None:
            if weapon:
                self.player.equipped_weapon = weapon
            else:
                self.player.equipped_weapon = create_weapon_from_db("Knife")

            self.player.hp = self.player.max_hp
            self.enemy = create_enemy_from_db(enemy_type)
            self.current_targets = []
            self.completed_stage_targets = []
            self.current_stage = 1
            self.total_stages = 1
            self.turn_number = 1
            self.qte_active = False
            self.show_hit_overlay = False
            self.log.clear()
            self.log.add(f"Encounter Started: Player vs {self.enemy.name}.")
            self.log.add(f"Equipped Weapon: {self.player.equipped_weapon.name}")

        def select_weapon(self, weapon_name: str) -> None:
            self.player.equipped_weapon = create_weapon_from_db(weapon_name)
            self.log.add(f"Debug: Weapon switched to {self.player.equipped_weapon.name}.")

        def restart_combat(self) -> None:
            weapon = self.player.equipped_weapon
            self.start_combat(weapon)
            self.log.add("Debug: Combat Restarted.")

        def toggle_log(self) -> None:
            self.show_log = not self.show_log

        def start_qte_phase(self) -> None:
            if self.enemy.current_hp <= 0 or self.player.hp <= 0:
                return

            weapon = self.player.equipped_weapon
            self.qte_time_remaining = weapon.time_limit
            self.qte_active = True
            self.show_hit_overlay = False
            self.current_stage = 1
            self.total_stages = len(weapon.stages)
            self.completed_stage_targets = []

            # Log Player turn header highlighted with color
            self.log.add(f"{{color=#ffcc00}}{{b}}Turn {self.turn_number}, Player{{/b}}{{/color}}")
            self._spawn_stage_targets()
            self.log.add(f"QTE Started! Total Timer: {weapon.time_limit:.1f}s across {self.total_stages} stages.")
            renpy.restart_interaction()

        def _spawn_stage_targets(self) -> None:
            weapon = self.player.equipped_weapon
            items_count = weapon.stages[self.current_stage - 1]

            positions = generate_qte_positions(
                layout_type=weapon.layout_type,
                num_points=items_count,
                pattern_params=weapon.pattern_params
            )

            target_id_offset = len(self.completed_stage_targets)
            self.current_targets = []
            for i, (x, y) in enumerate(positions):
                target = QTETarget(
                    target_id=target_id_offset + i + 1,
                    x=x,
                    y=y,
                    sprite=weapon.qte_sprite
                )
                self.current_targets.append(target)

            self.log.add(f"Stage {self.current_stage}/{self.total_stages} Spawned: {items_count} QTE targets ({weapon.layout_type}).")

        def click_target(self, target_id: int) -> None:
            if not self.qte_active:
                return

            for target in self.current_targets:
                if target.target_id == target_id and not target.is_clicked:
                    target.mark_hit()  # Sets is_clicked = True, opacity = 0.5
                    self.log.add(f"Hit target #{target_id}! (Opacity -> 50%)")
                    break

            # Check if all active stage targets are hit
            all_hit = all(t.is_clicked for t in self.current_targets)
            if all_hit:
                self.completed_stage_targets.extend(self.current_targets)
                if self.current_stage < self.total_stages:
                    self.current_stage += 1
                    self._spawn_stage_targets()
                else:
                    self.evaluate_qte_result()

        def evaluate_qte_result(self) -> None:
            if not self.qte_active:
                return

            self.qte_active = False
            weapon = self.player.equipped_weapon

            all_targets = list(self.completed_stage_targets)
            # If timer expired before stage completion, append current stage targets
            for t in self.current_targets:
                if t not in all_targets:
                    all_targets.append(t)

            total_targets = len(all_targets)
            hit_targets = sum(1 for t in all_targets if t.is_clicked)

            damage = 0
            if weapon.weapon_type == WeaponType.SLASHING:
                if hit_targets == total_targets and total_targets > 0:
                    damage = weapon.min_damage
                    self.log.add(f"PERFECT! Knife 100% combo hit for {damage} Slashing damage!")
                else:
                    damage = 0
                    self.log.add(f"MISSED! Slashing weapon combo broken ({hit_targets}/{total_targets} hits) -> 0 Damage.")

            elif weapon.weapon_type == WeaponType.BLUNT:
                ratio = hit_targets / float(total_targets) if total_targets > 0 else 0.0
                base_roll = random.randint(weapon.min_damage, weapon.max_damage)
                damage = int(base_roll * ratio)
                self.log.add(f"BLUNT HIT! Hammer dealt {damage} damage ({hit_targets}/{total_targets} hits).")

                if hit_targets == total_targets and total_targets > 0:
                    self.enemy.is_stunned = True
                    self.log.add("STUN APPLIED! 100% Blunt hit stunned the enemy for 1 turn!")

            else:  # REGULAR
                ratio = hit_targets / float(total_targets) if total_targets > 0 else 0.0
                damage = int(random.randint(weapon.min_damage, weapon.max_damage) * ratio)
                self.log.add(f"ATTACK: Dealt {damage} damage.")

            # Apply damage to enemy
            self.enemy.current_hp = max(0, self.enemy.current_hp - damage)

            # Show hit overlay for 1s only on successful damage attack
            if damage > 0:
                self.show_hit_overlay = True
                self.hit_overlay_timer = 1.0

            self._evaluate_body_parts()

            if self.enemy.current_hp <= 0:
                self.log.add(f"VICTORY! {self.enemy.name} has been destroyed!")
            else:
                self.process_enemy_turn()

        def _evaluate_body_parts(self) -> None:
            for part in self.enemy.body_parts:
                if not part.is_broken and self.enemy.current_hp <= part.threshold_hp:
                    part.is_broken = True
                    self.log.add(f"PART DESTROYED: {self.enemy.name}'s [{part.name}] broke!")

        def process_enemy_turn(self) -> None:
            if self.enemy.current_hp <= 0:
                return

            # Log Enemy turn header highlighted with color
            self.log.add(f"{{color=#ff6666}}{{b}}Turn {self.turn_number}, Enemy{{/b}}{{/color}}")

            if self.enemy.is_stunned:
                self.enemy.is_stunned = False
                self.log.add(f"ENEMY STUNNED: {self.enemy.name} skips their attack turn!")
            else:
                damage = random.randint(self.enemy.attack_min, self.enemy.attack_max)
                self.player.hp = max(0, self.player.hp - damage)
                self.log.add(f"ENEMY COUNTER: {self.enemy.name} attacks for {damage} damage! Player HP: {self.player.hp}/{self.player.max_hp}")
                if self.player.hp <= 0:
                    self.log.add("DEFEAT: Player has fallen in combat!")

            # Advance turn counter for next player action
            self.turn_number += 1

        def tick_timer(self, dt: float = 0.1) -> None:
            if self.show_hit_overlay:
                self.hit_overlay_timer -= dt
                if self.hit_overlay_timer <= 0.0:
                    self.show_hit_overlay = False
                    self.hit_overlay_timer = 0.0

            if self.qte_active:
                self.qte_time_remaining -= dt
                if self.qte_time_remaining <= 0.0:
                    self.qte_time_remaining = 0.0
                    self.log.add("TIME EXPIRED! QTE timer reached 0.")
                    self.evaluate_qte_result()

        def heal_player(self) -> None:
            if self.qte_active:
                return

            self.log.add(f"{{color=#ffcc00}}{{b}}Turn {self.turn_number}, Player{{/b}}{{/color}}")
            if self.player.food_count > 0 and self.player.hp < self.player.max_hp:
                self.player.food_count -= 1
                heal_amt = 25
                self.player.hp = min(self.player.max_hp, self.player.hp + heal_amt)
                self.log.add(f"HEALED: Restored +{heal_amt} HP using food item. Food left: {self.player.food_count}. Player HP: {self.player.hp}/{self.player.max_hp}")
                self.process_enemy_turn()
            elif self.player.food_count <= 0:
                self.log.add("HEAL FAILED: No food items remaining!")
            else:
                self.log.add("HEAL FAILED: Player HP already full.")
