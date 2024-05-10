
# The NES Video-Music Database
The NES Video-Music Database (NES-MVDB) is a dataset of 98,940 short (15 seconds) gameplay videos from 386 NES games, each paired with its original music piece in symbolic format (MIDI). NES-MVDB is built upon the Nintendo Entertainment System Music Database [(NES-MDB)](https://github.com/chrisdonahue/nesmdb#dataset-information). 

- [Dataset on Google Drive](https://drive.google.com/drive/folders/1H9LaoBqB-6-DUpXte0-DRKa8ko2cJOjv?usp=sharing)
- [Paper on arXiv](https://arxiv.org/abs/2404.04420)

# Dataset structure
The dataset is organized into 4 directories:
- **Midi**: all the original midi files from NES-MDB.
- **Audio**: all the original midi files from NES-MDB synthesized as MP3 with the original NES synth.
- **Videos**: all gameplay videos in the dataset, organized by game id, and sliced in fragments of 15 seconds
- **Video-Midi**: a csv file with the game id, name, and metadata of each game in the dataset.

The mapping csv file has the following structure:

![alt text](https://github.com/rubensolv/NES-VMDB/blob/main/images/mapping_csv_structure.png)
 
- `sliced query`:  contains the sliced fragment of the gameplay video extracted previously from YouTube. 
- `midi suggested`: file is related to the suggested music from NES-MDB which [Dejavu](https://github.com/worldveil/dejavu) (Shazam algorithm-based) did the match.
- `sliced query` and `sliced query` are confidence values related to the Dejavu score. Great values mean better confidence between the sliced query fragment and the midi suggested. 

<!--# Generating the database (Under construction)
A summary to generate the database in eight steps:
<ol>
 <li> We found and matched the gameplays on Youtube for each game existing in NES-MDB, generating the file nesvmdb_csv_youtube.csv. Code and data at folder 1 - YouTube vs mid files.</li>
 <li> Using the csv, we download each Youtube video in mp4 format. The code to perform the download is placed in folder 2 - Downloading Youtube Videos.</li>
 <li> After downloading all the videos, we sliced every gameplay in files of 15 seconds. The code to perform this process is placed at 3 - Slicing Youtube Videos.</li>
 <li> Using the slices generated from the previous step, we extracted the respective mp3 audio files from every slice. The code for this process can be found in folder 4 - Extracting MP3 from slices. You can download the extracted mp3 and mp4 files at this link https://drive.google.com/drive/folders/1SS-AfMczVaef56L9zsxaJJsr28eiHosW?usp=sharing </li>
 <li> At this point, Dejavu needs all the files (to build up the library and to find the matches) as mp3 files. So, we convert all the mid/vgm files on NES-MDB to MP3. Code can be found in folder 5 - Convert VGM (NESMDB) to mp3. You can download the NES-MDB mp3 files here https://drive.google.com/drive/folders/1UMrehR6_JNEHfNmTKI1HCPZxLJzuLKhh?usp=sharing. </li>
 <li> After all the previous steps, we have the required files to perform the match. Following the steps in https://github.com/worldveil/dejavu, you can install Dejavu. </li>
 <li> Copying the files on folder 6 - Install Dejavu, to your current Dejavu installation, you can start the matching process between the mp3's and mp4's slice and the NES-MDB mp3 files. If you want, you can download the full Dejavu folder with contents at this link https://drive.google.com/file/d/18W7_kIZIWuLfv6zQXErMAWmylisDA4T4/view?usp=sharing. </li>
 <li> The previous step produces the dataset save on folder 7 - Dataset Mapping/mapping_game. </li>
</ol>-->

## Citing this Dataset

This dataset was presented in the paper [The NES Video-Music Database: A Dataset of Symbolic Video Game Music Paired with Gameplay Videos](https://arxiv.org/abs/2404.04420), so if you use the dataset, please cite:

```
@article{cardoso2024nes,
  title={The NES Video-Music Database: A Dataset of Symbolic Video Game Music Paired with Gameplay Videos},
  author={Cardoso, Igor and Moraes, Rubens O and Ferreira, Lucas N},
  journal={arXiv preprint arXiv:2404.04420},
  year={2024}
}
```
