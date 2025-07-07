
from PIL import Image, ImageDraw, ImageFont
import os
import math

# === Text Style and Animation ===
def apply_fancy_text_style(draw, position, text, font, style="rainbow", frame=0, color="white"):
    x, y = position
    if style == "rainbow":
        colors = [
            (255, 0, 0), (255, 165, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)
        ]
        for i, char in enumerate(text):
            color_cycle = colors[(i + frame) % len(colors)]
            draw.text((x, y), char, font=font, fill=color_cycle)
            x += font.getbbox(char)[2] - font.getbbox(char)[0]
    elif style == "wave":
        for i, char in enumerate(text):
            y_offset = int(5 * math.sin((frame + i) * 0.5))
            draw.text((x, y + y_offset), char, font=font, fill=color)
            x += font.getbbox(char)[2] - font.getbbox(char)[0]
    elif style == "fade":
        alpha = int(255 * (0.5 + 0.5 * math.sin(frame * 0.3)))
        draw.text((x, y), text, font=font, fill=color)
    elif style == "slide-left":
        offset = int(5 * math.sin(frame * 0.3))
        draw.text((x - offset, y), text, font=font, fill=color)
    elif style == "slide-right":
        offset = int(5 * math.sin(frame * 0.3))
        draw.text((x + offset, y), text, font=font, fill=color)
    elif style == "zoom":
        scale = 1 + 0.05 * math.sin(frame * 0.3)
        font_size = int(font.size * scale)
        try:
            zoom_font = ImageFont.truetype("arial.ttf", font_size)
        except:
            zoom_font = font
        draw.text((x, y), text, font=zoom_font, fill=color)
    elif style == "rotate":
        draw.text((x, y), text[::-1] if frame % 2 == 0 else text, font=font, fill=color)
    elif style == "flip":
        draw.text((x, y), text.upper() if frame % 2 == 0 else text.lower(), font=font, fill=color)
    elif style == "pulse":
        brightness = int(128 + 127 * math.sin(frame * 0.3))
        draw.text((x, y), text, font=font, fill=(brightness, brightness, brightness))
    elif style == "shake":
        offset_x = int(3 * math.sin(frame * 2))
        offset_y = int(3 * math.cos(frame * 2))
        draw.text((x + offset_x, y + offset_y), text, font=font, fill=color)
    else:
        draw.text((x, y), text, font=font, fill=color)

# # === Get Position from Keyword or Coordinates ===
def get_position_from_input(position_input, image_size, text_size):
    keywords = {
        "top-left": (20, 20),
        "top-center": ((image_size[0] - text_size[0]) // 2, 20),
        "top-right": (image_size[0] - text_size[0] - 20, 20),
        "center": ((image_size[0] - text_size[0]) // 2, (image_size[1] - text_size[1]) // 2),
        "bottom-left": (20, image_size[1] - text_size[1] - 20),
        "bottom-center": ((image_size[0] - text_size[0]) // 2, image_size[1] - text_size[1] - 20),
        "bottom-right": (image_size[0] - text_size[0] - 20, image_size[1] - text_size[1] - 20)
    }

    if "," in position_input:
        try:
            x, y = map(int, position_input.split(","))
            return (x, y)
        except:
            return (50, 50)
    return keywords.get(position_input.lower(), (50, 50))



# === Create GIF Animation ===
def add_animated_text_box(image_path, output_path, text, font_size=40, position_input="50,50", style="rainbow", font_path="C:/Users/PC-16/Desktop/reel_invitation_creator/assets/fonts/ariali.ttf", animation="color-cycle", text_color="white"):
    if not os.path.exists(image_path):
        print("Image not found.")
        return

    base_image = Image.open(image_path).convert("RGB")
    frames = []
    total_frames = 15

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    try:
        text_width = int(font.getlength(text))
    except:
        text_width = sum(font.getsize(c)[0] for c in text)

    try:
        bbox = font.getbbox(text)
        text_height = bbox[3] - bbox[1]
    except:
        text_height = font.size
    image_size = base_image.size

    for i in range(total_frames):
        frame = base_image.copy()
        draw = ImageDraw.Draw(frame)

        pos = get_position_from_input(position_input, image_size, (text_width, text_height))

        apply_fancy_text_style(draw, pos, text, font, style=animation, frame=i, color=text_color)
        frames.append(frame)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)
    print(f"[✓] Animated GIF saved at: {output_path}")
    return output_path



# === Example usage ===
if __name__ == "__main__":
    image_path = input("Enter path to image: ").strip()
    text = input("Enter text to add: ").strip()
    font_size = int(input("Enter font size (e.g., 40): ") or "40")
    position_input = input("Enter position (x,y or keyword like 'top-center'): ").strip()
    print("Available animations: color-cycle, bounce, wave, fade, slide-left, slide-right, zoom, rotate, flip, pulse, shake")
    animation = input("Enter animation type: ").strip() or "color-cycle"
    text_color_input = input("Enter text color (name or RGB like 255,0,0): ").strip()

    if "," in text_color_input:
        try:
            text_color = tuple(map(int, text_color_input.split(",")))
        except:
            text_color = "white"
    else:
        text_color = text_color_input or "white"

    output_path = "animated_text.gif"
    add_animated_text_box(image_path, output_path, text, font_size, position_input, animation, animation=animation, text_color=text_color)


