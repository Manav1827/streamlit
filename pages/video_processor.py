import os
os.environ["IMAGEMAGICK_BINARY"] = "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"


# from moviepy.editor import *
# from PIL import Image, ImageDraw, ImageFont
# import os
# import torch
# from diffusers import StableDiffusionPipeline
# from math import ceil
# import json

# print(torch.cuda.is_available())

# device = "cuda" if torch.cuda.is_available() else "cpu"
# pipe = StableDiffusionPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device == "cuda" else torch.float32
# ).to(device)

# def generate_image_from_prompt(prompt, output_path="assets/generated_background.jpg"):
#     print(f"Generating AI image from prompt: {prompt}")
#     image = pipe(prompt).images[0]
#     os.makedirs("assets", exist_ok=True)
#     image = image.resize((1280, 720), Image.Resampling.LANCZOS)
#     image.save(output_path)
#     print(f"Generated image saved to: {output_path}")
#     return output_path

# def get_animation_clip(animation_type, duration, size=(1280, 720)):
#     anim_clip_path = {
#         "balloons": "assets/animations/balloons.mp4",
#         "confetti": "assets/animations/confetti.mp4"
#     }.get(animation_type)

#     if anim_clip_path and os.path.exists(anim_clip_path):
#         return VideoFileClip(anim_clip_path).resize(size).set_duration(duration).set_position("center").set_opacity(0.5)
#     return None

# def create_text_image(text, size=(1280, 720), font_size=60, bg_color=(0, 0, 0, 0), text_color='white'):
#     img = Image.new('RGBA', size, color=bg_color)
#     draw = ImageDraw.Draw(img)
#     try:
#         font = ImageFont.truetype("arial.ttf", font_size)
#     except IOError:
#         try:
#             font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
#         except IOError:
#             font = ImageFont.load_default()
#     bbox = draw.textbbox((0, 0), text, font=font)
#     w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
#     shadow_offset = 2
#     draw.text(((size[0] - w) / 2 + shadow_offset, (size[1] - h) / 2 + shadow_offset), text, fill='black', font=font)
#     draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=text_color, font=font)
#     path = f"temp_text_{abs(hash(text))}.png"
#     img.save(path)
#     print(f"Created text image: {path}")
#     return path

# def get_proportional_images(images, num_texts):
#     num_images = len(images)
#     if num_images >= num_texts:
#         return images[:num_texts]
#     repeats = []
#     per_image = num_texts / num_images
#     for i in range(num_images):
#         count = round(per_image * (i + 1)) - round(per_image * i)
#         repeats.extend([images[i]] * count)
#     return repeats

# def save_metadata(data):
#     meta_path = os.path.splitext(data["output_filename"])[0] + ".json"
#     with open(meta_path, "w") as f:
#         json.dump(data, f, indent=4)
#     print(f"Metadata saved to: {meta_path}")

# def load_metadata(meta_path):
#     if os.path.exists(meta_path):
#         with open(meta_path, "r") as f:
#             data = json.load(f)
#         print("Metadata loaded successfully.")
#         return data
#     else:
#         raise FileNotFoundError(f"No metadata found at {meta_path}")

# def create_invitation_video(data):
#     duration_per_clip = data.get("duration", 3)
#     animation_type = data.get("animation", "none")
#     video_size = (1280, 720)
#     clips = []
#     temp_paths = []

#     raw_paths = data.get("images", [])
#     if not raw_paths:
#         raise ValueError("No images provided.")
#     images = [path for path in raw_paths if os.path.exists(path)]

#     if not images:
#         raise ValueError("No valid images found.")

#     print(f"Total background images found: {len(images)}")

#     if data["type"] == "wedding":
#         text_slides = [
#             f"{data['groom_name']} ❤️ {data['bride_name']}",
#             "Invite you to celebrate their wedding",
#             f"On {data['wedding_date']}",
#             f"At {data['venue']}"
#         ]
#     elif data["type"] == "birthday":
#         text_slides = [f"You're Invited to {data['name']}'s Birthday Party!"]
#         if data["age"]:
#             text_slides.append(f"Turning {data['age']} 🎉")
#         text_slides += [
#             f"On {data['date']} at {data['time']}",
#             f"At {data['venue']}"
#         ]
#     else:
#         print("Unknown invitation type.")
#         return

