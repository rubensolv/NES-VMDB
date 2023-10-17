import os
import argparse
import re
from difflib import SequenceMatcher
from thefuzz import fuzz

from pytube import Playlist

def break_at_capital(name):
    final_name = ''
    for l in name:
        if l.isupper() and l not in['I','V']:
            final_name += ' '+l
        else:
            final_name += l
    return final_name.strip()

def include_joint(name):
    final_name = ''
    frags = name.split(" ")
    for i in range(len(frags)):
        if len(frags[i])==1:
            final_name = final_name.strip()
            final_name += '\''+frags[i]+' '
        else:
            final_name += frags[i]+' '
    return final_name.strip()

def get_game_titles(folder_mids):
    games = set()
    for file in os.listdir(folder_mids):
        if file.endswith(".mid"): 
            pattern = r'_[\d\d]\w_'
            data = re.search(pattern, file)    
            frag_name = file[4:data.span()[0]]
            frag_name = frag_name.replace("_", " ")
            frag_name = break_at_capital(frag_name)
            frag_name = include_joint(frag_name)
            #print(frag_name)  
            games.add(frag_name)      
    return games   

def similar(name, list_games):
    name = name.replace('(NES) Playthrough - NintendoComplete','').replace('(NES) Playthrough','').strip()
    score = 0.0
    score_fuzzy = 0.0
    for game in list_games:        
        calc = SequenceMatcher(None, game, name).ratio()         
        calc2 = fuzz.partial_ratio(name,game)     
        if calc > score:
            score = calc
            score_fuzzy = calc2
            # print(name,game, str(score))
            # print(name,game, str(score_fuzzy))
    return score, score_fuzzy

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='clean.py')
    parser.add_argument('--url', type=str, default='https://www.youtube.com/watch?v=ezydTKjg_nE&list=PL3gSj_kh1fHtxy0_CDUwa6UPCO3PSf87-')
    #parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--out', type=str, default='/home/rubens/pythonProjects/NesToMidGeneration/data/yt_nes_mp4/')
    #parser.add_argument('--out', type=str, default='smb://200.235.131.33/youtube_mp4_full/')
    parser.add_argument('--mids', type=str, default='/home/rubens/pythonProjects/NesToMidGeneration/data/nesmdb_midi/train/')
    args = parser.parse_args()
    
    #get the games titles based on the mids we have
    games_titles = get_game_titles(args.mids)

    p = Playlist(args.url)    
    print(f'Playlist Name: {p.title}')
    for i, video in enumerate(p.videos):
        #score, score_fuzzy = similar(video.title, games_titles)
        if True:
        # if score > 0.7 and score_fuzzy > 80:        
            try:
                video_title = video.title
            except:
                video_title = '%03d' % i + "_video"
            try:
                video_title = video_title.replace('/', '_')
                video_title += '.mp4'            
                video_title = os.path.join(args.out, video_title)

                if (not os.path.exists(video_title)) and (not os.path.exists(video_title.replace('.mp4','.mp3'))):
                    try:
                        streams = video.streams.filter(file_extension='mp4')

                        if len(streams) > 0:
                            print(f'Downloading video: {video_title}')
                            streams[0].download(filename=video_title, max_retries=3)
                        else:
                            print("No streams found!")
                    except KeyError:
                        print('No streams found')
                else:
                    print(f'{video_title} already downloaded')
            except: 
                print(f'{video_title} already downloaded')