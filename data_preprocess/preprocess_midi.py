
from tqdm import tqdm
import os
import multiprocessing as mp
import threading as td
import pandas as pd
import time
import subprocess
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def process_data(filenames, rng, output_dir):
    start, end = rng
    filenames = filenames[start:end]
    file_id = 0
    for filename in tqdm(filenames, total=len(filenames)):
        audio_path = f'{audio_dir}/{filename}'
        text = audio_path.split('/')[-1].replace('.mid', '')
        text = text.replace('_', ' ')
        text = text.replace('.flac', '')
        text = f'{text}, MIDI'
        audio_json = {'text': text, 'tag': dataset_name}
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'

        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                 'default=noprint_wrappers=1:nokey=1', audio_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        duration = str(result.stdout)[2:-3]
        if duration != 'N/A':
            duration = int(float(duration))
            for j in range(0, duration-10, 10):
                audio_json_save_path = f'{output_dir}/{file_id}.json'
                audio_save_path = f'{output_dir}/{file_id}.flac'
                json_dump(audio_json, audio_json_save_path)
                audio_to_flac(audio_path, audio_save_path,
                              AUDIO_SAVE_SAMPLE_RATE, segment_start=j,  segment_end=j+10)
                file_id += 1

        else:
            continue


if __name__ == '__main__':
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    dataset_name = 'midi_clean'
    data_dir = f'/opt/marianna/clap/raw_datasets/{dataset_name}'
    output_dir = f'/opt/marianna/clap/processed_datasets/{dataset_name}/clean_midi-4000'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = '/opt/marianna/clap/raw_datasets/clean_midi/AUDIO'
    start, end = 0, 4000
    filenames = os.listdir(audio_dir)[start:end]
    N = len(filenames)
    num_process = 70
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
        p = mp.Process(target=process_data, args=[filenames, rng, out_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