#     images = get_proportional_images(images, len(text_slides))

#     for i, (text, img_path) in enumerate(zip(text_slides, images)):
#         print(f"Creating clip {i+1}/{len(text_slides)} with background: {img_path}")
#         try:
#             bg_img = Image.open(img_path).resize(video_size, Image.Resampling.LANCZOS)
#             temp_bg_path = f"temp_bg_{i}.jpg"
#             bg_img.save(temp_bg_path)
#             temp_paths.append(temp_bg_path)
#         except:
#             temp_bg_path = f"temp_default_bg_{i}.jpg"
#             Image.new('RGB', video_size, color='lightblue').save(temp_bg_path)
#             temp_paths.append(temp_bg_path)

#         base_bg = ImageClip(temp_bg_path).set_duration(duration_per_clip)
#         text_img_path = create_text_image(text, size=video_size)
#         temp_paths.append(text_img_path)
#         text_clip = (
#             ImageClip(text_img_path, transparent=True)
#             .set_duration(duration_per_clip)
#             .set_position("center")
#             .fadein(0.5)
#             .fadeout(0.5)
#         )

#         overlay_clips = [base_bg.copy(), text_clip]
#         anim_clip = get_animation_clip(animation_type, duration_per_clip)
#         if anim_clip:
#             overlay_clips.append(anim_clip)
#             print(f"Added {animation_type} animation to clip {i+1}")

#         clips.append(CompositeVideoClip(overlay_clips).set_duration(duration_per_clip))

#     print("Concatenating all clips...")
#     final_video = concatenate_videoclips(clips)

#     if os.path.exists(data["music_path"]):
#         final_video = final_video.set_audio(AudioFileClip(data["music_path"]))
#     else:
#         print("Music not found. Proceeding without audio.")

#     os.makedirs(os.path.dirname(data["output_filename"]), exist_ok=True)
#     print(f"Saving final video to: {data['output_filename']}")
#     final_video.write_videofile(data["output_filename"], fps=24)

#     save_metadata(data)

#     print("Cleaning up temporary files...")
#     for path in temp_paths:
#         if os.path.exists(path):
#             os.remove(path)
#             print(f"Removed: {path}")

#     print("Video generation completed!")






# from moviepy.editor import *
# from PIL import Image, ImageDraw, ImageFont
# import os
# import torch
# from diffusers import StableDiffusionPipeline
# from math import ceil
# import json
# import numpy as np


# print(torch.cuda.is_available())

# device = "cuda" if torch.cuda.is_available() else "cpu"
# pipe = StableDiffusionPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device == "cuda" else torch.float32
# ).to(device)

# def generate_image_from_prompt(prompt, output_path="assets/generated_background.jpg"):
#     print(f"Generating AI image from prompt: {prompt}")
#     image = pipe(prompt).images[0]
#     os.makedirs("assets", exist_ok=True)
#     image = image.resize((1280, 720), Image.Resampling.LANCZOS)
#     image.save(output_path)
#     print(f"Generated image saved to: {output_path}")
#     return output_path

# def get_animation_clip(animation_type, duration, size=(1280, 720)):
#     anim_clip_path = {
#         "balloons": "assets/animations/balloons.mp4",
#         "confetti": "assets/animations/confetti.mp4"
#     }.get(animation_type)

#     if anim_clip_path and os.path.exists(anim_clip_path):
#         return VideoFileClip(anim_clip_path).resize(size).set_duration(duration).set_position("center").set_opacity(0.5)
#     return None

# def create_text_image(text, size=(1280, 720), font_size=60, bg_color=(0, 0, 0, 0), text_color='white'):
#     img = Image.new('RGBA', size, color=bg_color)
#     draw = ImageDraw.Draw(img)
#     try:
#         font = ImageFont.truetype("arial.ttf", font_size)
#     except IOError:
#         try:
#             font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
#         except IOError:
#             font = ImageFont.load_default()
#     bbox = draw.textbbox((0, 0), text, font=font)
#     w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
#     shadow_offset = 2
#     draw.text(((size[0] - w) / 2 + shadow_offset, (size[1] - h) / 2 + shadow_offset), text, fill='black', font=font)
#     draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=text_color, font=font)
#     path = f"temp_text_{abs(hash(text))}.png"
#     img.save(path)
#     print(f"Created text image: {path}")
#     return path

