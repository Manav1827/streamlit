from PIL import Image, ImageDraw, ImageFont

def generate_placeholder_image(text):
    img = Image.new('RGB', (600, 400), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0))
    return img
