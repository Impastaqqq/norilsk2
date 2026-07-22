# game/scripts/models/combat_models.rpy

init -2 python:
    from typing import List, Dict, Any, Optional

    class WeaponType:
        SLASHING = "SLASHING"
        BLUNT = "BLUNT"
        REGULAR = "REGULAR"

    class EnemyType:
        SMALL_TENDRIL = "SMALL_TENDRIL"
        MEDIUM_TENDRIL = "MEDIUM_TENDRIL"
        PARASITIC_TENDRIL = "PARASITIC_TENDRIL"
        BEHEMOTH = "BEHEMOTH"
        LEVIATHAN = "LEVIATHAN"
        FINAL_BOSS = "FINAL_BOSS"

    class WeaponData(renpy.store.object):
        def __init__(
            self,
            name: str,
            weapon_type: str,
            min_damage: int,
            max_damage: int,
            time_limit: float,
            layout_type: str,
            num_targets: int,
            qte_sprite: str,
            pattern_params: Optional[Dict[str, Any]] = None,
            stages: Optional[List[int]] = None
        ):
            super().__init__()
            self.name = name
            self.weapon_type = weapon_type
            self.min_damage = min_damage
            self.max_damage = max_damage
            self.time_limit = time_limit
            self.layout_type = layout_type
            self.num_targets = num_targets
            self.qte_sprite = qte_sprite
            self.pattern_params = pattern_params or {}
            self.stages = stages or [num_targets]

    class BodyPart(renpy.store.object):
        def __init__(self, name: str, threshold_hp: int):
            super().__init__()
            self.name = name
            self.threshold_hp = threshold_hp
            self.is_broken = False

    class EnemyData(renpy.store.object):
        def __init__(
            self,
            name: str,
            max_hp: int,
            body_parts: List[BodyPart],
            attack_min: int,
            attack_max: int,
            enemy_sprite: str = "images/combat/enemy_full.gif",
            hit_overlay_sprite: str = "images/combat/enemy_hit.gif",
            enemy_type: Optional[str] = None
        ):
            super().__init__()
            self.name = name
            self.enemy_type = enemy_type or EnemyType.SMALL_TENDRIL
            self.max_hp = max_hp
            self.current_hp = max_hp
            self.body_parts = body_parts
            self.attack_min = attack_min
            self.attack_max = attack_max
            self.is_stunned = False
            self.enemy_sprite = enemy_sprite
            self.hit_overlay_sprite = hit_overlay_sprite

    class QTETarget(renpy.store.object):
        def __init__(self, target_id: int, x: int, y: int, sprite: str):
            super().__init__()
            self.target_id = target_id
            self.x = x
            self.y = y
            self.sprite = sprite
            self.is_clicked = False
            self.opacity = 1.0

        def mark_hit(self) -> None:
            self.is_clicked = True
            self.opacity = 0.5

    class PlayerCombatState(renpy.store.object):
        def __init__(self, max_hp: int = 100, food_count: int = 3, weapon: Optional[WeaponData] = None):
            super().__init__()
            self.max_hp = max_hp
            self.hp = max_hp
            self.food_count = food_count
            self.equipped_weapon = weapon

    class CombatLog(renpy.store.object):
        def __init__(self):
            super().__init__()
            self.entries: List[str] = []

        def add(self, message: str) -> None:
            self.entries.append(message)

        def clear(self) -> None:
            self.entries = []
