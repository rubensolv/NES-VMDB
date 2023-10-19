

# General libraries
import glob
import json
import math
import os
from tqdm import tqdm
import hashlib
from operator import itemgetter
# Data manipulation libraries
import numpy as np
import scipy.signal
from collections import defaultdict
import re
# Audio processing libraries
import librosa
# Multiprocessing libraries
from multiprocessing import Pool



"""# Spectrogram"""
def generate_spectrogram(y, sr, n_fft=4096,):
    D = np.abs(librosa.stft(y, n_fft=n_fft,))

    return D

"""# Peaks"""

def find_peaks(data, axis, distance, height):
    x, y = [], []
    for index in range(data.shape[axis]):
        if axis == 0:
            peaks = scipy.signal.find_peaks(data[index], distance=distance, prominence=0)[0]
            x.extend([index] * len(peaks))
            y.extend(peaks)
        else:
            peaks = scipy.signal.find_peaks(data[:, index], distance=distance, prominence=0)[0]
            x.extend(peaks)
            y.extend([index] * len(peaks))
    return set(zip(x, y))

# Find peaks along frequency and time axis
def find_peaks_by_axis(Y, distance=10, height=20):
    output_freq = find_peaks(Y, axis=0, distance=200, height=height)
    output_time = find_peaks(Y, axis=1, distance=1, height=height)

    # Compute intersection
    output = output_freq.intersection(output_time)
    return list(output)

"""# Fingerprints"""

def generate_fingerprints(peaks, fan_value=10):
    idx_freq = 0
    idx_time = 1
    hashes = []
    peaks.sort(key=itemgetter(1))
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):
                freq1 = peaks[i][idx_freq]
                freq2 = peaks[i + j][idx_freq]
                t1 = peaks[i][idx_time]
                t2 = peaks[i + j][idx_time]
                t_delta = t2 - t1

                if 1 <= t_delta <= 10:
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))

                    hashes.append(h.hexdigest()[0:30])
    return hashes

def get_youtube_mp3_fingerprints(youtube_mp3_path):
    y, sr = librosa.load(youtube_mp3_path, sr=44100)
    D = generate_spectrogram(y, sr)
    peaks = find_peaks_by_axis(D)
    return generate_fingerprints(peaks)

def match(game_id, youtube_mp3_path, nesmdb_database):
    yt_fp = get_youtube_mp3_fingerprints(youtube_mp3_path)
    max = 0
    current_match = 'not found'
    nesmdb_available = nesmdb_database[game_id]
    for mdb_music, mdb_fp in nesmdb_available.items():
        intersection_size = len(set(mdb_fp).intersection(set(yt_fp)))
        if intersection_size > max:
            max = intersection_size
            current_match = mdb_music
    return current_match

if __name__ == '__main__':
    #Alterar aqui
    MDB_FP_PATH = "nesmdb_fingerprints_pt1.json"
    with open(MDB_FP_PATH, 'r') as f:
        nesmdb_database = json.loads(f.read())

        #testing method
        path_mp3_youtube = '/home/rubens/pythonProjects/NesToMidGeneration/nesmdb_mp3_from_mp4_sliced/325/'
        for file_name in os.listdir(path_mp3_youtube):
            game_id = file_name.split('_')[0]
            result = match(str(game_id), os.path.join(path_mp3_youtube,file_name), nesmdb_database=nesmdb_database)
            print('segment_mp3=',file_name,' music_suggested=',',',result)
        
    #all pool code here
    # pool = Pool(processes=20)
    # pool.map(download_video,rows)
    # pool.close() 
