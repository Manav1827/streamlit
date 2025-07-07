from moviepy.editor import ImageClip, concatenate_videoclips

def create_video_from_images(images, output="output.mp4"):
    clips = [ImageClip(img).set_duration(2) for img in images]
    video = concatenate_videoclips(clips)
    video.write_videofile(output, fps=24)
    return output
