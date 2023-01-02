from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import soundfile as sf
import pandas as pd
import sys
import shutil
import requests
import glob
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def download(URL, out_dir):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    doc = requests.get(URL, headers=headers)
    file_name = URL.split('/')[-1]
    file_name = f'{out_dir}/{file_name}'
    try:
        with open(file_name, 'wb') as f:
            f.write(doc.content)
    except:
        print(URL)


def process_part(meta, output_dir, audio_dir, st):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    
    for row in tqdm(meta.iterrows(), total=len(meta)):
            if file_id < 7:
                file_id += 1
                continue
            artist, project, project_type, number_of_tracks, url = row[1].values
            filename = url.split('/')[-1]
            tmp_dir = 'TMP'+ str(st)
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)
            if '.zip' in filename.lower():
                download(url, tmp_dir)
                os.system(f'unzip {tmp_dir}/{filename} -d {audio_dir}')
                shutil.rmtree(tmp_dir)
            else:
                download(url, audio_dir)
            if filename.endswith('.txt'):
                continue
            if os.path.isfile(f'{audio_dir}/{filename}') or filename.endswith('wav'):
                audio_path = f'{audio_dir}/{filename}'
                song = filename.split('/')[-1].split('.')[0].replace('-', '').replace('_', ' ').replace('  ', ' ')
                song = re.findall('[A-Z][^A-Z]*', song)
                song = ' '.join(song)
        
    

                caption = f'playing song "{song}" by {artist}, in the project {project}'

        
                audio_json_save_path = f'{output_dir}/{file_id}.json'
                audio_save_path = f'{output_dir}/{file_id}.flac'
                audio_json = {
                            'text': [caption],
                            'tag': ['music', 'song', song, artist, project],
                            'original_data': {
                                'title': 'Cambridge-mt Multitrack Dataset',
                                'description':"Here's a list of multitrack projects which can be freely downloaded for mixing practice purposes. All these projects are presented as ZIP archives containing uncompressed WAV files (24-bit or 16-bit resolution and 44.1kHz sample rate).",
                                'song1': song,
                                'artist': artist,
                                'project': project,
                                'filename':filename,
                                'url':url,
                                'project_type':project_type
                                },
                                }
                json_dump(audio_json, audio_json_save_path)
                audio_to_flac(
                    audio_path, audio_save_path,
                    AUDIO_SAVE_SAMPLE_RATE)
                # os.remove(audio_path)

                file_id +=1
            else:
                filename = filename.replace(".zip", "")
                for f in os.listdir(f'{audio_dir}/{filename}'):

                    if f.endswith('.txt'):
                        continue

                    audio_path = f'{audio_dir}/{filename}/{f}'
        
                    # try:    
                    #     sf.read(audio_path)
                    # except:
                    #     continue
                    
                    song = filename.split('/')[-1].split('.')[0].replace('-', '').replace('_', ' ').replace('  ', ' ')
                    song = re.findall('[A-Z][^A-Z]*', song)
                    song = ' '.join(song)
        

                    caption = f'playing song "{song}" by {artist}, in project "{project}"'

            
                    audio_json_save_path = f'{output_dir}/{file_id}.json'
                    audio_save_path = f'{output_dir}/{file_id}.flac'
                    audio_json = {
                                'text': [caption],
                                'tag': ['music', 'song', song, artist, project],
                                'original_data': {
                                    'title': 'Cambridge-mt Multitrack Dataset',
                                    'description':"Here's a list of multitrack projects which can be freely downloaded for mixing practice purposes. All these projects are presented as ZIP archives containing uncompressed WAV files (24-bit or 16-bit resolution and 44.1kHz sample rate).",
                                    'song1': song,
                                    'artist': artist,
                                    'project': project,
                                    'filename':filename,
                                    'url':url,
                                    'project_type':project_type
                                    },
                                    }
                    json_dump(audio_json, audio_json_save_path)
                    audio_to_flac(
                        audio_path, audio_save_path,
                        AUDIO_SAVE_SAMPLE_RATE,
                        no_log=True
                        )
                    # os.remove(audio_path)

                    file_id +=1

def preprocess(dataset_name, num_process):

    output_dir = f'{dataset_name}_processed'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    audio_dir = 'cambridge_mt_audio'
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    meta = pd.read_parquet('raw_dataset/cambridge_mt_meta.parquet')

    N = len(meta)
    print(N)
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
        # if out_dir in ['Cambridge_mt_processed/2','Cambridge_mt_processed/8']:
        p = mp.Process(target=process_part, args=[
                    meta[start:end], out_dir, audio_dir, start])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(dataset_name='Cambridge_mt', num_process=10)
