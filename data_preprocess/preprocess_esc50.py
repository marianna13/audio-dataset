
from tqdm import tqdm
import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if __name__ == '__main__':
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    dataset_name = 'ESC-50-master'
    data_dir = f'/mnt/marianna/clap/raw_datasets/{dataset_name}'
    output_dir = f'/mnt/marianna/clap/processed_datasets/{dataset_name}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'{data_dir}/audio'
    meta_dir = f'{data_dir}/meta/esc50.csv'

    meta = pd.read_csv(meta_dir)
    file_id = 0
    for row in tqdm(meta.iterrows(), total=len(meta)):
        filename, fold, target, category, esc10, src_file, take = row[1].values
        audio_path = f'{audio_dir}/{filename}'
        category = category.replace('_', ' ')
        text = f'The sound of the {category}'
        tag = category
        original_data = {
            'title': 'ESC-50',
            'Description': 'ESC-50: Dataset for Environmental Sound Classification',
            'license': 'Creative Commons Attribution Non-Commercial license',
            'fname': filename,
            'fold': fold,
            'target': target,
            'category': category,
            'esc10': esc10,
            'src_file': src_file,
            'take': take
        }
        audio_json = {'text': text, 'tag': tag,
                      'original_data': original_data}
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path, AUDIO_SAVE_SAMPLE_RATE)
        file_id += 1
