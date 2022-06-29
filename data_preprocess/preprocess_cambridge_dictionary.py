from tqdm import tqdm
import os
import pandas as pd
import multiprocessing as mp
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

present_fn = os.listdir(
    '/mnt/marianna/clap/raw_datasets/cambridge_dictionary/audio')


if __name__ == '__main__':
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    dataset_name = 'cambridge_dictionary'
    data_dir = f'/mnt/marianna/clap/raw_datasets/{dataset_name}'
    output_dir = f'/mnt/marianna/clap/processed_datasets/{dataset_name}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'{data_dir}/audio_us'
    meta_dir = f'/mnt/marianna/clap/raw_datasets/cambridge_dictionary/meta/text_audio_urls.csv'

    meta = pd.read_csv(meta_dir)
    filenames, texts = meta['us_audio_url'].values, meta['word'].values

    file_id = int(len(os.listdir(output_dir))/2)
    print(file_id)
    for filename, text in tqdm(zip(filenames, texts), total=len(filenames)):
        filename = filename.split('/')[-1]
        text = f'A person saying {text} in American accent'
        audio_path = f'{audio_dir}/{filename}'
        audio_json = {'text': text, 'tag': dataset_name}
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        if filename in present_fn:
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(audio_path, audio_save_path,
                          AUDIO_SAVE_SAMPLE_RATE, no_log=True)
            file_id += 1