# def get_proportional_images(images, num_texts):
#     num_images = len(images)
#     if num_images >= num_texts:
#         return images[:num_texts]
#     repeats = []
#     per_image = num_texts / num_images
#     for i in range(num_images):
#         count = round(per_image * (i + 1)) - round(per_image * i)
#         repeats.extend([images[i]] * count)
#     return repeats

# def save_metadata(data):
#     meta_path = os.path.splitext(data["output_filename"])[0] + ".json"
#     with open(meta_path, "w") as f:
#         json.dump(data, f, indent=4)
#     print(f"Metadata saved to: {meta_path}")

# def load_metadata(meta_path):
#     if os.path.exists(meta_path):
#         with open(meta_path, "r") as f:
#             data = json.load(f)
#         print("Metadata loaded successfully.")
#         return data
#     else:
#         raise FileNotFoundError(f"No metadata found at {meta_path}")

# def create_invitation_video(data):
#     duration_per_clip = data.get("duration", 3)
#     animation_type = data.get("animation", "none")
#     video_size = (1280, 720)
#     clips = []
#     temp_paths = []

#     raw_paths = data.get("images", [])
#     if not raw_paths:
#         raise ValueError("No images provided.")
#     images = [path for path in raw_paths if os.path.exists(path)]

#     if not images:
#         raise ValueError("No valid images found.")

#     print(f"Total background images found: {len(images)}")

#     if data["type"] == "wedding":
#         text_slides = [
#             f"{data['groom_name']} ❤️ {data['bride_name']}",
#             "Invite you to celebrate their wedding",
#             f"On {data['wedding_date']}",
#             f"At {data['venue']}"
#         ]
#     elif data["type"] == "birthday":
#         text_slides = [f"You're Invited to {data['name']}'s Birthday Party!"]
#         if data["age"]:
#             text_slides.append(f"Turning {data['age']} 🎉")
#         text_slides += [
#             f"On {data['date']} at {data['time']}",
#             f"At {data['venue']}"
#         ]
#     else:
#         print("Unknown invitation type.")
#         return

#     images = get_proportional_images(images, len(text_slides))

#     for i, (text, img_path) in enumerate(zip(text_slides, images)):
#         print(f"Creating clip {i+1}/{len(text_slides)} with background: {img_path}")
#         try:
#             bg_img = Image.open(img_path).resize(video_size, Image.Resampling.LANCZOS).convert("RGBA")
#         except:
#             print(f"Failed to load image: {img_path}, using fallback.")
#             bg_img = Image.new("RGBA", video_size, color="lightblue")

#         base_bg = ImageClip(np.array(bg_img)).set_duration(duration_per_clip)

#         text_img_path = create_text_image(text, size=video_size)
#         temp_paths.append(text_img_path)
#         text_clip = (
#             ImageClip(text_img_path, transparent=True)
#             .set_duration(duration_per_clip)
#             .set_position(("center",))
#             .fadein(0.5)
#             .fadeout(0.5)
#         )

#         overlay_clips = [base_bg.copy(), text_clip]
#         anim_clip = get_animation_clip(animation_type, duration_per_clip)
#         if anim_clip:
#             overlay_clips.append(anim_clip)
#             print(f"Added {animation_type} animation to clip {i+1}")

#         clips.append(CompositeVideoClip(overlay_clips).set_duration(duration_per_clip))

#     print("Concatenating all clips...")
#     final_video = concatenate_videoclips(clips)

#     if os.path.exists(data["music_path"]):
#         final_video = final_video.set_audio(AudioFileClip(data["music_path"]))
#     else:
#         print("Music not found. Proceeding without audio.")

#     os.makedirs(os.path.dirname(data["output_filename"]), exist_ok=True)
#     print(f"Saving final video to: {data['output_filename']}")
#     final_video.write_videofile(data["output_filename"], fps=24)

