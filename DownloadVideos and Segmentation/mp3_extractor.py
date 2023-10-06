import os
import argparse
import librosa
import numpy as np
# from pydub import AudioSegment
from pydub import AudioSegment, silence

# Function to detect song transitions based on silence segments
def detect_transitions(audio_stream, min_silence_duration=1):
    myaudio = AudioSegment.from_mp3(audio_stream)
    dBFS=myaudio.dBFS
    transitions = silence.detect_nonsilent(myaudio, min_silence_len=min_silence_duration*1000, silence_thresh=dBFS-16)
    print(transitions)
    return transitions

def save_timestamps(transitions, output_dir="output/"):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Define output filename
    output_file = os.path.join(output_dir, "transitions.txt")

    # Convert transition from samples to seconds
    transition_in_secs = [((start/1000),(stop/1000)) for start,stop in transitions] #in sec
    
    with open(output_file, "a") as myfile:
        for t in transition_in_secs:
            start_time, end_time = t
            myfile.write(f"{start_time} {end_time}\n")

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
        print(f"Segment {i + 1} saved as {output_file}")

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Detect song transitions based on silent segments and split the audio file.")
    
    # Add a positional argument for the input audio stream file
    parser.add_argument("audio_stream", help="Path to the input audio stream file (e.g., a WAV file).")
    
    # Add optional arguments for silence threshold and min silence duration
    parser.add_argument("--min_silence_duration", type=int, default=1,
                        help="Minimum duration of silence (in seconds) to be considered a transition (default: 2).")
    
    # Add an optional argument for the output directory
    parser.add_argument("--output_dir", default="output/",
                        help="Directory to save the split audio segments (default: 'output/').")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Detect song transitions
    transitions = detect_transitions(args.audio_stream, args.min_silence_duration)
    
    for transition_duration in transitions:
        print(f"{transition_duration} seconds")
    
    # Split audio at detected transitions and save segments
    split_audio_at_transitions(args.audio_stream, transitions, args.output_dir)

    # Save transitions in a txt file
    save_timestamps(transitions)