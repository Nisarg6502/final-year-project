#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pathlib import Path
from pexels import query_images
from pexels import search_images

def images_to_video(images, output_dir='Images', video_size=(1920, 1080)):
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []

    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"image_{i}.jpg")
        image.save(image_path, "JPEG")
        image_paths.append(image_path)

    stitch_images(image_paths, output_dir, video_size)

# Step 1: Stitch Images
def stitch_images(image_paths, output_dir='Output_Video', video_size=(1920, 1080)):
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of image paths
    image_paths = [str(img_path) for img_path in Path(image_paths).glob('*.jpg')]
    
    # Load each image as a video clip and set duration to 5 seconds
    clips = [VideoFileClip(image_path).resize(video_size).set_duration(5).crossfadein(0.5).crossfadeout(0.5).set_position(lambda t: ("left", "center")) for image_path in image_paths]
    
    # Concatenate the clips to create the final video
    final_clip = concatenate_videoclips(clips)
    
    # Write the final video to the output directory
    output_video_path = os.path.join(output_dir, "stitched_video.mp4")
    final_clip.write_videofile(output_video_path, fps=10)

# Step 2: Define time_to_seconds function as before
def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

# Step 3: Define create_subtitle_clips function as before
def create_subtitle_clips(subtitles, video_size=(1920, 1080), fontsize=40, font='Arial', color='yellow'):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        # Adjust the relative size of the text by changing the // 20 value
        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color='black',
                             size=(video_size[0], video_size[1] * 3 // 20)).set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_size[1] * 17 // 20

        text_position = (subtitle_x_position, subtitle_y_position)
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips

# Step 4: Process Press Release
def process_press_release(stitched_video_path, srt_file='subtitling.txt', output_subtitled_folder='Output_Video_Subtitled'):
    # Load stitched video
    video = VideoFileClip(stitched_video_path)

    # Load subtitles
    subtitles = pysrt.open(srt_file)

    # Create subtitle clips
    subtitle_clips = create_subtitle_clips(subtitles, video.size)

    # Add subtitles to the video
    final_video = CompositeVideoClip([video] + subtitle_clips)

    # Write subtitled video file
    begin, _ = os.path.splitext(os.path.basename(stitched_video_path))
    output_subtitled_file = os.path.join(output_subtitled_folder, begin + '_subtitled' + ".mp4")
    final_video.write_videofile(output_subtitled_file, codec='libx264')

# Step 1: Stitch Images
# list_query = ["Orange", "Cat", "Sleeping", "Table"]
# query_id = search_images(list_query, api_key)
# images = query_images()
# images_to_video(images)

# Step 4: Process Press Release
process_press_release(os.path.join('Output_Video', "stitched_video.mp4"))


# In[ ]:




