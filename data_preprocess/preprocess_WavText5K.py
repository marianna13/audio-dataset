from tqdm import tqdm
import os
import pandas as pd
import multiprocessing as mp
import sys
import soundfile as sf
import re
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def download_and_save_file(URL, audio_dir):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://bigsoundbank.com',
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
        view_link,download_link,title,description, fname, tags = row[1].values


        
        tags = tags if tags==tags else ""
        audio_path = download_and_save_file(download_link, audio_dir)
        try:    
            sf.read(audio_path)
        except:
            continue
        description = description if description==description else ""
        text = description if description!="" else f'the sound of {title}'
        tag = tags.replace('[','').replace(']','').replace("'",'').split(', ')
        if tags==[""]:
            tag = [title]
        audio_json = {
            'text': [text],
            'tag': tag,
            'original_data': {
                'title': 'WavText5K',
                'description': 'WavText5K collection consisting of 4525 audios, 4348 descriptions, 4525 audio titles and 2058 tags.',
                'license': 'MIT License',
                'download_link': download_link,
                'view_link':view_link,
                'audio_title':title,
                'fname':fname,
                'audiodescription':description,
                'tags': tags
            }
        }
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'

        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path,
                      AUDIO_SAVE_SAMPLE_RATE, no_log=True)
        file_id += 1


if __name__ == '__main__':
    dataset_name = 'WavText5K_processed'
    output_dir = f'{dataset_name}'
    meta_dir = '/home/ubuntu/marianna/clap/WavText5K/WavText5K.csv'
    preprocess(meta_dir=meta_dir, output_dir=output_dir,
               audio_dir='WavText5K/AUDIO')
