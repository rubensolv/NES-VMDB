import os
import argparse
import numpy as np
# from pydub import AudioSegment
from pydub import AudioSegment, silence
from multiprocessing import Process
from multiprocessing import Semaphore

class Mp3_detector():
    
    def __init__(self, path_file_in, dir_out, min_silence=1):
        self.audio_stream = path_file_in
        self.output_dir = dir_out
        self.min_silence_duration  = min_silence
        file_name = os.path.basename(path_file_in)
        self.name = os.path.splitext(file_name)[0]
    
        # Function to detect song transitions based on silence segments
    def detect_transitions(self):
        myaudio = AudioSegment.from_mp3(self.audio_stream)
        dBFS=myaudio.dBFS
        transitions = silence.detect_nonsilent(myaudio, min_silence_len=self.min_silence_duration*1000, silence_thresh=dBFS-16)
        #print(transitions)
        return transitions

    def save_timestamps(self,transitions, output_dir="output/"):
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Define output filename
        output_file = os.path.join(output_dir, str(self.name)+".txt")

        # Convert transition from samples to seconds
        transition_in_secs = [((start/1000),(stop/1000)) for start,stop in transitions] #in sec
        
        with open(output_file, "a") as myfile:
            for t in transition_in_secs:
                start_time, end_time = t
                myfile.write(f"{start_time} {end_time}\n")
        return output_file

    # Function to split audio at detected transitions
    def split_audio_at_transitions(audio_stream, transitions, output_dir="output/"):
        # Load the audio stream
        audio = AudioSegment.from_file(audio_stream)
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Split the audio at detected transitions
        for i, transition_duration in enumerate(transitions):
            start_time, end_time = transition_duration
            segment = audio[start_time:end_time]
            
            # Save the segment as a separate audio file
            output_file = os.path.join(output_dir, f"segment_{i + 1}.mp3")
            segment.export(output_file, format="mp3")
            #print(f"Segment {i + 1} saved as {output_file}")
    
    def run(self):
        # Detect song transitions
        transitions = self.detect_transitions()
        
        # for transition_duration in transitions:
        #     print(f"{transition_duration} seconds")
        
        # # Split audio at detected transitions and save segments
        # self.split_audio_at_transitions(self.audio_stream, transitions, self.output_dir)

        # Save transitions in a txt file
        return self.save_timestamps(transitions, self.output_dir)


if __name__ == "__main__":
    concurrency = 7    
    myPathIn = '/home/rubens/pythonProjects/NesToMidGeneration/data/teste_dead/'
    myPathOut = '/home/rubens/pythonProjects/NesToMidGeneration/data/teste_dead_list_transitions/'
    
    total = 0
    for file in os.listdir(myPathIn):
        print('Starting file....'+file)
        d = Mp3_detector(os.path.join(myPathIn, file), myPathOut, min_silence=3)
        d.run()    
        total+=1        
        print('Processing....'+str(total))
        
        