#main
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter,ImageOps
from diffusers import StableDiffusionPipeline
import torch
import face_recognition
import math
import numpy as np
from rj import apply_fancy_text_style,get_position_from_input,add_animated_text_box
from effect import apply_drop_shadow, apply_glow, apply_outline, apply_duotone
CHERRY_FUCHSIA = (222, 49, 99)

# === Paths ===
os.makedirs("templates", exist_ok=True)
os.makedirs("output", exist_ok=True)

# === Predefined layout (overrideable) ===

PREDEFINED_LAYOUTS = {
    "templates/template1.jpg": {
        "text_pos": "auto",  # or a specific coordinate like (50, 50)
        "photo_pos": "auto"
    }
}
def generate_image_from_prompt(prompt):
    import replicate
    import requests
    import os
    import tempfile

    REPLICATE_API_TOKEN = "YOUR_REPLICATE_API_TOKEN"

    replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

    output = replicate_client.run(
        "stability-ai/stable-diffusion:db21e45d35c3c47d7864f6e9b7e7aa70e42d3b61e2cc65382b0de1e9651e135b",
        input={"prompt": prompt}
    )

    image_url = output
    response = requests.get(image_url)

    output_path = os.path.join(tempfile.gettempdir(), f"ai_generated_{abs(hash(prompt))}.png")
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

# === Fancy Text Effects ===
def create_gradient_color(start_color, end_color, steps, current_step):
    """Create gradient color between two colors"""
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    
    ratio = current_step / max(steps - 1, 1)
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    
    return (r, g, b)

