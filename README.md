# The NES Video-Music Database
Paper on [FDG 2024](https://www.fdg.org.br/) named The NES Music-Video Database: A Dataset of Symbolic Video Game Music
Paired with Gameplay Videos.


We introduce a novel dataset named NES-MVDB, comprising 98,940 gameplay videos from 386 NES games, each paired with its original music piece in symbolic format (MIDI). NES-MVDB is built upon the Nintendo Entertainment System Music Database (NES-MDB), encompassing 5,278 music pieces from the soundtracks of 397 NES games. Our approach involves collecting long-play videos for 386 games in the original dataset, slicing them into 15-second-long clips, and extracting the audio from each clip. Subsequently, we apply an audio fingerprinting algorithm (similar to Shazam) to automatically identify the corresponding piece in the [NES-MDB](https://github.com/chrisdonahue/nesmdb#dataset-information) dataset.  Additionally to the dataset, we introduce a baseline method based on the [Controllable Music Transformer](https://github.com/cardoso-data-science/nesmvdb-bl) to generate NES music conditioned on gameplay clips. We evaluated this approach with objective metrics, and the results showed that the conditional CMT improves musical structural quality when compared to its unconditional counterpart. Moreover, we used a neural classifier to predict the game genre of the generated pieces. Results showed that they matched the genre of their gameplay clips as accurately as the human pieces.



# Dataset Information
The dataset can be found in the folder [7-Dataset Mapping]([https://github.com/cardoso-data-science/nesmvdb-bl](https://github.com/rubensolv/NES-VMDB/tree/main/7%20-%20Dataset%20Mapping/mapping_game)) and it is named with the ID of each game listed in the csv file [nesvmdb_csv_youtube](https://github.com/rubensolv/NES-VMDB/blob/main/1%20-%20youtube%20vs%20mid%20files/nesvmdb_csv_youtube.csv). 
In summary, each file is named as Game_id_*gameID*.csv. The mapping csv file has the following structure:
![alt text](https://github.com/rubensolv/NES-VMDB/blob/main/images/mapping_csv_structure.png)
 
The column sliced query contains the sliced fragment of the gameplay video extracted previously from YouTube. The column midi suggested file is related to the suggested music from NES-MDB which [Dejavu](https://github.com/worldveil/dejavu) (Shazam algorithm-based) did the match. The following columns are confidence values related to the Dejavu score. Great values mean better confidence between the sliced query fragment and the midi suggested. 


# Generating the database
To generate the database we performed six steps:
<ol>
 <li> We found and matched the gameplays on Youtube for each game existing in NES-MDB, generating the file nesvmdb_csv_youtube.csv. Code and data at folder 1 - YouTube vs mid files </li>
 <li> Using the csv, we download each Youtube video in mp4 format. The code to perform the download is placed in folder 2 - Downloading Youtube Videos</li>
 <li> After downloading all the videos, we sliced every gameplay in files of 15 seconds. The code to perform this process is placed at 3 - Slicing Youtube Videos </li>
 <li> </li>
</ol>
# Relevant links

Nes longplay videos (library)
https://www.youtube.com/watch?v=ezydTKjg_nE&list=PL3gSj_kh1fHtxy0_CDUwa6UPCO3PSf87-

# Commands
python3 -m venv venv

pip install --update pip

pip install -r requirements.txt

python3 mp3_transitions_collector_parallel.py

python3 segment_video_sec_parallel.py

# current pipeline

Extrair os mp3 dos videos que estao na pasta youtube_mp4_full usando o ffmpeg; for i in *.mp4; do ffmpeg -i "$i" -vn -ac 1 -f mp3 "${i%.*}".mp3; done

Gerar as transicoes (cut_points) para serem utilizadas para cortar o video usando as classes https://github.com/rubensolv/NesToMidGeneration/blob/main/mp3_transition_collector_parallel.py ou https://github.com/rubensolv/NesToMidGeneration/blob/main/mp3_transition_collector_class.py

Copiar os arquivos gerados (transicoes ou cut_points) e utilizar a classe https://github.com/rubensolv/NesToMidGeneration/blob/main/segment_video_sec_parallel.py para, dado o txt das transicoes, realizar a segmentacao do MP4.
