from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import soundfile as sf
import pandas as pd
import sys
import glob
from pydub import AudioSegment
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def process_part(audio_files, output_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    from utils.get_duration import get_flac_duration
    file_id = 0
    
    for audio_path in tqdm(audio_files, total=len(audio_files)):
        
            try: 
            	f = AudioSegment.from_file(audio_path)
            	duration = f.duration_seconds
       	    except:
           	    continue

            filename = audio_path.split('/')[-1]
            emotion = filename.split('_')[0]
            text = f'sound of knocking with {emotion}'
            tags = ['sound of knocking', emotion]


     
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            print(audio_save_path)
            audio_json = {
                        'text': [text],
                        'tag': tags,
                        'original_data': {
                            'title': 'Knocking Sound Effects With Emotional Intentions',
                            'description':'The dataset was recorded by the professional foley artist Ulf Olausson at the FoleyWorks (http://foleyworks.se/) studios in Stockholm on the 15th October, 2019. Inspired by previous work on knocking sounds [1]. we chose five type of emotions to be portrayed in the dataset: anger, fear, happiness, neutral and sadness.',
                            'license': 'Creative Commons Attribution 4.0 International',
                            'filename':filename,
                            'duration':duration,
                            'emotion':emotion,
                            },
                            }
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(
                audio_path, audio_save_path,
                AUDIO_SAVE_SAMPLE_RATE,
                no_log=True)

            file_id +=1

def preprocess(dataset_name, num_process):

    output_dir = f'{dataset_name}_processed'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    audio_dir = 'Knocking_effects/Knocking Sound Effects With Emotional Intentions'
    audio_files = glob.glob(f'{audio_dir}/**/*.wav', recursive=True)

    N = len(audio_files)
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
                       audio_files[start:end], out_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(dataset_name='Knocking_sounds', num_process=4)
