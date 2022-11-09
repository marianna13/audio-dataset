from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import soundfile as sf
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def process_part(meta, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    
    for row in tqdm(meta.iterrows(), total=len(meta)):
            filename, song, artist, album = row[1].values
            audio_path = audio_dir+'/'+filename
       
            try:    
                sf.read(audio_path)
            except:
                continue

            caption = f'playing song "{song}" by {artist}, in the "{album}" album'

     
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [caption],
                        'tag': ['music', 'song', song, artist, album],
                        'original_data': {
                            'title': 'Tunebot',
                            'description':'The dataset is a collection of 10,000 sung contributions to the Tunebot search engine. Each contribution is a recording of a contributor singing a song to Tunebot. In addition to the 10,000 contributions, there is an associated Google spreadsheet to look up the artist, album, and song for any file. ',
                            'song1': song,
                            'artist': artist,
                            'album': album,
                            'filename':filename,
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
    audio_dir = 'raw_dataset/Tunebot'

    sheet_url = 'https://docs.google.com/spreadsheets/d/1DEGydHiJKdb1mMgev_yZLuzsXBUiDerESJg-LCjUvJQ/edit#gid=265039039'
    meta_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

    meta = pd.read_csv(meta_url)

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
                       meta[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(dataset_name='Tunebot', num_process=4)
