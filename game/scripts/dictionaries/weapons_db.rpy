# game/scripts/dictionaries/weapons_db.rpy

init -1 python:
    from typing import Dict, Any, List

    # Master Weapon Database Dictionary
    WEAPONS_DB: Dict[str, Dict[str, Any]] = {
        "Knife": {
            "name": "Knife",
            "weapon_type": WeaponType.SLASHING,
            "min_damage": 20,
            "max_damage": 20,
            "time_limit": 10.0,
            "layout_type": "ARC",
            "num_targets": 10,
            "stages": [5, 5],
            "qte_sprite": "images/combat/qte_knife.png",
            "pattern_params": {"length": 650, "curvature": 0.45, "center_x": 960, "center_y": 540}
        },
        "Hammer": {
            "name": "Hammer",
            "weapon_type": WeaponType.BLUNT,
            "min_damage": 12,
            "max_damage": 18,
            "time_limit": 14.0,
            "layout_type": "SQUARE",
            "num_targets": 8,
            "stages": [4, 4],
            "qte_sprite": "images/combat/qte_hammer.png",
            "pattern_params": {"size": 360, "center_x": 960, "center_y": 540}
        },
        "Stick": {
            "name": "Stick",
            "weapon_type": WeaponType.REGULAR,
            "min_damage": 10,
            "max_damage": 15,
            "time_limit": 15.0,
            "layout_type": "RANDOM",
            "num_targets": 6,
            "stages": [6],
            "qte_sprite": "images/combat/qte_hammer.png",
            "pattern_params": {}
        },
        "Sledge Hammer": {
            "name": "Sledge Hammer",
            "weapon_type": WeaponType.BLUNT,
            "min_damage": 10,
            "max_damage": 24,
            "time_limit": 12.0,
            "layout_type": "SQUARE",
            "num_targets": 8,
            "stages": [4, 4],
            "qte_sprite": "images/combat/qte_hammer.png",
            "pattern_params": {"size": 400, "center_x": 960, "center_y": 540}
        },
        "Taser": {
            "name": "Taser",
            "weapon_type": WeaponType.BLUNT,
            "min_damage": 8,
            "max_damage": 14,
            "time_limit": 8.0,
            "layout_type": "SQUARE",
            "num_targets": 4,
            "stages": [2, 2],
            "qte_sprite": "images/combat/qte_hammer.png",
            "pattern_params": {"size": 300, "center_x": 960, "center_y": 540}
        },
        "Chainsaw": {
            "name": "Chainsaw",
            "weapon_type": WeaponType.SLASHING,
            "min_damage": 50,
            "max_damage": 50,
            "time_limit": 10.0,
            "layout_type": "ARC",
            "num_targets": 10,
            "stages": [5, 5],
            "qte_sprite": "images/combat/qte_knife.png",
            "pattern_params": {"length": 750, "curvature": 0.5, "center_x": 960, "center_y": 540}
        },
        "Katana": {
            "name": "Katana",
            "weapon_type": WeaponType.SLASHING,
            "min_damage": 30,
            "max_damage": 30,
            "time_limit": 15.0,
            "layout_type": "ARC",
            "num_targets": 15,
            "stages": [5, 5, 5],
            "qte_sprite": "images/combat/qte_knife.png",
            "pattern_params": {"length": 700, "curvature": 0.4, "center_x": 960, "center_y": 540}
        },
        "Axe": {
            "name": "Axe",
            "weapon_type": WeaponType.SLASHING,
            "min_damage": 35,
            "max_damage": 35,
            "time_limit": 12.0,
            "layout_type": "ARC",
            "num_targets": 10,
            "stages": [5, 5],
            "qte_sprite": "images/combat/qte_knife.png",
            "pattern_params": {"length": 650, "curvature": 0.45, "center_x": 960, "center_y": 540}
        },
        "Gun": {
            "name": "Gun",
            "weapon_type": WeaponType.REGULAR,
            "min_damage": 10,
            "max_damage": 25,
            "time_limit": 10.0,
            "layout_type": "RANDOM",
            "num_targets": 4,
            "stages": [4],
            "qte_sprite": "images/combat/qte_knife.png",
            "pattern_params": {}
        },
        "Ice Pick": {
            "name": "Ice Pick",
            "weapon_type": WeaponType.REGULAR,
            "min_damage": 15,
            "max_damage": 24,
            "time_limit": 8.0,
            "layout_type": "RANDOM",
            "num_targets": 4,
            "stages": [4],
            "qte_sprite": "images/combat/qte_knife.png",
            "pattern_params": {}
        }
    }

    def create_weapon_from_db(weapon_name: str = "Knife") -> WeaponData:
        """
        Factory function instantiating a WeaponData object from WEAPONS_DB.
        """
        data = WEAPONS_DB.get(weapon_name)
        if not data:
            data = WEAPONS_DB["Knife"]

        stages = data.get("stages", [data["num_targets"]])
        total_targets = sum(stages)

        return WeaponData(
            name=data["name"],
            weapon_type=data["weapon_type"],
            min_damage=data["min_damage"],
            max_damage=data["max_damage"],
            time_limit=data["time_limit"],
            layout_type=data["layout_type"],
            num_targets=total_targets,
            qte_sprite=data["qte_sprite"],
            pattern_params=dict(data["pattern_params"]),
            stages=list(stages)
        )
