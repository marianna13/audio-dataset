
from tqdm import tqdm
import librosa
import os
import subprocess
import pandas as pd
import multiprocessing as mp
import time
import sys
import math
import re
import shutil
import zipfile
import random
from split_and_rename import split_dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))



def process_data(meta, output_dir, audio_dir):
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    import numpy as np
    file_id = 0
    for row in tqdm(meta.iterrows(), total=len(meta)):
        t = tables.open_file(h5_path, mode='r')
        metadata = t.root.metadata
        title = metadata.songs.cols.title[0]
        artist = metadata.songs.cols.artist_name[0]
        release = metadata.songs.cols.release[0]
        song_id = metadata.songs.cols.song_id[0]
        analysis = t.root.analysis
        duration = analysis.songs.cols.duration[0]
        audio_md = analysis.songs.cols.audio_md5[0]
        for j in range(0, duration-10, 10):
        original_data = {
                        'title': 'Million Song Dataset',
                        'description':"The Million Song Dataset is a freely-available collection of audio features and metadata for a million contemporary popular music tracks.",
                        'filename':audio_md.decode("utf-8"),
                        'id': str(song_id.decode("utf-8")),
                        'artist': artist.decode("utf-8"),
                        'duration':duration,
                        'release': release.decode("utf-8"),
                        'split':[j, j+10]
                        }
                
        audio_json = {
                        'text': [title.decode("utf-8")], 
                        'tag': [artist.decode("utf-8")], 
                        'original_data':original_data,
                        }

        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path,
            AUDIO_SAVE_SAMPLE_RATE)
        file_id += 1
        if file_id==10:
            break

def process(dataset_name):
    output_dir = f'/home/ubuntu/marianna/clap/processed_datasets/{dataset_name}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'/home/ubuntu/marianna/clap/vocalsketch/AUDIO'
    meta_dir = f'/home/ubuntu/marianna/clap/vocalsketch/vocal_imitations.csv'

    meta = pd.read_csv(meta_dir)
    N = len(meta)

    file_id = 0
    num_process = 20
    processes = []
    out_dirs = [f'{output_dir}/{i} 'for i in range(num_process)]
    for out_dir in out_dirs:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
            for i in range(num_process)]
    print(N, rngs)
    s = time.time()
    for rng, out_dir in zip(rngs, out_dirs):
        start, end = rng
        p = mp.Process(target=process_data, args=[
                       meta.iloc[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
    return output_dir


if __name__ == '__main__':
    from utils.merge_dirs import merge_dirs
    from utils.unzip import unzip_file
    dataset_name = 'million_songs'
    process(dataset_name)