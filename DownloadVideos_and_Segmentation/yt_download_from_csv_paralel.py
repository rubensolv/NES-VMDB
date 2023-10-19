import os
import argparse
import re
from difflib import SequenceMatcher
from thefuzz import fuzz

from pytube import YouTube
import csv
from multiprocessing import Pool

def download_video(row):
    name_file = 'nesmdb_mp4/'+str(row[0])+'.mp4'      
    if os.path.isfile(name_file):
        print(name_file, ' already downloaded!')
    elif len(row[2])==0:
        print(name_file, ' No link!')
    else:
        print(name_file)
        try:
            streams = YouTube(row[2]).streams.get_by_resolution('240p')        
            if streams is not None:
                streams.download(filename=name_file, max_retries=3)                    
            else:
                YouTube(row[2]).streams.get_lowest_resolution().download(filename=name_file, max_retries=3)
            print('--done  ',name_file) 
        except:
            print('----## error ##  ',name_file) 
            
if __name__ == '__main__':    
    
    rows = list()
    with open('nesmdb_csv_youtube.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:                           
                rows.append(row)
                line_count += 1            
    print(f'Processed {line_count} lines.')                    
    pool = Pool(processes=20)
    pool.map(download_video,rows)
    pool.close()    
        
