
from tqdm import tqdm
import os
import multiprocessing as mp
import pandas as pd
import time
import subprocess
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def process_data(filenames, rng, output_dir, audio_dir, dataset_name):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    from utils.to_audio import midi_to_audio
    start, end = rng
    filenames = filenames[start:end]
    file_id = 0
    for filename in tqdm(filenames, total=len(filenames)):
        
        midi_path = f'{audio_dir}/{filename}'
        audio_path = midi_path.replace('.mid', 'flac')
        subfolders = filename.replace('.mid','').split('___')[:-1]
        
        tag = filename.replace('.mid','').split('___')[-1].replace('.', ' ').replace('_',' ')
        
        text = ' '.join(subfolders).replace('_', ' ')
        text = f'{text} MIDI version'
        if not text.isdigit():

            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            midi_to_audio(midi_file=midi_path,
                        audio_file=audio_path.replace('.mid', 'flac'))

            result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                    'default=noprint_wrappers=1:nokey=1', audio_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            duration = str(result.stdout)[2:-3]
            if duration != 'N/A':
                try:
                    duration = int(float(duration))
                    for j in range(0, duration-10, 10):
                        audio_json = {
                            'text': [text],
                            'tag': [tag],
                            'original_data': {
                                'title': dataset_name,
                                'description': f'{dataset_name} MIDI files',
                                'subfolders': subfolders,
                                'filename':filename,
                                'split': [j, j+10]
                                },
                                }
                        audio_json_save_path = f'{output_dir}/{file_id}.json'
                        audio_save_path = f'{output_dir}/{file_id}.flac'
                        json_dump(audio_json, audio_json_save_path)
                        audio_to_flac(audio_path, audio_save_path,
                                    AUDIO_SAVE_SAMPLE_RATE, segment_start=j,  segment_end=j+10)
                        file_id += 1
                except ValueError:
                    continue

            else:
                continue

        else:
            continue


def preprocess(audio_dir, output_dir, dataset_name, num_process):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    filenames = os.listdir(audio_dir)
    N = len(filenames)
    processes = []
    out_dirs = [f'{output_dir}/{i} 'for i in range(num_process)]
    for out_dir in out_dirs:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
            for i in range(num_process)]
    print(rngs)
    s = time.time()
    for rng, out_dir in zip(rngs, out_dirs):
        start, end = rng
        p = mp.Process(target=process_data, args=[
                       filenames, rng, out_dir, audio_dir, dataset_name])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')


if __name__ == '__main__':
    dataset_name = '130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]'
    audio_dir = f'raw_datasets/{dataset_name}'
    output_dir = f'processed/{dataset_name}'
    preprocess(audio_dir, output_dir, dataset_name, num_process=70)
