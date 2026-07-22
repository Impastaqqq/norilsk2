# game/scripts/dictionaries/enemies_db.rpy

init -1 python:
    from typing import Dict, Any, List

    # Master Enemy Database Dictionary
    ENEMIES_DB: Dict[str, Dict[str, Any]] = {
        EnemyType.SMALL_TENDRIL: {
            "name": "Small Tendril",
            "enemy_type": EnemyType.SMALL_TENDRIL,
            "max_hp": 50,
            "attack_min": 5,
            "attack_max": 10,
            "enemy_sprite": "images/combat/enemy_full.gif",
            "hit_overlay_sprite": "images/combat/enemy_hit.gif",
            "body_parts": [
                {"name": "Top Tendril", "threshold_hp": 25},
                {"name": "Main Core", "threshold_hp": 0}
            ]
        },
        EnemyType.MEDIUM_TENDRIL: {
            "name": "Medium Tendril",
            "enemy_type": EnemyType.MEDIUM_TENDRIL,
            "max_hp": 90,
            "attack_min": 10,
            "attack_max": 20,
            "enemy_sprite": "images/combat/enemy_full.gif",
            "hit_overlay_sprite": "images/combat/enemy_hit.gif",
            "body_parts": [
                {"name": "Top Part", "threshold_hp": 60},
                {"name": "Middle Part", "threshold_hp": 30},
                {"name": "Base", "threshold_hp": 0}
            ]
        },
        EnemyType.PARASITIC_TENDRIL: {
            "name": "Parasitic Tendril",
            "enemy_type": EnemyType.PARASITIC_TENDRIL,
            "max_hp": 120,
            "attack_min": 10,
            "attack_max": 15,
            "enemy_sprite": "images/combat/enemy_full.gif",
            "hit_overlay_sprite": "images/combat/enemy_hit.gif",
            "body_parts": [
                {"name": "Part 1", "threshold_hp": 60},
                {"name": "Part 2", "threshold_hp": 30},
                {"name": "Core", "threshold_hp": 0}
            ]
        },
        EnemyType.BEHEMOTH: {
            "name": "Behemoth",
            "enemy_type": EnemyType.BEHEMOTH,
            "max_hp": 200,
            "attack_min": 40,
            "attack_max": 40,
            "enemy_sprite": "images/combat/enemy_full.gif",
            "hit_overlay_sprite": "images/combat/enemy_hit.gif",
            "body_parts": [
                {"name": "Arm 1", "threshold_hp": 150},
                {"name": "Arm 2", "threshold_hp": 100},
                {"name": "Carapace", "threshold_hp": 50},
                {"name": "Head Core", "threshold_hp": 0}
            ]
        },
        EnemyType.LEVIATHAN: {
            "name": "Leviathan",
            "enemy_type": EnemyType.LEVIATHAN,
            "max_hp": 200,
            "attack_min": 10,
            "attack_max": 30,
            "enemy_sprite": "images/combat/enemy_full.gif",
            "hit_overlay_sprite": "images/combat/enemy_hit.gif",
            "body_parts": [
                {"name": "Tentacle 1", "threshold_hp": 150},
                {"name": "Tentacle 2", "threshold_hp": 100},
                {"name": "Eye Shell", "threshold_hp": 50},
                {"name": "Mouth", "threshold_hp": 0}
            ]
        },
        EnemyType.FINAL_BOSS: {
            "name": "Final Boss",
            "enemy_type": EnemyType.FINAL_BOSS,
            "max_hp": 210,
            "attack_min": 40,
            "attack_max": 40,
            "enemy_sprite": "images/combat/enemy_full.gif",
            "hit_overlay_sprite": "images/combat/enemy_hit.gif",
            "body_parts": [
                {"name": "Crown", "threshold_hp": 168},
                {"name": "Left Wing", "threshold_hp": 126},
                {"name": "Right Wing", "threshold_hp": 84},
                {"name": "Chest Plate", "threshold_hp": 42},
                {"name": "Heart Core", "threshold_hp": 0}
            ]
        }
    }

    def create_enemy_from_db(enemy_type: str = EnemyType.SMALL_TENDRIL) -> EnemyData:
        """
        Factory function creating an EnemyData instance from ENEMIES_DB template.
        """
        data = ENEMIES_DB.get(enemy_type)
        if not data:
            data = ENEMIES_DB[EnemyType.SMALL_TENDRIL]

        body_parts = [
            BodyPart(name=p["name"], threshold_hp=p["threshold_hp"])
            for p in data["body_parts"]
        ]

        return EnemyData(
            name=data["name"],
            max_hp=data["max_hp"],
            body_parts=body_parts,
            attack_min=data["attack_min"],
            attack_max=data["attack_max"],
            enemy_sprite=data["enemy_sprite"],
            hit_overlay_sprite=data["hit_overlay_sprite"],
            enemy_type=data["enemy_type"]
        )
