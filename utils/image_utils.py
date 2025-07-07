from PIL import Image

def resize_image(image_path, output_size):
    img = Image.open(image_path)
    img = img.resize(output_size)
    img.save(image_path)
    return image_path
