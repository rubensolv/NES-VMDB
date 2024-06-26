import argparse
import json
import sys
from argparse import RawTextHelpFormatter
from os.path import isdir
import os

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

import shutil
import mysql.connector
import psycopg2
import csv

#DEFAULT_CONFIG_FILE = "dejavu.cnf.SAMPLE"
DEFAULT_CONFIG_FILE = "dejavu.cnf.post.SAMPLE"


def init(configpath):
    """
    Load config from a JSON file
    connection = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=host,
        port=port
)
    """
    try:
        with open(configpath) as f:
            config = json.load(f)

            connection = psycopg2.connect(
                host=config['database']["host"],
                port=config['database']["port"],
                user=config['database']["user"],
                password=config['database']["password"],
                dbname=config['database']["database"]
            )

            mycursor = connection.cursor()

            mycursor.execute("CREATE DATABASE "+config['database']["database"]+";")
            mycursor.close()
    except IOError as err:
        print(f"Cannot open configuration: {str(err)}. Exiting") 
    except:
        print('Continuing....')       

    # create a Dejavu instance
    return Dejavu(config)

def get_list_done():
    path_list = '/home/dpiubuntu/Documents/dejavu/mapping_game/'
    text_itens = []
    for f in os.listdir(path_list):
        frags = f.split('_')
        text_itens.append(frags[2].replace('.csv',''))
    to_int = list()
    for i in text_itens:
        to_int.append(int(i))
    return to_int
    

def get_games_id(min, max):
    games_id = dict()
    for f in os.listdir('nesmdb_mid_audio/'):
        value = int(f[0:3])
        if value >= min and value <= max:
            if value not in get_list_done():
                DIR = os.path.join('nesmd_mid_audio_sliced/',f[0:3])
                total = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
                if total in games_id:
                    lst = games_id[total]
                    lst.add(f[0:3])
                    games_id[total] = lst
                else:
                    item = set()
                    item.add(f[0:3])
                    games_id[total] = item
            
    return games_id

def organize_mids_by_id(game_id):
    for f in os.listdir('nesmdb_mid_audio/'):
        if game_id == f[0:3]:
            previous_path = os.path.join('nesmd_mid_audio_sliced/',f[0:3]) 
            if not os.path.isdir(previous_path):
                os.mkdir(previous_path)
            shutil.copyfile(os.path.join('nesmdb_mid_audio/',f),os.path.join('nesmd_mid_audio_sliced/',f[0:3],f) )

def cleaning_db(configpath, djv):    
    to_delete = list()
    for song in djv.get_fingerprinted_songs():
        to_delete.append(song['song_id'])
    djv.delete_songs_by_id(to_delete)   
    djv = init(config_file)
    print("Total of Fingers after Cleaning (validating log): ", djv.db.get_num_fingerprints())
    return djv

if __name__ == '__main__':
     # Parse arguments
    parser = argparse.ArgumentParser(description='dejavu.py')
    parser.add_argument('--begin', type=int, default='200')
    parser.add_argument('--end', type=int, default='400')
    parser.add_argument('--config_file', type=str, default="dejavu.cnf.post.SAMPLE")
    args = parser.parse_args()

    # Sort in folders the mp's midis. 
    # games_id = get_games_id()
    # for game in games_id:
    #     organize_mids_by_id(game)

    #cleaning DB
    config_file = args.config_file
    print(config_file)
    djv = init(config_file)    
    #print("Total of Fingers: ", djv.db.get_num_fingerprints())
    djv = cleaning_db(config_file, djv)
    #print("Total of Fingers: ", djv.db.get_num_fingerprints())
    #Finishing
    games_id = get_games_id(args.begin, args.end)
    for game_key in sorted(games_id.keys()):
        for game in games_id[game_key]:
            print("Generating fingers to ", game)
            path_fingers = os.path.join('nesmd_mid_audio_sliced/',game)
            djv.fingerprint_directory(path_fingers, [".mp3" ], 20)
            print("Total of Fingers: ", djv.db.get_num_fingerprints())
            # Recognize audio from a file
            path_slices = os.path.join('nesmdb_mp3_from_mp4_sliced/',game)
            if os.path.isdir(path_slices):
                print("### Game id  ", game)
                print("sliced_query,midi_suggested,input_confidence,fingerprinted_confidence")
                path_mapping_log = 'mapping_game/Game_id_'+game+'.csv'
                with open(path_mapping_log, 'w', encoding='UTF8') as f:            
                    f.write("sliced_query,midi_suggested,input_confidence,fingerprinted_confidence\n")
                for file in os.listdir(path_slices):
                    if '.mp3' in file:                
                        #print('Evaluating file ', file)
                        path_file = os.path.join(path_slices,file)
                        try:
                            results = djv.recognize(FileRecognizer, path_file)
                        except:
                            print("----Problem ",path_file)
                        #print(f"From file we recognized: {results}\n")
                        try:
                            result = results['results'][0]
                            print(file+','+result['song_name'].decode('utf-8')+','+
                                str(result['input_confidence'])+','+str(result['fingerprinted_confidence']) )    
                            with open(path_mapping_log, 'a', encoding='UTF8') as f:
                                f.write(file+','+result['song_name'].decode('utf-8')+','+
                                    str(result['input_confidence'])+','+str(result['fingerprinted_confidence'])+'\n')
                        except:
                            print('@@@ error @@@ Evaluating file ', file)                                
                            print(f"From file we recognized: {results}\n")
                else:
                    print("Game id", game, " has no slices")
            djv = cleaning_db(config_file, djv)
        
