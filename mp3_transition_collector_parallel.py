import os
import argparse
import numpy as np
# from pydub import AudioSegment
from pydub import AudioSegment, silence
from multiprocessing import Process, Pool

# Function to detect song transitions based on silence segments
def detect_transitions(audio_stream, min_silence_duration=1):
    myaudio = AudioSegment.from_mp3(audio_stream)
    dBFS=myaudio.dBFS
    transitions = silence.detect_nonsilent(myaudio, min_silence_len=min_silence_duration*1000, silence_thresh=dBFS-16)
    print(audio_stream)
    return transitions

def save_timestamps(transitions, output_dir, file_name):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Define output filename
    output_file = os.path.join(output_dir, file_name+".txt")

    # Convert transition from samples to seconds
    transition_in_secs = [((start/1000),(stop/1000)) for start,stop in transitions] #in sec
    
    with open(output_file, "a") as myfile:
        for t in transition_in_secs:
            start_time, end_time = t
            myfile.write(f"{start_time} {end_time}\n")

def run(audio_stream):
    output_dir = '/home/rubens/pythonProjects/NesToMidGeneration/data/list_transitions/'
    min_silence_duration = 1
    # Detect song transitions
    transitions = detect_transitions(audio_stream, min_silence_duration)
    
    # Save transitions in a txt file
    file_name = os.path.basename(audio_stream)
    name = os.path.splitext(file_name)[0]
    save_timestamps(transitions,output_dir, name)

def check_file_converted(file,output_dir):
    file = file.replace('.mp3','.txt')
    return os.path.isfile(os.path.join(output_dir,file))

if __name__ == "__main__":
    concurrency = 2
    myPathIn = '/home/rubens/pythonProjects/NesToMidGeneration/data/full_mp3_from_mp4/'
    musics = []    
    total = 0
    for file in os.listdir(myPathIn):
        if not check_file_converted(file,'/home/rubens/pythonProjects/NesToMidGeneration/data/list_transitions/'):
            print(file)
            musics.append(os.path.join(myPathIn, file))
    
    pool = Pool(processes=concurrency)
    pool.map(run,musics)
    pool.close()
        