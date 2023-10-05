# import cv2
import os
import argparse
import numpy as np
import moviepy.editor as mp

# def segment_video(video_path, segment_ranges):
#     shots_path = '%d.mp4' 
#
#     cap = cv2.VideoCapture(video_path)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#
#     for i, (start_frame, end_frame) in enumerate(segment_ranges):
#         print(f'--- Processing scene {i}: {start_frame}-{end_frame}')
#
#         writer = cv2.VideoWriter(shots_path % i, fourcc, fps, size)
#         cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
#        
#         ret = True # has frame returned
#         while(cap.isOpened() and ret and writer.isOpened()):
#             ret, frame = cap.read()
#             frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
#             if frame_number < end_frame:
#                 writer.write(frame)
#             else:
#                 break
#
#         writer.release()

# def segment_audio(video_path, segment_ranges, fps=30):
#     shots_path = '%d.mp4'
#     video_clip = mp.VideoFileClip(video_path)
#    
#     for i, (start_frame, end_frame) in enumerate(segment_ranges):
#         print(f'--- Processing scene {i}: {start_frame}-{end_frame}')
#
#         start_time = (start_frame - 1)/fps
#         end_time = (end_frame - 1)/fps
#
#         # Load audio subclip for frames start_frame and end_frame
#         audio_clip = video_clip.audio.subclip(start_time, end_time)
#         audio_clip.write_audiofile('%d.mp3' % i)
#        
#         # Load shot with index and attach audio
#         shot = mp.VideoFileClip(shots_path % i)
#         shot_with_audio = shot.set_audio(audio_clip)
#         shot_with_audio.write_videofile(shots_path % i, codec='libx264', audio_codec='aac')
#        
#         # audio_clip.close()
#         shot.close()

def segment_video(video_path, segment_ranges):
    shots_dir = os.path.splitext(os.path.basename(args.video))[0]
    shots_path = os.path.join(shots_dir, '%d.mp4')
    video_clip = mp.VideoFileClip(video_path)

    for i, (start_frame, end_frame) in enumerate(segment_ranges):
        print(f'--- Processing scene {i}: {start_frame}-{end_frame}')

        start_time = start_frame/video_clip.fps
        end_time = end_frame/video_clip.fps

        shot = video_clip.subclip(start_time, end_time)
        shot.write_videofile(shots_path % i, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
     # Parse arguments
    parser = argparse.ArgumentParser(description='train_ftm.py')
    parser.add_argument('--video', type=str, required=True, help="Path to input video.")
    parser.add_argument('--scenes', type=str, required=True, help="Path with cute scenes.")
    args = parser.parse_args()

    # Create dir with video name
    shots_dir = os.path.splitext(os.path.basename(args.video))[0]
    os.makedirs(shots_dir, exist_ok=True)

    # Segment Video
    scenes = np.loadtxt(args.scenes, dtype=int, delimiter=' ')
    
    print("Segmenting Video")
    segment_video(args.video, scenes)

    # print("Segmenting Audio")
    # segment_audio(args.video, scenes)