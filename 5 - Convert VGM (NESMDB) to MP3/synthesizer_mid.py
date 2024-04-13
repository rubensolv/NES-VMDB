from nesmdb.convert import midi_to_wav
from scipy.io.wavfile import write

with open('/storage1/dados/es91661/rendering_mid/train/001_1942_02_03Restart.mid', 'rb') as f:
  mid = f.read()
# Quantizes MIDI to 100Hz before rendering
# Can set to None to avoid quantization but will take more time/memory
wav = midi_to_wav(mid, midi_to_wav_rate=100)

write("example.wav", 44100, wav)