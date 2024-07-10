def interpolate_colors(color1, color2, num_values):
    return [(color1[0] + (color2[0] - color1[0]) * i / num_values,
             color1[1] + (color2[1] - color1[1]) * i / num_values,
             color1[2] + (color2[2] - color1[2]) * i / num_values)
            for i in range(num_values)]

def generate_rainbow_colors(num_values):
    rainbow_colors = [
        (255, 0, 0),   # Red
        (255, 165, 0), # Orange
        (255, 255, 0), # Yellow
        (0, 255, 0),   # Green
        (0, 100, 255), # Blue
        (75, 0, 130),  # Indigo
        (148, 0, 211)  # Violet
    ]

    rainbow_fade = [
        (255, 0, 0),   # Red
        (255, 165, 0), # Orange
        (255, 255, 0), # Yellow
        (0, 255, 0),   # Green
        (0, 100, 255), # Blue
        (75, 0, 130),  # Indigo
        (148, 0, 211),  # Violet
        (75, 0, 130),  # Indigo
        (0, 100, 255), # Blue
        (0, 255, 0),   # Green
        (255, 255, 0), # Yellow
        (255, 165, 0), # Orange
        (255, 0, 0)   # Red
    ]
    
    all_colors = []
    for i in range(len(rainbow_fade) - 1):
        interpolated_colors = interpolate_colors(rainbow_fade[i], rainbow_fade[i + 1], num_values)
        all_colors.extend(interpolated_colors)
    
    return all_colors