def draw_rainbow_text(draw, position, text, font, rainbow_colors=None):
    """Draw text with rainbow gradient effect"""
    if rainbow_colors is None:
        rainbow_colors = [
            (255, 0, 0),    # Red
            (255, 165, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (75, 0, 130),   # Indigo
            (238, 130, 238) # Violet
        ]
    
    x, y = position
    char_x = x
    
    for i, char in enumerate(text):
        if char == ' ':
            char_width = font.getbbox(' ')[2] - font.getbbox(' ')[0]
            char_x += char_width
            continue
            
        # Get color for this character
        color_index = (i * len(rainbow_colors)) // len(text)
        color_index = min(color_index, len(rainbow_colors) - 1)
        color = rainbow_colors[color_index]
        
        # Draw character
        draw.text((char_x, y), char, font=font, fill=color)
        
        # Move to next character position
        char_width = font.getbbox(char)[2] - font.getbbox(char)[0]
        char_x += char_width

def draw_glowing_text(draw, position, text, font, glow_color=(255, 255, 0), text_color=(255, 255, 255), glow_radius=3):
    """Draw text with glowing effect"""
    x, y = position
    
    # Draw glow effect (multiple layers)
    for radius in range(glow_radius, 0, -1):
        alpha = int(255 * (1 - radius / (glow_radius + 1)))
        glow_with_alpha = glow_color + (alpha,)
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    draw.text((x + dx, y + dy), text, font=font, fill=glow_color)
    
    # Draw main text
    draw.text((x, y), text, font=font, fill=text_color)

def draw_3d_text(draw, position, text, font, shadow_color=(100, 100, 100), text_color=(255, 255, 255), depth=3):
    """Draw text with 3D shadow effect"""
    x, y = position
    
    # Draw shadow layers for 3D effect
    for i in range(depth, 0, -1):
        shadow_alpha = int(150 - (i * 30))
        shadow_alpha = max(shadow_alpha, 50)
        current_shadow = tuple(list(shadow_color) + [shadow_alpha]) if len(shadow_color) == 3 else shadow_color
        draw.text((x + i, y + i), text, font=font, fill=shadow_color)
    
    # Draw main text
    draw.text((x, y), text, font=font, fill=text_color)

def draw_outlined_text(draw, position, text, font, outline_color=(0, 0, 0), text_color=(255, 255, 255), outline_width=2):
    """Draw text with outline"""
    x, y = position
    
    # Draw outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    
    # Draw main text
    draw.text((x, y), text, font=font, fill=text_color)

def draw_gradient_text(draw, position, text, font, start_color=(255, 0, 128), end_color=(0, 255, 255)):
    """Draw text with gradient effect"""
    x, y = position
    text_width = font.getbbox(text)[2] - font.getbbox(text)[0]
    
    # Create a temporary image for gradient
    temp_img = Image.new('RGBA', (text_width + 20, 100), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Draw each character with gradient color
    char_x = 0
    for i, char in enumerate(text):
        if char == ' ':
            char_width = font.getbbox(' ')[2] - font.getbbox(' ')[0]
            char_x += char_width
            continue
        
        # Calculate gradient color for this character
        progress = i / max(len(text) - 1, 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)
        
        temp_draw.text((char_x, 10), char, font=font, fill=(r, g, b, 255))
        char_width = font.getbbox(char)[2] - font.getbbox(char)[0]
        char_x += char_width
    
    # Paste the gradient text onto main image
    if hasattr(draw, '_image'):
        draw._image.paste(temp_img, (x, y), temp_img)

def apply_fancy_text_style(draw, position, text, font, style="rainbow"):
    """Apply different fancy text styles"""
    styles = {
        "rainbow": lambda: draw_rainbow_text(draw, position, text, font),
        "glow": lambda: draw_glowing_text(draw, position, text, font, 
                                        glow_color=(255, 215, 0), text_color=(255, 255, 255)),
        "3d": lambda: draw_3d_text(draw, position, text, font, 
                                 shadow_color=(128, 0, 128), text_color=(255, 255, 255)),
        "outline": lambda: draw_outlined_text(draw, position, text, font, 
                                            outline_color=(0, 0, 0), text_color=(255, 215, 0)),
        "gradient": lambda: draw_gradient_text(draw, position, text, font, 
                                             start_color=(255, 0, 128), end_color=(0, 255, 255)),
        "fire": lambda: draw_gradient_text(draw, position, text, font, 
                                         start_color=(255, 0, 0), end_color=(255, 255, 0)),
        "ocean": lambda: draw_gradient_text(draw, position, text, font, 
                                          start_color=(0, 100, 255), end_color=(0, 255, 200)),
        "sunset": lambda: draw_gradient_text(draw, position, text, font, 
                                           start_color=(255, 94, 77), end_color=(255, 206, 84))
    }
    
    if style in styles:
        styles[style]()
    else:
        # Default to rainbow if style not found
        draw_rainbow_text(draw, position, text, font)

# === AI Template Generator ===
def generate_ai_template(prompt: str, output_path: str):
    print("[*] Generating AI template...")
    try:
        model_id = "runwayml/stable-diffusion-v1-5"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = StableDiffusionPipeline.from_pretrained(model_id)
        pipe = pipe.to(device)
        
        # Enhanced prompt for better birthday themes
        enhanced_prompt = f"{prompt}"
        
        image = pipe(enhanced_prompt).images[0]
        image = image.resize((800, 800), Image.Resampling.LANCZOS)
        image.save(output_path)
        print(f"[+] AI-generated template saved at {output_path}")
        return output_path
    except Exception as e:
        print(f"[!] AI generation failed: {e}")
        # Create a colorful fallback template
        fallback_img = Image.new('RGB', (800, 800), color='navy')
        draw = ImageDraw.Draw(fallback_img)
        
        # Add some colorful shapes for visual appeal
        for i in range(20):
            x = (i * 40) % 800
            y = (i * 30) % 800
            color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)][i % 5]
            draw.ellipse([x, y, x+60, y+60], fill=color + (50,))
        
        fallback_img.save(output_path)
        return output_path

# === Face Detection ===
def detect_face_regions(image_path):
    try:
        img = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(img)
        return face_locations
    except:
        return []

