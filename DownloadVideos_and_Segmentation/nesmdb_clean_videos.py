import os
import shutil 
import argparse
import re
import librosa
import matplotlib.pyplot as plt
import moviepy.editor as mp
import numpy as np

def traverse_dir(
        root_dir,
        extension=('mp4'),
        amount=None,
        str_=None,
        is_pure=False,
        verbose=False,
        is_sort=False,
        is_ext=True):

    if verbose:
        print('[*] Scanning...')

    cnt, file_list = 0, []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension):
                if (amount is not None) and (cnt == amount):
                    break
                if str_ is not None:
                    if str_ not in file:
                        continue

                mix_path = os.path.join(root, file)
                pure_path = mix_path[len(root_dir)+1:] if is_pure else mix_path

                if not is_ext:
                    ext = pure_path.split('.')[-1]
                    pure_path = pure_path[:-(len(ext)+1)]
                if verbose:
                    print(pure_path)
                file_list.append(pure_path)
                cnt += 1
    if verbose:
        print('Total: %d files' % len(file_list))
        print('Done!!!')

    if is_sort:
        file_list.sort()

    return file_list

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='clean.py')
    parser.add_argument('--path_indir', type=str, required=True)
    args = parser.parse_args()

    # list files
    videofiles = traverse_dir(
        args.path_indir,
        extension='mp4',
        is_pure=True,
        is_sort=True)
    n_files = len(videofiles)
    print('num video files:', n_files)

    wavfiles = traverse_dir(
        args.path_indir,
        extension='wav',
        is_pure=True,
        is_sort=True)
    n_files = len(videofiles)
    print('num wav files:', n_files)

    # collect
    data = []
    for fidx in range(n_files):
        path_video = videofiles[fidx]
        path_wav = wavfiles[fidx]
        print('{}/{}'.format(fidx, n_files))
    
        # paths
        path_videofile = os.path.join(args.path_indir, path_video)
        path_wavfile = os.path.join(args.path_indir, path_wav)

        print(f'{path_videofile}')
        print(f'{path_wavfile}')
        
        video_clip = mp.VideoFileClip(path_videofile)

        count_black = 0
        total_frames = 0
        for frame in video_clip.iter_frames():
            if (frame == 0).all() == True:
                count_black += 1
            total_frames += 1

        if count_black == total_frames:
            print("Complete black!")

        # samplerate, wave = wavfile.read(path_wavfile)
        # 
        video_clip.audio.write_audiofile("tmp.wav", ffmpeg_params=["-ac", "1"])
        wave, sr = librosa.load("tmp.wav", sr=None)
        silence = librosa.effects.split(y=wave, frame_length=1000, top_db=60)
        
        if silence.shape[0] == 1:
            silence_duration = silence[0][1] - silence[0][0]
            if silence_duration == wave.size:
                print("Complete silence!")
        
        # plt.plot(myaudio)
        # plt.savefig(f'{os.path.splitext(path_wavfile)[0]}.png')  
        # plt.clf()