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
import yt_dlp
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
    
    return file_name

def get_tags(yt_link):
    ydl_opts = {
          'ignoreerrors': True,
          'no_warnings':True,
          'quiet':True,
          'skip_download':True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info =  ydl.extract_info(yt_link)
        return info['tags']



def process_part(meta, output_dir, audio_dir, st):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    
    for row in tqdm(meta.iterrows(), total=len(meta)):
            artist, song, about, yt_link = row[1].values

            try:

                yt_id = yt_link.replace('http://www.youtube.com/watch?v=', '')
                try:
                    tags = get_tags(yt_link)
                    tags = [t.encode("ascii", "ignore").decode() for t in tags]
                except:
                    continue
            
            except:
                continue

            audio_path = audio_dir+'/'+yt_id+'.m4a'
            song = song.encode('utf-8').decode('utf-8')
            artist = artist.encode('utf-8').decode('utf-8')
            caption = about.encode("ascii", "ignore").decode() if about else f'playing song "{song}" by {artist}'
        

    
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [caption],
                        'tag': tags,
                        'original_data': {
                            'title': 'Genius',
                            'description':"A lyrics & music review website",
                            'song': song,
                            'artist': artist,
                            'about': caption,
                            'url':yt_link,
                            
                            },
                            }
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(
                audio_path, audio_save_path,
                AUDIO_SAVE_SAMPLE_RATE)

            file_id +=1
           

def preprocess(dataset_name, num_process):

    output_dir = f'{dataset_name}_processed'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    audio_dir = 'GENIUS_AUDIO'
    # if not os.path.exists(audio_dir):
    #     os.makedirs(audio_dir)

    df = pd.read_parquet('genius_meta.parquet')

    # meta = df[~df['ABOUT'].isna()][:10]
    meta = df

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
        p = mp.Process(target=process_part, args=[
                       meta[start:end], out_dir, audio_dir, start])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(dataset_name='Genius', num_process=100)
