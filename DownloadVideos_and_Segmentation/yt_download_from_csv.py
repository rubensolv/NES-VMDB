import os
import argparse
import re
from difflib import SequenceMatcher
from thefuzz import fuzz

from pytube import YouTube
import csv

def download_video(row):
    name_file = 'nesmdb_mp4/'+row[0]+'.mp4'      
    streams = YouTube(row[2]).streams.get_by_resolution('240p')
    if streams is not None:
        streams.download(filename=name_file, max_retries=3)                    
    else:
        YouTube(row[2]).streams.get_lowest_resolution().download(filename=name_file, max_retries=3)
        
if __name__ == '__main__':            
    with open('nesmdb_csv_youtube.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:           
                download_video(row=row)
                line_count += 1                
        print(f'Processed {line_count} lines.')