# game/scripts/services/qte_positioning_service.rpy

init -1 python:
    import math
    import random
    from typing import List, Tuple, Dict, Any

    def generate_knife_arc(
        center_x: int = 960,
        center_y: int = 540,
        length: int = 600,
        curvature: float = 0.4,
        num_points: int = 3,
        randomize_shape: bool = True
    ) -> List[Tuple[int, int]]:
        """
        Generates dynamic positioning along an arc curve of dynamic shape for a fixed number of QTE items.
        :param center_x: Base center X coordinate
        :param center_y: Base center Y coordinate
        :param length: Base horizontal arc span in pixels
        :param curvature: Base curvature magnitude
        :param num_points: Fixed number of QTE target items to generate
        :param randomize_shape: If True, dynamically randomizes arc curvature, angle, and span shape
        """
        points = []
        if num_points <= 0:
            return []

        # Dynamic arc shape randomization
        if randomize_shape:
            length = random.randint(int(length * 0.85), int(length * 1.15))
            # Randomize curvature magnitude and curve orientation (upward vs downward curve)
            curve_mag = random.uniform(0.3, 0.55)
            orientation = random.choice([1, -1])
            curvature = curve_mag * orientation
            center_x += random.randint(-100, 100)
            center_y += random.randint(-60, 60)

        if num_points == 1:
            return [(center_x, center_y)]

        half_len = length / 2.0
        start_x = center_x - half_len

        for i in range(num_points):
            t = i / float(num_points - 1)  # 0.0 to 1.0
            x = start_x + t * length
            # Quadratic arc curve calculation
            arc_height = length * curvature
            y = center_y - (4.0 * arc_height * t * (1.0 - t))
            points.append((int(x), int(y)))

        return points


    def generate_hammer_square(
        center_x: int = 960,
        center_y: int = 540,
        size: int = 350,
        num_points: int = 4,
        randomize_shape: bool = True
    ) -> List[Tuple[int, int]]:
        """
        Generates dynamic positioning along a square perimeter of variable size for fixed number of QTE items.
        """
        if randomize_shape:
            size = random.randint(int(size * 0.85), int(size * 1.15))
            center_x += random.randint(-80, 80)
            center_y += random.randint(-60, 60)

        half_size = size / 2.0
        x_min = center_x - half_size
        x_max = center_x + half_size
        y_min = center_y - half_size
        y_max = center_y + half_size

        corners = [
            (int(x_min), int(y_min)),  # Top-Left
            (int(x_max), int(y_min)),  # Top-Right
            (int(x_max), int(y_max)),  # Bottom-Right
            (int(x_min), int(y_max)),  # Bottom-Left
        ]

        if num_points == 4:
            return corners
        elif num_points <= 0:
            return []

        # Distribute along perimeter for num_points != 4
        perimeter = 4 * size
        step = perimeter / float(num_points)
        points = []

        for i in range(num_points):
            dist = i * step
            if dist < size:
                x = x_min + dist
                y = y_min
            elif dist < 2 * size:
                x = x_max
                y = y_min + (dist - size)
            elif dist < 3 * size:
                x = x_max - (dist - 2 * size)
                y = y_max
            else:
                x = x_min
                y = y_max - (dist - 3 * size)

            points.append((int(x), int(y)))

        return points


    def generate_qte_positions(
        layout_type: str,
        num_points: int,
        pattern_params: Dict[str, Any],
        screen_width: int = 1920,
        screen_height: int = 1080,
        randomize_shape: bool = True
    ) -> List[Tuple[int, int]]:
        """
        Dispatches QTE position calculation based on weapon layout type.
        """
        center_x = pattern_params.get("center_x", screen_width // 2)
        center_y = pattern_params.get("center_y", screen_height // 2)

        if layout_type == "ARC":
            length = pattern_params.get("length", 600)
            curvature = pattern_params.get("curvature", 0.4)
            return generate_knife_arc(center_x, center_y, length, curvature, num_points, randomize_shape=randomize_shape)

        elif layout_type == "SQUARE":
            size = pattern_params.get("size", 350)
            return generate_hammer_square(center_x, center_y, size, num_points, randomize_shape=randomize_shape)

        else:
            # Fallback random scatter
            points = []
            margin = 200
            for _ in range(num_points):
                rx = random.randint(margin, screen_width - margin)
                ry = random.randint(margin, screen_height - margin)
                points.append((rx, ry))
            return points