#     save_metadata(data)

#     print("Cleaning up temporary files...")
#     for path in temp_paths:
#         if os.path.exists(path):
#             os.remove(path)
#             print(f"Removed: {path}")

#     print("Video generation completed!")


# codw with centre bottom text
# from moviepy.editor import *
# from PIL import Image, ImageDraw, ImageFont
# import os
# import torch
# from diffusers import StableDiffusionPipeline
# from math import ceil
# import json
# import numpy as np


# print(torch.cuda.is_available())

# device = "cuda" if torch.cuda.is_available() else "cpu"
# pipe = StableDiffusionPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device == "cuda" else torch.float32
# ).to(device)

# def generate_image_from_prompt(prompt, output_path="assets/generated_background.jpg"):
#     print(f"Generating AI image from prompt: {prompt}")
#     image = pipe(prompt).images[0]
#     os.makedirs("assets", exist_ok=True)
#     image = image.resize((1280, 720), Image.Resampling.LANCZOS)
#     image.save(output_path)
#     print(f"Generated image saved to: {output_path}")
#     return output_path

# def get_animation_clip(animation_type, duration, size=(1280, 720)):
#     anim_clip_path = {
#         "balloons": "assets/animations/balloons.mp4",
#         "confetti": "assets/animations/confetti.mp4"
#     }.get(animation_type)

#     if anim_clip_path and os.path.exists(anim_clip_path):
#         return VideoFileClip(anim_clip_path).resize(size).set_duration(duration).set_position("center").set_opacity(0.5)
#     return None

# def create_text_image(text, size=(1280, 720), font_size=60, bg_color=(0, 0, 0, 0), text_color='white'):
#     img = Image.new('RGBA', size, color=bg_color)
#     draw = ImageDraw.Draw(img)
#     try:
#         font = ImageFont.truetype("arial.ttf", font_size)
#     except IOError:
#         try:
#             font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
#         except IOError:
#             font = ImageFont.load_default()
#     bbox = draw.textbbox((0, 0), text, font=font)
#     w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
#     shadow_offset = 2
#     # Position text at bottom with some margin
#     text_x = (size[0] - w) / 2
#     text_y = size[1] - h - 50  # 50 pixels from bottom
#     draw.text((text_x + shadow_offset, text_y + shadow_offset), text, fill='black', font=font)
#     draw.text((text_x, text_y), text, fill=text_color, font=font)
#     path = f"temp_text_{abs(hash(text))}.png"
#     img.save(path)
#     print(f"Created text image: {path}")
#     return path

# def get_proportional_images(images, num_texts):
#     num_images = len(images)
#     if num_images >= num_texts:
#         return images[:num_texts]
#     repeats = []
#     per_image = num_texts / num_images
#     for i in range(num_images):
#         count = round(per_image * (i + 1)) - round(per_image * i)
#         repeats.extend([images[i]] * count)
#     return repeats

# def save_metadata(data):
#     meta_path = os.path.splitext(data["output_filename"])[0] + ".json"
#     with open(meta_path, "w") as f:
#         json.dump(data, f, indent=4)
#     print(f"Metadata saved to: {meta_path}")

# def load_metadata(meta_path):
#     if os.path.exists(meta_path):
#         with open(meta_path, "r") as f:
#             data = json.load(f)
#         print("Metadata loaded successfully.")
#         return data
#     else:
#         raise FileNotFoundError(f"No metadata found at {meta_path}")

# def create_invitation_video(data):
#     duration_per_clip = data.get("duration", 3)
#     animation_type = data.get("animation", "none")
#     video_size = (1280, 720)
#     clips = []
#     temp_paths = []

#     raw_paths = data.get("images", [])
#     if not raw_paths:
#         raise ValueError("No images provided.")
#     images = [path for path in raw_paths if os.path.exists(path)]

#     if not images:
#         raise ValueError("No valid images found.")

#     print(f"Total background images found: {len(images)}")

