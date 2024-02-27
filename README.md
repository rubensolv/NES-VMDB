# The NES Video-Music Database
FDG 2024 NES project.

# Relevant links

Nes longplay videos (library)
https://www.youtube.com/watch?v=ezydTKjg_nE&list=PL3gSj_kh1fHtxy0_CDUwa6UPCO3PSf87-

Github nes-mid dataset 
https://github.com/chrisdonahue/nesmdb#dataset-information

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
