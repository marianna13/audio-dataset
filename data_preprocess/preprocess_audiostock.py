
from tqdm import tqdm
import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if __name__ == '__main__':
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    dataset_name = 'audiostock'
    data_dir = f'/mnt/marianna/clap/raw_datasets/{dataset_name}'
    output_dir = f'/mnt/marianna/clap/processed_datasets/{dataset_name}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'{data_dir}/audio'
    meta_dir = f'/mnt/marianna/clap/raw_datasets/audiostock/meta/meta.csv'

    meta = pd.read_csv(meta_dir)
    filenames, texts = meta['fname'].values, meta['text'].values
    file_id = 0
    for filename, text in tqdm(zip(filenames, texts), total=len(filenames)):
        audio_path = f'{audio_dir}/{filename}'
        audio_json = {'text': text, 'tag': 'audiostock'}
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        print(audio_save_path, audio_path)
        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path, AUDIO_SAVE_SAMPLE_RATE)
        file_id += 1
