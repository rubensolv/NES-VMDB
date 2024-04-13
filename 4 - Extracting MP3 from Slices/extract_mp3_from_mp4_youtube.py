from moviepy.editor import *
import os
from multiprocessing import Pool

def mp4tomp3(mp4file,mp3file):
    videoclip=VideoFileClip(mp4file)
    audioclip=videoclip.audio
    audioclip.write_audiofile(mp3file)
    audioclip.close()
    videoclip.close()

def mp4tomp3Tuple(path_tuple):
    try:
        mp4file = path_tuple[0]
        mp3file = path_tuple[1]
        clip = AudioFileClip(mp4file)
        clip.write_audiofile(mp3file)
        clip.close()
    except:
        print('----Error---- ',path_tuple)
    #videoclip=VideoFileClip(mp4file)
    #audioclip=videoclip.audio
    #audioclip.write_audiofile(mp3file)
    #audioclip.close()
    #videoclip.close()

if __name__ == '__main__':
    video_ori = '/home/rubens/pythonProjects/NesToMidGeneration/nesmdb_mp4_sliced/'
    mp3_dest = '/home/rubens/pythonProjects/NesToMidGeneration/nesmdb_mp3_from_mp4_sliced/'
    folders_videos = os.listdir(video_ori)
    for folder in folders_videos:
        sub_files_path = os.path.join(video_ori,folder)
        sub_mp3_path = os.path.join(mp3_dest,folder)        
        if not os.path.exists(sub_mp3_path):
            # Create a new directory because it does not exist
            os.makedirs(sub_mp3_path)

            sub_files = os.listdir(sub_files_path)
            p = Pool(24)
            to_map = list()
            for file in sub_files:
                mp4_file = os.path.join(sub_files_path,file)
                mp3_file = os.path.join(sub_mp3_path,file.replace('.mp4','.mp3'))
                #mp4tomp3(mp4_file,mp3_file)
                to_map.append([mp4_file, mp3_file])
            p.map(mp4tomp3Tuple, to_map)
            p.close()
        else:
            print(folder, ' already converted')