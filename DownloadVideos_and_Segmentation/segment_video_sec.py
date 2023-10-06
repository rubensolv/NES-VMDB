# import cv2
import os
import argparse
import numpy as np
import moviepy.editor as mp

def segment_video(video_path, segment_ranges):
    shots_dir = os.path.splitext(os.path.basename(args.video))[0]
    shots_path = os.path.join(shots_dir, '%d.mp4')
    video_clip = mp.VideoFileClip(video_path)

    for i, (start_frame, end_frame) in enumerate(segment_ranges):
        print(f'--- Processing scene {i}: {start_frame}-{end_frame}')

        start_time = start_frame#*video_clip.fps
        end_time = end_frame#*video_clip.fps
        print(start_time, end_time)
        shot = video_clip.subclip(float(start_time), float(end_time))
        print(shot)
        #shot = video_clip.set_audio
        shot.write_videofile(shots_path % i, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
     # Parse arguments
    parser = argparse.ArgumentParser(description='train_ftm.py')
    parser.add_argument('--video', type=str, required=True, help="Path to input video.", default='/home/rubens/pythonProjects/NesToMidGeneration/data/yt_nes_mp4/Castlevania\ \(NES\)\ Playthrough.mp4')
    parser.add_argument('--scenes', type=str, required=True, help="Path with cute scenes.", default='/home/rubens/pythonProjects/NesToMidGeneration/DownloadVideos\ and\ Segmentation/output/transitions.txt')
    args = parser.parse_args()

    # Create dir with video name
    shots_dir = os.path.splitext(os.path.basename(args.video))[0]
    os.makedirs(shots_dir, exist_ok=True)

    # Segment Video
    scenes = np.loadtxt(args.scenes, dtype=float, delimiter=' ')
    print(scenes)
    print("Segmenting Video")
    segment_video(args.video, scenes)

    # print("Segmenting Audio")
    # segment_audio(args.video, scenes)