# === Utility for Bounding Boxes ===
def boxes_overlap(box1, box2):
    x1, y1, x2, y2 = box1
    a1, b1, a2, b2 = box2
    return not (x2 < a1 or x1 > a2 or y2 < b1 or y1 > b2)

# === Text Utilities ===
def get_text_box_position(x, y, text_lines, font):
    width = 0
    bbox = font.getbbox("Ay")
    line_height = (bbox[3] - bbox[1]) + 15  # Increased spacing for fancy text
    for line in text_lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        if w > width:
            width = w
    height = line_height * len(text_lines)
    return (x, y, x + width, y + height)

# === Position Finding ===
def choose_safe_corner(image_size, face_locations, avoid_boxes=[]):
    width, height = image_size
    corners = {
        "top-left": (20, 20),
        "top-right": (width - 170, 20),
        "bottom-left": (20, height - 170),
        "bottom-right": (width - 170, height - 170),
    }

    for name, (x, y) in corners.items():
        new_box = (x, y, x + 150, y + 150)
        is_safe = True
        for (top, right, bottom, left) in face_locations:
            if not (new_box[2] < left or new_box[0] > right or new_box[3] < top or new_box[1] > bottom):
                is_safe = False
                break
        for abox in avoid_boxes:
            if boxes_overlap(new_box, abox):
                is_safe = False
                break
        if is_safe:
            return x, y
    return corners["bottom-right"]

