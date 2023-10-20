import argparse
import json
import sys
from argparse import RawTextHelpFormatter
from os.path import isdir
import os

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

DEFAULT_CONFIG_FILE = "dejavu.cnf.SAMPLE"


def init(configpath):
    """
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print(f"Cannot open configuration: {str(err)}. Exiting")
        sys.exit(1)

    # create a Dejavu instance
    return Dejavu(config)


if __name__ == '__main__':
    config_file = DEFAULT_CONFIG_FILE
    djv = init(config_file)
    print("Total of Fingers: ", djv.db.get_num_fingerprints())
    djv.fingerprint_directory('/home/rubens/pythonProjects/dejavu/base036/', [".mp3" ], 20)
    print("Total of Fingers: ", djv.db.get_num_fingerprints())
    # Recognize audio from a file
    for file in os.listdir('036/')[0:10]:
        print('Evaluating file ', file)
        results = djv.recognize(FileRecognizer, "/home/rubens/pythonProjects/dejavu/036/"+file)
        print(f"From file we recognized: {results}\n")
    