#     if data["type"] == "wedding":
#         text_slides = [
#             f"{data['groom_name']} ❤️ {data['bride_name']}",
#             "Invite you to celebrate their wedding",
#             f"On {data['wedding_date']}",
#             f"At {data['venue']}"
#         ]
#     elif data["type"] == "birthday":
#         text_slides = [f"You're Invited to {data['name']}'s Birthday Party!"]
#         if data["age"]:
#             text_slides.append(f"Turning {data['age']} 🎉")
#         text_slides += [
#             f"On {data['date']} at {data['time']}",
#             f"At {data['venue']}"
#         ]
#     else:
#         print("Unknown invitation type.")
#         return

#     images = get_proportional_images(images, len(text_slides))

#     # We'll keep track of all opened clips to close later
#     opened_clips = []

#     for i, (text, img_path) in enumerate(zip(text_slides, images)):
#         print(f"Creating clip {i+1}/{len(text_slides)} with background: {img_path}")
#         try:
#             bg_img = Image.open(img_path).resize(video_size, Image.Resampling.LANCZOS).convert("RGBA")
#         except:
#             print(f"Failed to load image: {img_path}, using fallback.")
#             bg_img = Image.new("RGBA", video_size, color="lightblue")

#         base_bg = ImageClip(np.array(bg_img)).set_duration(duration_per_clip)
#         opened_clips.append(base_bg)

#         text_img_path = create_text_image(text, size=video_size)
#         temp_paths.append(text_img_path)
#         text_clip = (
#             ImageClip(text_img_path, transparent=True)
#             .set_duration(duration_per_clip)
#             .set_position("center")
#             .fadein(0.5)
#             .fadeout(0.5)
#         )
#         opened_clips.append(text_clip)

#         overlay_clips = [base_bg, text_clip]
#         anim_clip = get_animation_clip(animation_type, duration_per_clip)
#         if anim_clip:
#             overlay_clips.append(anim_clip)
#             opened_clips.append(anim_clip)
#             print(f"Added {animation_type} animation to clip {i+1}")

#         composite_clip = CompositeVideoClip(overlay_clips).set_duration(duration_per_clip)
#         opened_clips.append(composite_clip)
#         clips.append(composite_clip)

#     print("Concatenating all clips...")
#     final_video = concatenate_videoclips(clips)
#     opened_clips.append(final_video)

#     audio_clip = None
#     if os.path.exists(data["music_path"]):
#         audio_clip = AudioFileClip(data["music_path"])
#         final_video = final_video.set_audio(audio_clip)
#         opened_clips.append(audio_clip)
#     else:
#         print("Music not found. Proceeding without audio.")

#     os.makedirs(os.path.dirname(data["output_filename"]), exist_ok=True)
#     print(f"Saving final video to: {data['output_filename']}")
#     final_video.write_videofile(data["output_filename"], fps=24)

#     save_metadata(data)

#     print("Cleaning up temporary files...")
#     for path in temp_paths:
#         if os.path.exists(path):
#             os.remove(path)
#             print(f"Removed: {path}")

#     # Close all opened clips to avoid the WinError 6 on Windows
#     for clip in opened_clips:
#         try:
#             clip.close()
#         except Exception as e:
#             print(f"Failed to close clip: {e}")

#     print("Video generation completed!")






#code with multiple photos at center
# from moviepy.editor import *
# from PIL import Image, ImageDraw, ImageFont
# import os
# import torch
# from diffusers import StableDiffusionPipeline
# import json
# import numpy as np

# print(torch.cuda.is_available())

# device = "cuda" if torch.cuda.is_available() else "cpu"
# pipe = StableDiffusionPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5",
#     torch_dtype=torch.float16 if device == "cuda" else torch.float32
# ).to(device)


# def generate_image_from_prompt(prompt, output_path="assets/generated_background.jpg"):
#     print(f"Generating AI image from prompt: {prompt}")
#     image = pipe(prompt).images[0]
#     os.makedirs("assets", exist_ok=True)
#     image = image.resize((1280, 720), Image.Resampling.LANCZOS)
#     image.save(output_path)
#     print(f"Generated image saved to: {output_path}")
#     return output_path


# def get_animation_clip(animation_type, duration, size=(1280, 720)):
#     anim_clip_path = {
#         "balloons": "assets/animations/balloons.mp4",
#         "confetti": "assets/animations/confetti.mp4"
#     }.get(animation_type)