def choose_safe_text_position(image_size, face_locations, avoid_boxes=[]):
    width, height = image_size
    text_boxes = {
        "top-center": (width // 2 - 250, 30),
        "top-left": (30, 30),
        "top-right": (width - 520, 30),
        "center-left": (30, height // 2 - 100),
        "center-right": (width - 520, height // 2 - 100),
        "bottom-left": (30, height - 200),
        "bottom-center": (width // 2 - 250, height - 200),
        "bottom-right": (width - 520, height - 200),
    }

    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    text_lines = ["🎉 Happy Birthday!", "📅 Date"]
    
    # Prioritize center positions for better visibility
    priority_order = ["top-center", "bottom-center", "center-left", "center-right", 
                     "top-left", "top-right", "bottom-left", "bottom-right"]
    
    for position_name in priority_order:
        if position_name in text_boxes:
            x, y = text_boxes[position_name]
            box = get_text_box_position(x, y, text_lines, font)
            is_safe = True
            
            # Check against faces
            for (top, right, bottom, left) in face_locations:
                if not (box[2] < left or box[0] > right or box[3] < top or box[1] > bottom):
                    is_safe = False
                    break
            
            # Check against other avoid boxes
            if is_safe:
                for abox in avoid_boxes:
                    if boxes_overlap(box, abox):
                        is_safe = False
                        break
            
            if is_safe:
                return x, y
    
    return 30, 30  # Fallback position

def add_text_to_image(image, name, date, position_keyword_or_auto, avoid_boxes=[], text_style="rainbow"):
    """Add fancy colorful text to image"""
    draw = ImageDraw.Draw(image)

    # Start with larger font for better visual impact
    font_size = 80
    max_width = int(image.width * 0.85)  # Allow more width for fancy text
    
    # Create text lines with emojis and styling
    text_lines = [
        f"🎉 Happy Birthday {name}! 🎂",
        f"📅 {date} 🎈"
    ]

    # Adjust font size to fit
    while font_size > 20:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", font_size)  # Try different case
            except:
                font = ImageFont.load_default()
                break

        max_line_width = max([font.getbbox(line)[2] - font.getbbox(line)[0] for line in text_lines])
        if max_line_width <= max_width:
            break
        font_size -= 3

    # Get face locations for avoidance
    face_locations = []
    if hasattr(image, 'filename'):
        face_locations = detect_face_regions(image.filename)
        for (top, right, bottom, left) in face_locations:
            avoid_boxes.append((left, top, right, bottom))

    # Determine text position
    # Determine text position
    if position_keyword_or_auto == "auto":
        x, y = choose_safe_text_position((image.width, image.height), face_locations, avoid_boxes)
    elif isinstance(position_keyword_or_auto, str):
        temp_img = Image.new('RGBA', (100, 100))  # Dummy overlay size for mapping
        x, y = get_position_from_keyword(image, temp_img, position_keyword_or_auto)
    else:
        x, y = position_keyword_or_auto


    # Draw each line with fancy styling
    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1] + 20
    
    for i, line in enumerate(text_lines):
        current_y = y + (i * line_height)
        
        # Choose different styles for different lines
        if i == 0:  # Happy Birthday line
            if text_style == "mixed":
                apply_fancy_text_style(draw, (x, current_y), line, font, "rainbow")
            else:
                apply_fancy_text_style(draw, (x, current_y), line, font, text_style)
        else:  # Date line
            if text_style == "mixed":
                apply_fancy_text_style(draw, (x, current_y), line, font, "gradient")
            else:
                # Use a complementary style for date
                date_style = "gradient" if text_style == "rainbow" else text_style
                apply_fancy_text_style(draw, (x, current_y), line, font, date_style)

    # Calculate text bounding box
    text_box = get_text_box_position(x, y, text_lines, font)
    return image, text_box

def add_personal_photo(background, personal_photo_path, position_keyword_or_auto, avoid_boxes=[], new_size=(200, 200)):
    """Add personal photo with rounded corners and border"""
    try:
        personal = Image.open(personal_photo_path).convert("RGBA")
        
        # Resize maintaining aspect ratio
        personal = personal.resize(new_size, Image.Resampling.LANCZOS)

        
        # Create rounded corners
        mask = Image.new('L', personal.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, personal.width, personal.height], 
                                  radius=20, fill=255)
        
        # Apply mask for rounded corners
        rounded_personal = Image.new('RGBA', personal.size, (255, 255, 255, 0))
        rounded_personal.paste(personal, (0, 0))
        rounded_personal.putalpha(mask)
        
        # Add colorful border
        border_img = Image.new('RGBA', (personal.width + 10, personal.height + 10), (255, 215, 0, 255))
        border_mask = Image.new('L', border_img.size, 0)
        border_draw = ImageDraw.Draw(border_mask)
        border_draw.rounded_rectangle([0, 0, border_img.width, border_img.height], 
                                    radius=25, fill=255)
        border_img.putalpha(border_mask)
        
        # Combine border and photo
        final_photo = Image.new('RGBA', border_img.size, (255, 255, 255, 0))
        final_photo.paste(border_img, (0, 0), border_img)
        final_photo.paste(rounded_personal, (5, 5), rounded_personal)
        
        # Determine position
        if position_keyword_or_auto == "auto":
            face_locations = []
            if hasattr(background, 'filename'):
                face_locations = detect_face_regions(background.filename)
            x, y = choose_safe_corner((background.width, background.height), face_locations, avoid_boxes)
        else:
            temp_img = Image.new('RGBA', (final_photo.width, final_photo.height))
            x, y = get_position_from_keyword(background, temp_img, position_keyword_or_auto)
        
        # Paste photo onto background
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        
        background.paste(final_photo, (x, y), final_photo)
        return background, (x, y, x + final_photo.width, y + final_photo.height)
        
    except Exception as e:
        print(f"[!] Error adding personal photo: {e}")
        # Return original background with dummy box
        return background, (0, 0, 150, 150)

def get_position_from_keyword(background, overlay, position_keyword):
    bw, bh = background.width, background.height
    ow, oh = overlay.width, overlay.height

    position_map = {
        "top-left": (20, 20),
        "top-center": ((bw - ow) // 2, 20),
        "top-right": (bw - ow - 20, 20),

        "center-left": (20, (bh - oh) // 2),
        "center": ((bw - ow) // 2, (bh - oh) // 2),
        "center-right": (bw - ow - 20, (bh - oh) // 2),

        "bottom-left": (20, bh - oh - 20),
        "bottom-center": ((bw - ow) // 2, bh - oh - 20),
        "bottom-right": (bw - ow - 20, bh - oh - 20)
    }

    if isinstance(position_keyword, tuple):
        return position_keyword
    return position_map.get(position_keyword, (50, 50))  # default fallback

# === Main Generation ===
def generate_birthday_image(name, date, template_type, personal_photo_path, prompt=None, text_style="rainbow"):
    """Generate birthday image with fancy colorful text"""
    
    if template_type == "p":
        template_path = "templates/template1.jpg"
        if not os.path.exists(template_path):
            print("[*] Creating default colorful template...")
            # Create a vibrant default template
            default_template = Image.new('RGB', (800, 800), color=(30, 30, 60))
            draw = ImageDraw.Draw(default_template)
            
            # Add colorful background pattern
            colors = [(255, 100, 150), (100, 255, 150), (150, 100, 255), (255, 255, 100)]
            for i in range(0, 800, 100):
                for j in range(0, 800, 100):
                    color = colors[(i//100 + j//100) % len(colors)]
                    draw.rectangle([i, j, i+50, j+50], fill=color + (50,))
            
            default_template.save(template_path)
            
        layout = PREDEFINED_LAYOUTS.get(template_path, {
            "text_pos": "auto",
            "photo_pos": "auto"
        })

    elif template_type == "ai":
        if not prompt:
            raise ValueError("Prompt required for AI image generation.")
        template_path = "templates/ai_generated.jpg"
        generate_ai_template(prompt, template_path)
        layout = {
            "text_pos": "auto",
            "photo_pos": "auto"
        }
    else:
        raise ValueError("Invalid template type!")

    # Load and prepare background
    bg = Image.open(template_path).convert("RGB")
    bg.filename = template_path  # for face_recognition
    
    # Ensure good resolution
    if bg.width < 600 or bg.height < 600:
        bg = bg.resize((800, 800), Image.Resampling.LANCZOS)

    # Step 1: Detect all faces in the background image
    face_locations = detect_face_regions(bg.filename)
    avoid_boxes = []
    for (top, right, bottom, left) in face_locations:
        avoid_boxes.append((left, top, right, bottom))

    # Step 2: Add personal photo, avoiding faces
    bg, personal_box = add_personal_photo(bg, personal_photo_path, layout["photo_pos"], avoid_boxes=avoid_boxes, new_size=(200, 200))

    avoid_boxes.append(personal_box)

    # Step 3: Add fancy text, avoiding faces + personal image
    bg, text_box = add_text_to_image(bg, name, date, layout["text_pos"], avoid_boxes=avoid_boxes, text_style=text_style)

    # Convert back to RGB for saving
    if bg.mode == 'RGBA':
        rgb_bg = Image.new('RGB', bg.size, (255, 255, 255))
        rgb_bg.paste(bg, mask=bg.split()[-1] if bg.mode == 'RGBA' else None)
        bg = rgb_bg

    output_path = f"output/{name.replace(' ', '_')}_birthday_fancy.jpg"
    bg.save(output_path, quality=95)
    print(f"[✓] Fancy birthday image saved to: {output_path}")
    return output_path
    
# === Image Re-Editing ===
def edit_generated_image(name, date, template_path, personal_photo_path, text_pos="auto", photo_pos="auto", new_size=(150, 150), text_style="rainbow"):
    """Edit generated image with fancy text styling"""
    bg = Image.open(template_path).convert("RGB")
    bg.filename = template_path
    
    # Ensure good resolution
    if bg.width < 600 or bg.height < 600:
        bg = bg.resize((800, 800), Image.Resampling.LANCZOS)

    # Add personal photo with new settings
    bg, personal_box = add_personal_photo(bg, personal_photo_path, photo_pos, avoid_boxes=[], new_size=new_size)


    # Re-add fancy text avoiding new personal image
    bg, text_box = add_text_to_image(bg, name, date, text_pos, avoid_boxes=[personal_box], text_style=text_style)

    # Convert to RGB for saving
    if bg.mode == 'RGBA':
        rgb_bg = Image.new('RGB', bg.size, (255, 255, 255))
        rgb_bg.paste(bg, mask=bg.split()[-1] if bg.mode == 'RGBA' else None)
        bg = rgb_bg

    edited_path = f"output/{name.replace(' ', '_')}_birthday_edited_fancy.jpg"
    bg.save(edited_path, quality=95)
    print(f"[✓] Fancy edited birthday image saved to: {edited_path}")
    return edited_path


def apply_effects(input_path, shadow_effect, duotone_effect):
    image = Image.open(input_path).convert('RGBA')

    # ---------- Apply Shadow ----------
    if shadow_effect == 'drop_shadow':
        image = apply_drop_shadow(image)
    elif shadow_effect == 'glow':
        image = apply_glow(image)
    elif shadow_effect == 'outline':
        image = apply_outline(image)
    elif shadow_effect.lower() == 'none':
        pass  # No shadow applied

    # ---------- Apply Duotone ----------
    if duotone_effect == 'cherry_fuchsia':
        image = apply_duotone(
            image,
            shadow_color=CHERRY_FUCHSIA,
            highlight_color=(255, 255, 255)
        )
    elif duotone_effect == 'grayscale':
        image = image.convert('L').convert('RGBA')
    elif duotone_effect.lower() == 'none':
        pass  # No duotone applied

    # ---------- Save Output ----------
    output_path = os.path.join(
    "outputs", f"effect_{os.path.splitext(os.path.basename(input_path))[0]}.png"
    )

    os.makedirs("outputs", exist_ok=True)
    image.save(output_path)

    return output_path
# === CLI ===
if __name__ == "__main__":
    print("🎨 === Fancy Colorful Birthday Generator === 🎨\n")
    
    name = input("Enter birthday person's name: ").strip()
    if not name:
        name = "Friend"
        
    date = input("Enter birthday date (e.g. June 10, 2025): ").strip()
    if not date:
        date = "Today"
        
    template_type = input("Template type - Predefined or AI? (p/ai): ").strip().lower()
    
    if template_type not in ["p", "ai"]:
        print("❌ Please enter 'p' for Predefined or 'ai' for AI template.")
        exit(1)

    personal_photo_path = input("Enter path to personal image: ").strip()
    
    if not os.path.exists(personal_photo_path):
        print(f"❌ Personal photo not found at: {personal_photo_path}")
        exit(1)

    # Choose text style
    print("\n🎨 Choose text style:")
    print("  1. rainbow - Colorful rainbow text")
    print("  2. glow - Golden glowing text")
    print("  3. 3d - 3D shadow effect")
    print("  4. gradient - Gradient colors")
    print("  5. fire - Fire gradient (red to yellow)")
    print("  6. ocean - Ocean gradient (blue to cyan)")
    print("  7. sunset - Sunset gradient (orange to yellow)")
    print("  8. mixed - Different styles for each line")
    
    style_choice = input("Enter style number (1-8) or name [default: rainbow]: ").strip().lower()
    
    style_map = {
        "1": "rainbow", "rainbow": "rainbow",
        "2": "glow", "glow": "glow",
        "3": "3d", "3d": "3d",
        "4": "gradient", "gradient": "gradient",
        "5": "fire", "fire": "fire",
        "6": "ocean", "ocean": "ocean",
        "7": "sunset", "sunset": "sunset",
        "8": "mixed", "mixed": "mixed"
    }
    
    text_style = style_map.get(style_choice, "rainbow")

    try:
        if template_type == "ai":
            prompt = input("Enter prompt for AI background (e.g., balloons, cake, colorful confetti): ").strip()
            if not prompt:
                prompt = "birthday party, balloons, cake, colorful decorations"
                
            output_path = generate_birthday_image(name, date, template_type, personal_photo_path, prompt, text_style)
            template_path = "templates/ai_generated.jpg"
        else:
            output_path = generate_birthday_image(name, date, template_type, personal_photo_path, text_style=text_style)
            template_path = "templates/template1.jpg"

        print(f"\n✅ Fancy birthday image generated successfully!")
        print(f"🎨 Style used: {text_style}")
        print(f"📁 Saved at: {output_path}")

        #Ask for editing
        edit_choice = input("\nDo you want to edit the image? (y/n): ").strip().lower()
        if edit_choice == "y":
            print("\n📍 Position options:")
            print("  top-left, top-center, top-right")
            print("  center-left, center, center-right")
            print("  bottom-left, bottom-center, bottom-right")
            print("  Or type coordinates like '250,300'")

            pos_input = input("Enter new position for the personal image: ").strip().lower()

            if "," in pos_input:
                try:
                    x, y = map(int, pos_input.split(","))
                    new_photo_pos = (max(0, x), max(0, y))
                except:
                    print("❌ Invalid coordinates. Using default 'bottom-right'.")
                    new_photo_pos = "bottom-right"
            elif pos_input in [
                "top-left", "top-center", "top-right",
                "center-left", "center", "center-right",
                "bottom-left", "bottom-center", "bottom-right"
            ]:
                new_photo_pos = pos_input
            else:
                print("❌ Invalid position keyword. Using default 'bottom-right'.")
                new_photo_pos = "top-left"

            size_input = input("Enter new size for the personal image (width,height): ")
                               
            if "," in size_input:
                try:
                    new_size = tuple(map(int, size_input.split(",")))
                    new_size = (max(50, new_size[0]), max(50, new_size[1]))  # Ensure minimum size
                except:
                    print("❌ Invalid size. Using default (150, 150).")
                    new_size = (200, 200)
            else:
                new_size = (200, 200)
            text_pos = input("Enter new text position (auto or keyword): ").strip().lower()
            if text_pos not in ["auto", "top-left", "top-center", "top-right",
                                "center-left", "center", "center-right",
                                "bottom-left", "bottom-center", "bottom-right"]:
                text_pos = "auto"         
            edited_path = edit_generated_image(name, date, template_path, personal_photo_path, 
                                               text_pos=text_pos, photo_pos=new_photo_pos, 
                                               new_size=new_size, text_style=text_style)
            print(f"✅ Edited image saved at: {edited_path}")
    except Exception as e:  
        print(f"❌ Error generating image: {e}")
        exit(1)
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user.")
        exit(0)
        
    image = Image.open(edited_path).convert('RGBA')

    print("Available shadow effects: drop_shadow, glow, outline")
    shadow_effect = input("Enter shadow effect to apply: ").strip().lower()

    if shadow_effect == 'drop_shadow':
        image = apply_drop_shadow(image)
    elif shadow_effect == 'glow':
        image = apply_glow(image)
    elif shadow_effect == 'outline':
        image = apply_outline(image)
    else:
        print("Invalid shadow effect entered. No shadow effect will be applied.")

    print("Available duotone effects: cherry_fuchsia, grayscale, none")
    duotone_effect = input("Enter duotone effect to apply: ").strip().lower()

    if duotone_effect == 'cherry_fuchsia':
        image = apply_duotone(image, shadow_color=CHERRY_FUCHSIA, highlight_color=(255,255,255))
    elif duotone_effect == 'grayscale':
        image = image.convert('L').convert('RGBA')
    elif duotone_effect == 'none':
        pass
    else:
        print("Invalid duotone effect entered. No duotone effect will be applied.")

    output_path = 'final_output.png'
    image.save(output_path)
    print(f"Final image saved as {output_path}")        
    animate_choice = input("\nDo you want to add an animated text box? (y/n): ").strip().lower()
    if animate_choice == "y":
        text = input("Enter text to add: ").strip()
        font_size = int(input("Enter font size (e.g., 40): ") or "50")
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
        add_animated_text_box(edited_path, output_path, text, font_size, position_input, animation, animation=animation, text_color=text_color)


    
        
