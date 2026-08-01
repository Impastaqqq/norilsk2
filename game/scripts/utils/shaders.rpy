# shaders.rpy

init python:
    # 1D border fade shader
    # u_fade_size can be passed in pixels (e.g., 20.0 for 20px) or normalized fraction (e.g. 0.15 for 15%)
    # fragment_500 runs AFTER Ren'Py's texture sampler (renpy.texture at 200/300) computes gl_FragColor.
    renpy.register_shader("fade_borders", variables="""
        uniform float u_fade_size;
        uniform vec2 u_model_size;
        attribute vec4 a_position;
        varying vec2 v_pos;
    """, vertex_200="""
        v_pos = a_position.xy;
    """, fragment_500="""
        float px_fade = (u_fade_size <= 1.0) ? (u_fade_size * min(u_model_size.x, u_model_size.y)) : u_fade_size;
        
        vec2 edge_dist = min(v_pos, u_model_size - v_pos);
        float alpha_factor = smoothstep(0.0, px_fade, edge_dist.x) * smoothstep(0.0, px_fade, edge_dist.y);
        
        gl_FragColor *= alpha_factor;
    """)

    # 2D border fade shader (separate X and Y fade sizes)
    renpy.register_shader("fade_borders_xy", variables="""
        uniform vec2 u_fade_size;
        uniform vec2 u_model_size;
        attribute vec4 a_position;
        varying vec2 v_pos;
    """, vertex_200="""
        v_pos = a_position.xy;
    """, fragment_500="""
        float px_fade_x = (u_fade_size.x <= 1.0) ? (u_fade_size.x * u_model_size.x) : u_fade_size.x;
        float px_fade_y = (u_fade_size.y <= 1.0) ? (u_fade_size.y * u_model_size.y) : u_fade_size.y;
        
        vec2 edge_dist = min(v_pos, u_model_size - v_pos);
        float alpha_factor = smoothstep(0.0, px_fade_x, edge_dist.x) * smoothstep(0.0, px_fade_y, edge_dist.y);
        
        gl_FragColor *= alpha_factor;
    """)

    # Procedural Film Grain Noise Shader
    renpy.register_shader("film_grain", variables="""
        uniform float u_grain_strength;
        uniform float u_grain_speed;
        uniform float u_time;
        uniform vec2 u_model_size;
        attribute vec4 a_position;
        varying vec2 v_pos;
    """, vertex_200="""
        v_pos = a_position.xy;
    """, fragment_500="""
        vec2 uv = v_pos / u_model_size;
        vec2 seed = uv + vec2(sin(u_time * u_grain_speed), cos(u_time * u_grain_speed * 1.37));
        float noise = fract(sin(dot(seed, vec2(12.9898, 78.233))) * 43758.5453123);
        float grain = (noise - 0.5) * u_grain_strength;
        gl_FragColor.rgb += vec3(grain);
    """)


# ATL Transforms (mesh True is required for Ren'Py to generate a GL mesh for 2D images/displayables)
transform border_fade(fade_size=20.0):
    mesh True
    shader "fade_borders"
    u_fade_size fade_size

transform border_fade_xy(fade_x=20.0, fade_y=20.0):
    mesh True
    shader "fade_borders_xy"
    u_fade_size (fade_x, fade_y)

transform film_grain(strength=0.08, speed=15.0):
    mesh True
    shader "film_grain"
    u_grain_strength strength
    u_grain_speed speed

