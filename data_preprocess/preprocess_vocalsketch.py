
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
import soundfile as sf
from split_and_rename import split_dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))



def process_data(meta, output_dir, audio_dir):
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    import numpy as np
    file_id = 0
    for row in tqdm(meta.iterrows(), total=len(meta)):
        (id,filename,stimulus_type,included,draft,training,participant_id,
        satisfaction,sound_label,sound_label_id,sound_recording,sound_recording_id,
        audio_concept_subset,description,
        participants_sound_recording_description_confidence,description_match)= row[1].values
        audio_path = audio_dir+'/'+filename
        try:    
            sf.read(audio_path)
        except:
            continue
        if type(description)==float:
            continue
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                    'default=noprint_wrappers=1:nokey=1', audio_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
        duration = str(result.stdout)[2:-3]
        text = filename.split(' -')[0]
        text = f'playing a vocal imitation of {description}'
        caption = [text]
        original_data = {
                'title': 'VocalSketch Data Set 1.1.2',
                'description':"This dataset contains thousands of vocal imitations of a large set of diverse sounds. These imitations were collected from hundreds of contributors via Amazon's Mechanical Turk website.",
                'license':'',
                'filename':filename,
                'id': str(id),
                'stimulus_type': stimulus_type,
                'duration':duration,
                'included': included,
                'draft': draft,
                'sound_label': str(sound_label),
                'sound_label_id':str(sound_label_id),
                'sound_recording':str(sound_recording),
                'recording_description':description
                }
        audio_json = {
                'text': caption, 
                'tag': [description], 
                'original_data':original_data,
                }

        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path,
            AUDIO_SAVE_SAMPLE_RATE)
        file_id += 1

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
    dataset_name = 'VocalSketch'
    process(dataset_name)
