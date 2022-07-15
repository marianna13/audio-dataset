from tqdm import tqdm
import os
import pandas as pd
import multiprocessing as mp
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def download_and_save_file(URL, audio_dir):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://dictionary.cambridge.org/dictionary/english',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,',
        'cookie': 'prov=6bb44cc9-dfe4-1b95-a65d-5250b3b4c9fb; _ga=GA1.2.1363624981.1550767314; __qca=P0-1074700243-1550767314392; notice-ctt=4%3B1550784035760; _gid=GA1.2.1415061800.1552935051; acct=t=4CnQ70qSwPMzOe6jigQlAR28TSW%2fMxzx&s=32zlYt1%2b3TBwWVaCHxH%2bl5aDhLjmq4Xr',
    }
    doc = requests.get(URL, headers=headers)
    file_name = URL.split('/')[-1]
    audio_path = f'{audio_dir}/{file_name}'
    with open(audio_path, 'wb') as f:
        f.write(doc.content)
    return audio_path


def preprocess(meta_dir, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    meta = pd.read_csv(meta_dir)

    file_id = 0
    for row in tqdm(meta.iterrows(), total=len(meta)):
        index, label, URL, us_URL = row[1].values
        text = f'the person is reading the word {label} in British accent'

        audio_path = download_and_save_file(URL, audio_dir)
        audio_json = {
            'text': [text],
            'tag': [label],
            'original_data': {
                'title': 'Cambridge Dictionary dataset',
                'Description': 'Words and their pronunciations scraped from the Cambridge Dictionary website',
                'URL': URL,
                'accent': 'British'
            }
        }
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'

        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path,
                      AUDIO_SAVE_SAMPLE_RATE, no_log=True)
        file_id += 1


if __name__ == '__main__':
    dataset_name = 'cambridge_dictionary'
    output_dir = f'{dataset_name}'
    meta_dir = 'cambridge_dictionary/meta.csv'
    preprocess(meta_dir=meta_dir, output_dir=output_dir,
               audio_dir='cambridge_dictionary/AUDIO')
