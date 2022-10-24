from tqdm import tqdm
import os
import pandas as pd
import multiprocessing as mp
import sys
import soundfile as sf
import requests
import time
import librosa
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def download_and_save_file(URL, audio_dir):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://www.zapsplat.com/sound-effect-category/',
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


def preprocess(meta, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    file_id = 0
    for row in tqdm(meta.iterrows(), total=len(meta)):
        text, URL, tags, category, lic  = row[1].values
        tags = tags.split(',')

        audio_path = download_and_save_file(URL, audio_dir)
        # sy, sr = librosa.load(audio_path)
        # try:    
        #     sf.read(audio_path)
        # except:
        #     continue

        audio_json = {
            'text': [text],
            'tag': tags,
            'original_data': {
                'title': 'ZAPSPLAT dataset',
                'Description': 'Free sound effects from ZAPSPLAT website',
                'audio_title':text,
                'category':category,
                'URL': URL,
                'license': lic,
                'tags':tags
            }
        }
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'

        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path,
                      AUDIO_SAVE_SAMPLE_RATE, no_log=True)
        file_id += 1


if __name__ == '__main__':
    dataset_name = 'ZAPSPLAT_dataset'
    output_dir = f'{dataset_name}'
    audio_dir = 'ZAPSLAT/AUDIO'
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    meta_dir = 'ZAPSLAT/ZAPSPLAT_meta.parquet'
    meta = pd.read_parquet(meta_dir)
    num_process = 10
    N = len(meta)
    processes = []
    out_dirs = [f'{output_dir}/{i}' for i in range(num_process)]
    for out_dir in out_dirs:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
            for i in range(num_process)]
    print(rngs)
    s = time.time()
    for rng, out_dir in zip(rngs, out_dirs):
        start, end = rng
        p = mp.Process(target=preprocess, args=[
                       meta[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
