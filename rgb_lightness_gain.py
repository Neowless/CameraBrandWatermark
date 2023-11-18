import colorsys

def rgb_to_hsl(r, g, b):
    # Normalize RGB values to be in the range [0, 1]
    r /= 255.0
    g /= 255.0
    b /= 255.0

    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    # Scale HSL values to the usual ranges
    h *= 360.0
    l *= 100.0
    s *= 100.0

    return h, s, l

def hsl_to_rgb(h, s, l):
    # Scale HSL values to be in the range [0, 1]
    h /= 360.0
    l /= 100.0
    s /= 100.0

    # Convert HSL to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)

    # Scale RGB values to the usual range
    r *= 255.0
    g *= 255.0
    b *= 255.0

    return int(r), int(g), int(b)

def adjust_lightness(rgb, ratio):
    # Convert RGB to HSL
    h, s, l = rgb_to_hsl(*rgb)

    # Increase lightness by the specified ratio
    l = min(100, 100*ratio)

    # Convert back to RGB
    adjusted_rgb = hsl_to_rgb(h, s, l)

    return adjusted_rgb
