from PIL import Image, ImageFilter, ImageOps
import numpy as np

CHERRY_FUCHSIA = (222, 49, 99)

def apply_drop_shadow(image, offset=(10, 10), shadow_color=CHERRY_FUCHSIA, background_color=(255,255,255), blur_radius=10):
    shadow = Image.new('RGBA', image.size, (0,0,0,0))
    alpha = image.split()[-1]
    shadow.paste(Image.new('RGBA', image.size, shadow_color + (255,)), mask=alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

    bg_size = (image.size[0] + abs(offset[0]), image.size[1] + abs(offset[1]))
    background = Image.new('RGBA', bg_size, background_color + (255,))
    background.paste(shadow, offset, shadow)
    background.paste(image, (0,0), image)
    return background

def apply_glow(image, glow_color=CHERRY_FUCHSIA, blur_radius=15):
    alpha = image.split()[-1]
    glow = Image.new('RGBA', image.size, glow_color + (0,))
    glow.paste(Image.new('RGBA', image.size, glow_color + (255,)), mask=alpha)
    for _ in range(2):
        glow = glow.filter(ImageFilter.GaussianBlur(blur_radius))
    out = Image.alpha_composite(glow, image)
    return out

def apply_outline(image, outline_color=CHERRY_FUCHSIA, outline_width=5):
    mask = image.split()[-1]
    outline = ImageOps.expand(mask, border=outline_width, fill=255)
    outline_img = Image.new('RGBA', outline.size, outline_color + (0,))
    outline_img.paste(Image.new('RGBA', outline.size, outline_color + (255,)), mask=outline)
    offset = (outline_width, outline_width)
    outline_img.paste(image, offset, image)
    return outline_img

def apply_duotone(image, shadow_color=CHERRY_FUCHSIA, highlight_color=(255,255,255)):
    gray = image.convert('L')
    arr = np.array(gray).astype(np.float32) / 255.0
    shadow = np.array(shadow_color, dtype=np.float32)
    highlight = np.array(highlight_color, dtype=np.float32)
    duotone_arr = (shadow[None,None,:] * (1 - arr[:,:,None]) +
                   highlight[None,None,:] * arr[:,:,None]).astype(np.uint8)
    duotone_img = Image.fromarray(duotone_arr, mode='RGB')
    return duotone_img

def main():
    photo_path = input("Enter photo path: ")
    image = Image.open(photo_path).convert('RGBA')

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

if __name__ == '__main__':
    main()