#     if anim_clip_path and os.path.exists(anim_clip_path):
#         return VideoFileClip(anim_clip_path).resize(size).set_duration(duration).set_position("center").set_opacity(0.5)
#     return None


# def create_text_image(text, size=(1280, 720), font_size=60, bg_color=(0, 0, 0, 0), text_color='white'):
#     img = Image.new('RGBA', size, color=bg_color)
#     draw = ImageDraw.Draw(img)
#     try:
#         font = ImageFont.truetype("arial.ttf", font_size)
#     except IOError:
#         try:
#             font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
#         except IOError:
#             font = ImageFont.load_default()
#     bbox = draw.textbbox((0, 0), text, font=font)
#     w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
#     shadow_offset = 2
#     text_x = (size[0] - w) / 2
#     text_y = size[1] - h - 50  # Position 50px from bottom
#     draw.text((text_x + shadow_offset, text_y + shadow_offset), text, fill='black', font=font)
#     draw.text((text_x, text_y), text, fill=text_color, font=font)
#     path = f"temp_text_{abs(hash(text))}.png"
#     img.save(path)
#     print(f"Created text image: {path}")
#     return path


# def get_proportional_images(images, num_texts):
#     num_images = len(images)
#     if num_images >= num_texts:
#         return images[:num_texts]
#     repeats = []
#     per_image = num_texts / num_images
#     for i in range(num_images):
#         count = round(per_image * (i + 1)) - round(per_image * i)
#         repeats.extend([images[i]] * count)
#     return repeats


# def save_metadata(data):
#     meta_path = os.path.splitext(data["output_filename"])[0] + ".json"
#     with open(meta_path, "w") as f:
#         json.dump(data, f, indent=4)
#     print(f"Metadata saved to: {meta_path}")


# def load_metadata(meta_path):
#     if os.path.exists(meta_path):
#         with open(meta_path, "r") as f:
#             data = json.load(f)
#         print("Metadata loaded successfully.")
#         return data
#     else:
#         raise FileNotFoundError(f"No metadata found at {meta_path}")


# def create_invitation_video(data):
#     duration_per_clip = data.get("duration", 3)
#     animation_type = data.get("animation", "none")
#     video_size = (1280, 720)
#     clips = []
#     temp_paths = []

#     raw_paths = data.get("images", [])
#     if not raw_paths:
#         raise ValueError("No images provided.")
#     images = [path for path in raw_paths if os.path.exists(path)]

#     if not images:
#         raise ValueError("No valid images found.")

#     print(f"Total background images found: {len(images)}")

#     if data["type"] == "wedding":
#         text_slides = [
#             f"{data['groom_name']} ❤️ {data['bride_name']}",
#             "Invite you to celebrate their wedding",
#             f"On {data['wedding_date']}",
#             f"At {data['venue']}"
#         ]
#     elif data["type"] == "birthday":
#         text_slides = [f"You're Invited to {data['name']}'s Birthday Party!"]
#         if data["age"]:
#             text_slides.append(f"Turning {data['age']} 🎉")
#         text_slides += [
#             f"On {data['date']} at {data['time']}",
#             f"At {data['venue']}"
#         ]
#     else:
#         print("Unknown invitation type.")
#         return

#     images = get_proportional_images(images, len(text_slides))
#     opened_clips = []

#     for i, (text, img_path) in enumerate(zip(text_slides, images)):
#         print(f"Creating clip {i+1}/{len(text_slides)} with background: {img_path}")
#         try:
#             bg_img = Image.open(img_path).resize(video_size, Image.Resampling.LANCZOS).convert("RGBA")
#         except:
#             print(f"Failed to load image: {img_path}, using fallback.")
#             bg_img = Image.new("RGBA", video_size, color="lightblue")

#         base_bg = ImageClip(np.array(bg_img)).set_duration(duration_per_clip)
#         opened_clips.append(base_bg)

