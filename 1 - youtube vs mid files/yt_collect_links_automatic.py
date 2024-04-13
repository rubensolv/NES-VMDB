import os
import argparse
import re
from difflib import SequenceMatcher
from thefuzz import fuzz

from pytube import Playlist

from youtubesearchpython import VideosSearch

import csv

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
            id_frag_name = file[0:3]
            frag_name = file[4:data.span()[0]]
            frag_name = frag_name.replace("_", " ")
            frag_name = break_at_capital(frag_name)
            frag_name = include_joint(frag_name)
            #print(frag_name)  
            games.add(tuple((id_frag_name, frag_name)))      
    return games   

def search_youtube(query):
    videosSearch = VideosSearch(query, limit = 3)
    results = videosSearch.result()
    # print(query)
    # for r in results['result']:
    #   print(r)
    if 'result' in results and len(results['result']) > 0:
        first_video = results['result'][0]
        video_url = first_video['link']
        video_channel = first_video['channel']['name']
        return video_url, video_channel
    return None, None

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='clean.py')    
    parser.add_argument('--mids', type=str, default='nesmdb_midi/all/')
    args = parser.parse_args()
    
    #get the games titles based on the mids we have
    games_titles = get_game_titles(args.mids)
    with open('nesvmdb_csv_youtube.csv', 'w', newline='') as csvfile:
        nesmdb_csv_youtube = csv.writer(csvfile)
        nesmdb_csv_youtube.writerow(['game_id', 'game_name', 'game_url', 'game_channel'])
        for i in games_titles:        
            video_url, video_channel = search_youtube(i[1] + " NES World of Longplay"  )
            print(i[0], ',', i[1] , ',', video_url, ',', video_channel)
            nesmdb_csv_youtube.writerow([i[0], i[1], video_url, video_channel])
            csvfile.flush()
