from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
# Define the input video file and output directory
input_video_file = '/home/rubens/pythonProjects/NesToMidGeneration/data/test_slicing_mp4/Tecmo Super Bowl (NES) Playthrough [2022, Bengals season].mp4'
output_directory = '/home/rubens/pythonProjects/NesToMidGeneration/data/test_slicing_mp4/Tecmo Super Bowl (NES) Playthrough [2022, Bengals season]/'
# Define the duration of each segment in seconds (e.g., 15 seconds)
segment_duration = 15
# Create a VideoFileClip object from the input video
video = VideoFileClip(input_video_file)
# Get the total duration of the video in seconds
video_duration = video.duration
# Calculate the number of segments
num_segments = int(video_duration / segment_duration)
# Ensure the output directory exists
import os
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Iterate through the segments and extract each one
for i in range(num_segments):
    start_time = i * segment_duration
    end_time = (i + 1) * segment_duration
    # Define the output file name
    output_file = os.path.join(output_directory, f'segment_{i + 1}.mp4')
    # Extract the subclip
    ffmpeg_extract_subclip(input_video_file, start_time, end_time, targetname=output_file)
# Close the VideoFileClip object
video.reader.close()
print('Video segments have been created in the output directory.')