import argparse
from colormath.color_objects import sRGBColor, HSLColor
from colormath.color_conversions import convert_color
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from art import *

def hex_to_rgb(hex_color):
    """Convert HEX to RGB color."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB to HEX color."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def create_harmonized_colors(hex_color, num_variations):
    """Create harmonized colors based on various color theories."""
    base_rgb = sRGBColor(*hex_to_rgb(hex_color), is_upscaled=True)
    base_hsl = convert_color(base_rgb, HSLColor)

    harmonized_colors = {
        'Monochromatic': [],
        'Gradient Balance': []
    }
    fewer_variations = num_variations // 4  # Adjust this as needed
    # Generating colors for each scheme...
    for i in range(num_variations):
        # Monochromatic Scheme
        mono_hsl = HSLColor(base_hsl.hsl_h, base_hsl.hsl_s, 0.2 + 0.6 * i / (num_variations - 1))
        harmonized_colors['Monochromatic'].append(rgb_to_hex(convert_color(mono_hsl, sRGBColor).get_upscaled_value_tuple()))

       # Constant Lightness and Saturation Scheme
        harmonized_colors['Gradient Balance'] = []
        hue_step = 360 / num_variations  # To evenly distribute hues across the color wheel

        for i in range(num_variations):
            # Base color with constant lightness and saturation
            new_hue = (base_hsl.hsl_h + hue_step * i) % 360
            constant_ls_hsl = HSLColor(new_hue, base_hsl.hsl_s, base_hsl.hsl_l)
            harmonized_colors['Gradient Balance'].append(rgb_to_hex(convert_color(constant_ls_hsl, sRGBColor).get_upscaled_value_tuple()))

            # Monochromatic variation with adjusted lightness and saturation
            adjusted_lightness = max(min(base_hsl.hsl_l + 0.15, 1), 0)  # Ensuring within 0-1 range
            adjusted_saturation = max(min(base_hsl.hsl_s - 0.15, 1), 0)  # Ensuring within 0-1 range
            mono_variant_hsl = HSLColor(new_hue, adjusted_saturation, adjusted_lightness)
            harmonized_colors['Gradient Balance'].append(rgb_to_hex(convert_color(mono_variant_hsl, sRGBColor).get_upscaled_value_tuple()))

    return harmonized_colors

def display_color_schemes(harmonized_colors, base_color):
    """Display the harmonized color schemes."""
    scheme_descriptions = {
        'Monochromatic': 'Ideal for charts with a single metric.',
        'Gradient Balance': 'Gradient balance contrasting colors, idea for gradient balance.'
    }

    # Setting a larger width for the figure (e.g., 15 inches wide and height depending on the number of schemes)
    """Display the harmonized color schemes."""
    fig_width = 15  # Width in inches
    fig_height = 2 * len(harmonized_colors)  # Height in inches, adjust as needed
    fig, axes = plt.subplots(len(harmonized_colors), 1, figsize=(fig_width, fig_height))

    fig.suptitle("TAPTOK Color Harmonizer", fontsize=16, fontweight='bold')


    for ax, (scheme, colors) in zip(axes, harmonized_colors.items()):
        ax.set_title(f"{scheme} Scheme - {scheme_descriptions[scheme]}", fontsize=10, pad=20)
        ax.text(0.5, 1.05, f"Base Color: {base_color}", transform=ax.transAxes, ha="center", fontsize=8)
        for i, color in enumerate(colors):
            rect = patches.Rectangle((i, 0), 1, 1, linewidth=1, edgecolor='none', facecolor=color)
            ax.add_patch(rect)
            ax.text(i + 0.5, -0.5, color, ha='center', va='center', fontsize=8)
        ax.set_xlim(0, len(colors))
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')

    mng = plt.get_current_fig_manager()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def console_intro():
    """Display an ASCII art intro in the console."""
    tprint("TAPTOK", font="small")
    print("Color Harmonizer v1.0 by Jaime Manteiga\nDec 3, 2023\n")

# Parse command line arguments for hex color and number of variations
parser = argparse.ArgumentParser(description="Generate harmonized color schemes from a given hex color.")
parser.add_argument("-c", "--color", type=str, required=True, help="Hex color (e.g., #32a852)")
parser.add_argument("-v", "--variations", type=int, default=4, help="Number of color variations (default: 4)")
args = parser.parse_args()

# Display console intro
console_intro()

# Generate harmonized colors and display color schemes
harmonized_colors = create_harmonized_colors(args.color, args.variations)
display_color_schemes(harmonized_colors, args.color)

# Print the harmonized colors
print("\nHarmonized Color Schemes Hex Codes:")
for scheme, colors in harmonized_colors.items():
    print(f"{scheme} Scheme Colors: {', '.join(colors)}")