#         text_img_path = create_text_image(text, size=video_size)
#         temp_paths.append(text_img_path)
#         text_clip = (
#             ImageClip(text_img_path, transparent=True)
#             .set_duration(duration_per_clip)
#             .set_position("center")
#             .fadein(0.5)
#             .fadeout(0.5)
#         )
#         opened_clips.append(text_clip)

#         overlay_clips = [base_bg, text_clip]
#         anim_clip = get_animation_clip(animation_type, duration_per_clip)
#         if anim_clip:
#             overlay_clips.append(anim_clip)
#             opened_clips.append(anim_clip)
#             print(f"Added {animation_type} animation to clip {i+1}")

#         composite_clip = CompositeVideoClip(overlay_clips).set_duration(duration_per_clip)
#         opened_clips.append(composite_clip)
#         clips.append(composite_clip)

#     print("Concatenating all clips...")
#     final_video = concatenate_videoclips(clips)
#     opened_clips.append(final_video)

#     audio_clip = None
#     if os.path.exists(data["music_path"]):
#         audio_clip = AudioFileClip(data["music_path"])
#         final_video = final_video.set_audio(audio_clip)
#         opened_clips.append(audio_clip)
#     else:
#         print("Music not found. Proceeding without audio.")

#     os.makedirs(os.path.dirname(data["output_filename"]), exist_ok=True)
#     print(f"Saving final video to: {data['output_filename']}")
#     final_video.write_videofile(data["output_filename"], fps=24)

#     save_metadata(data)

#     print("Cleaning up temporary files...")
#     for path in temp_paths:
#         if os.path.exists(path):
#             os.remove(path)
#             print(f"Removed: {path}")

#     for clip in opened_clips:
#         try:
#             clip.close()
#         except Exception as e:
#             print(f"Failed to close clip: {e}")

#     print("Video generation completed!")




import os
os.environ["IMAGEMAGICK_BINARY"] = "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"

from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import torch
from diffusers import StableDiffusionPipeline
import json
import numpy as np

print(torch.cuda.is_available())

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)


def generate_image_from_prompt(prompt, output_path="assets/generated_background.jpg"):
    print(f"Generating AI image from prompt: {prompt}")
    image = pipe(prompt).images[0]
    os.makedirs("assets", exist_ok=True)
    image = image.resize((1280, 720), Image.Resampling.LANCZOS)
    image.save(output_path)
    print(f"Generated image saved to: {output_path}")
    return output_path


def get_animation_clip(animation_type, duration, size=(1280, 720)):
    anim_clip_path = {
        "balloons": "assets/animations/balloons.mp4",
        "confetti": "assets/animations/confetti.mp4"
    }.get(animation_type)

    if anim_clip_path and os.path.exists(anim_clip_path):
        return VideoFileClip(anim_clip_path).resize(size).set_duration(duration).set_position("center").set_opacity(0.5)
    return None


def create_text_image(text, size=(1280, 720), font_size=60, bg_color=(0, 0, 0, 0), text_color='white'):
    img = Image.new('RGBA', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    shadow_offset = 2
    text_x = (size[0] - w) / 2
    text_y = size[1] - h - 50  # Position 50px from bottom
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, fill='black', font=font)
    draw.text((text_x, text_y), text, fill=text_color, font=font)
    path = f"temp_text_{abs(hash(text))}.png"
    img.save(path)
    print(f"Created text image: {path}")
    return path


def get_proportional_images(images, num_texts):
    num_images = len(images)
    if num_images >= num_texts:
        return images[:num_texts]
    repeats = []
    per_image = num_texts / num_images
    for i in range(num_images):
        count = round(per_image * (i + 1)) - round(per_image * i)
        repeats.extend([images[i]] * count)
    return repeats


