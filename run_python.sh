#!/bin/bash

#PBS -N Segmentation
#PBS -l nodes=1:ppn=8,mem=10gb,walltime=24:00:00
#PBS -q qtime

cd /storage1/dados/es91661/NesToMidGeneration

source /etc/profile.d/modules.sh

module load python/3.10.13

source /storage1/dados/es91661/NesToMidGeneration/venv/bin/activate

python segment_video_sec_parallel.py



