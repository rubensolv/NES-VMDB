from nesmdb.convert import vgm_to_wav
from scipy.io.wavfile import write
import os

#Collect all the scenes files
path_vgm= '/storage1/dados/es91661/rendering_mid/train_vgm/'
vgms = os.listdir(path_vgm)    
for vgm_name in vgms:   
  print(vgm_name)
  with open(os.path.join(path_vgm,vgm_name), 'rb') as f:
    vgm = f.read()

  wav = vgm_to_wav(vgm)
  to_save = '/storage1/dados/es91661/rendering_mid/waves_files/'+vgm_name.replace('.vgm','')+'.wav'
  print(to_save)
  write(to_save, 44100, wav)