def save_metadata(data):
    meta_path = os.path.splitext(data["output_filename"])[0] + ".json"
    with open(meta_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Metadata saved to: {meta_path}")


def load_metadata(meta_path):
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            data = json.load(f)
        print("Metadata loaded successfully.")
        return data
    else:
        raise FileNotFoundError(f"No metadata found at {meta_path}")

def get_sticker_clips(sticker_paths, duration, positions, sizes):
    sticker_clips = []
    for i, path in enumerate(sticker_paths):
        if not os.path.exists(path):
            print(f"Sticker not found: {path}")
            continue

        try:
            position = positions[i] if i < len(positions) else ("right", "top")
            size = sizes[i] if i < len(sizes) else (100, 100)
            clip = ImageClip(path).resize(size).set_duration(duration)

            # Support both ("left", "top") and (x, y)
            if isinstance(position, str) or (isinstance(position, tuple) and any(isinstance(p, str) for p in position)):
                clip = clip.set_position(position)
            elif isinstance(position, tuple) and all(isinstance(p, int) for p in position):
                clip = clip.set_position(position)
            else:
                print(f"Invalid position for sticker: {position}. Using default.")
                clip = clip.set_position(("right", "top"))

            sticker_clips.append(clip)
        except Exception as e:
            print(f"Error loading sticker {path}: {e}")
    return sticker_clips




def create_invitation_video(data):
    duration_per_clip = data.get("duration", 3)
    animation_type = data.get("animation", "none")
    video_size = (1280, 720)
    clips = []
    temp_paths = []

    raw_paths = data.get("images", [])
    if not raw_paths:
        raise ValueError("No images provided.")
    images = [path for path in raw_paths if os.path.exists(path)]                                   

    if not images:
        raise ValueError("No valid images found.")

    print(f"Total background images found: {len(images)}")

    text_slides = data.get("text_slides")
    if not text_slides:
        raise ValueError("No text slides provided.")


    images = get_proportional_images(images, len(text_slides))
    opened_clips = []

    sticker_paths = data.get("sticker_paths", [])
    sticker_positions = data.get("sticker_positions", [])
    sticker_sizes = data.get("sticker_sizes", [])

    for i, (text, img_path) in enumerate(zip(text_slides, images)):
        print(f"Creating clip {i+1}/{len(text_slides)} with background: {img_path}")
        try:
            bg_img = Image.open(img_path).resize(video_size, Image.Resampling.LANCZOS).convert("RGBA")
        except:
            print(f"Failed to load image: {img_path}, using fallback.")
            bg_img = Image.new("RGBA", video_size, color="lightblue")

        base_bg = ImageClip(np.array(bg_img)).set_duration(duration_per_clip)
        opened_clips.append(base_bg)

        text_img_path = create_text_image(text, size=video_size)
        temp_paths.append(text_img_path)
        text_clip = (
            ImageClip(text_img_path, transparent=True)
            .set_duration(duration_per_clip)
            .set_position("center")
            .fadein(0.5)
            .fadeout(0.5)
        )
        opened_clips.append(text_clip)

        overlay_clips = [base_bg, text_clip]

        # Add sticker if provided
        # Add multiple stickers
        if sticker_paths:
            sticker_clips = get_sticker_clips(sticker_paths, duration_per_clip, sticker_positions, sticker_sizes)
            for sc in sticker_clips:
                overlay_clips.append(sc)
                opened_clips.append(sc)


        # Add animation if provided
        anim_clip = get_animation_clip(animation_type, duration_per_clip)
        if anim_clip:
            overlay_clips.append(anim_clip)
            opened_clips.append(anim_clip)
            print(f"Added {animation_type} animation to clip {i+1}")

        composite_clip = CompositeVideoClip(overlay_clips).set_duration(duration_per_clip)
        opened_clips.append(composite_clip)
        clips.append(composite_clip)

    print("Concatenating all clips...")
    final_video = concatenate_videoclips(clips)
    opened_clips.append(final_video)

    audio_clip = None
    if os.path.exists(data["music_path"]):
        audio_clip = AudioFileClip(data["music_path"])
        final_video = final_video.set_audio(audio_clip)
        opened_clips.append(audio_clip)
    else:
        print("Music not found. Proceeding without audio.")

    os.makedirs(os.path.dirname(data["output_filename"]), exist_ok=True)
    print(f"Saving final video to: {data['output_filename']}")
    final_video.write_videofile(data["output_filename"], fps=24)

    save_metadata(data)

    print("Cleaning up temporary files...")
    for path in temp_paths:
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed: {path}")

    for clip in opened_clips:
        try:
            clip.close()
        except Exception as e:
            print(f"Failed to close clip: {e}")

    print("Video generation completed!")
