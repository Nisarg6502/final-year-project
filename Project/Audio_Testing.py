#!/usr/bin/env python
# coding: utf-8

# In[1]:


from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os


# In[2]:


# Get the desired video title
# title = input("Enter a title: ")


# In[3]:
def merge_av(audio, video):

    # Open the video and audio
    video_clip = VideoFileClip(video)
    audio_clip = AudioFileClip(audio)


    # In[4]:


    # Concatenate the video clip with the audio clip
    final_clip = video_clip.set_audio(audio_clip)


    # In[5]:


    # Export the final video with audio
    final_clip.write_videofile("Final_Merged" + ".mp4")


# In[ ]:




