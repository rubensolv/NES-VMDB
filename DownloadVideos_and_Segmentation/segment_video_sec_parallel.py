# import cv2
import os
import argparse
import numpy as np
import moviepy.editor as mp

def segment_video(video_path, segment_ranges, shots_dir):    
    shots_path = os.path.join(shots_dir, '%d.mp4')
    video_clip = mp.VideoFileClip(video_path)

    for i, (start_frame, end_frame) in enumerate(segment_ranges):
        print(f'--- Processing scene {i}: {start_frame}-{end_frame}')

        start_time = start_frame#*video_clip.fps
        end_time = end_frame#*video_clip.fps
        #print(start_time, end_time)
        shot = video_clip.subclip(float(start_time), float(end_time))
        #print(shot)
        #shot = video_clip.set_audio
        shot.write_videofile(shots_path % i, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
     # Parse arguments
    videos_dir = '/storage1/dados/es91661/NesToMidGeneration/data/yt_nes_mp4/'
    scenes_dir = '/storage1/dados/es91661/NesToMidGeneration/data/list_transitions/'
    output_dir = '/storage1/dados/es91661/NesToMidGeneration/data/fragments/'
    
    #Collect all the scenes files
    scenes = os.listdir(scenes_dir)    
    for scene in scenes:        
        try:
            # Create dir with video name
            shots_dir = os.path.splitext(os.path.basename(scene))[0]
            shots_dir = os.path.join(output_dir,shots_dir)
            os.makedirs(shots_dir, exist_ok=True)

            # Segment Video
            scene_frags = np.loadtxt(os.path.join(scenes_dir,scene), dtype=float, delimiter=' ')
            print(scene_frags)
            print("Segmenting Video")
            segment_video(os.path.join(videos_dir,scene.replace('.txt','.mp4')), scene_frags, shots_dir)
        except:
            print('-------Problem on ',scene)
    # print("Segmenting Audio")
    # segment_audio(args.video, scenes)