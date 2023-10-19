# -*- coding: utf-8 -*-
"""BlackAdam_deploy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GHpdkBPsUsWlct_DZaucUOsSAZGKhTSO
"""

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

#Alterar aqui
MDB_MP3_PATH = "/content/gdrive/MyDrive/BlackAdam/mp3_database_from_nesmdb/"
MDB_FP_PATH = "/content/gdrive/MyDrive/BlackAdam/nesmd_fingerprints.json/"

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

                    hashes.append(h.hexdigest()[0:20])
    return hashes

"""# Fingerprinting NESmdb"""

mdb_musics = glob.glob(MDB_MP3_PATH + '/*.mp3')

def extract_path_info(dir):
    pattern = re.compile(r'(\d+)_(.+?)_(\d{2}_\d{2}.+\.mp3)$')
    result = {}
    file_name = dir.split("/")[-1]
    if (match := pattern.search(file_name)):
        id_jogo = match.group(1)
        nome_jogo = match.group(2)
        return id_jogo, file_name
    return -1, file_name

finalFile = defaultdict(dict)
for path in tqdm(mdb_musics, desc="Processing musics"):
    try:
        result = {}
        game_id, file_name = extract_path_info(path)

        y, sr = librosa.load(path, sr=44100)
        D = generate_spectrogram(y, sr)
        peaks = find_peaks_by_axis(D)
        fingerprints = generate_fingerprints(peaks)

        if game_id != -1:
            result[file_name] = fingerprints
            finalFile[game_id].update(result)

    except Exception as e:
        print(f"An error occurred: {e}")

json_object = json.dumps(finalFile)
with open(MDB_FP_PATH, 'w') as f:
    f.write(json_object)
del json_object

"""# Matching


"""

def get_youtube_mp3_fingerprints(youtube_mp3_path)
    y, sr = librosa.load(youtube_mp3_path, sr=44100)
    D = generate_spectrogram(y, sr)
    peaks = find_peaks_by_axis(D)
    return generate_fingerprints(peaks)

def match(game_id, youtube_mp3_path, nesmdb_database):
    yt_fp = get_youtube_mp3_fingerprints(youtube_mp3_path)
    max = 0
    current_match = ''
    nesmdb_available = nesmdb_database[game_id]
    for mdb_music, mdb_fp in nesmdb_available.items():
        intersection_size = len(set(mdb_fp).intersection(set(yt_fp)))
        if intersection_size > max:
            max = intersection_size
            current_match = mdb_music
    return current_match







