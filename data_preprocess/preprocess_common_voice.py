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
            filename, text, age, gender, accents = row[1].values
            gender_str = gender if type(gender)==str else 'person'
            age_str = f'in their {age}' if type(age)==str else ''
            age = age if type(age)==str else ''
            accents_str = f'in {accents} accent' if type(accents)==str else ''
            audio_path = audio_dir+'/'+filename
            # try:    
            #     sf.read(audio_path)
            # except:
            #     continue

            caption = f'A {gender_str} {age_str} saying "{text}" {accents_str}'

     
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [caption],
                        'original_data': {
                            'title': 'Common Voice',
                            'description':'Each entry in the dataset consists of a unique MP3 and corresponding text file. Many of the 24,211 recorded hours in the dataset also include demographic metadata like age, sex, and accent that can help train the accuracy of speech recognition engines.',
                            'license':'CC-0',
                            'text': text,
                            'accent': accents_str,
                            'gender': gender_str,
                            'age': age,
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

    audio_dir = '/fsx/marianna/clap/cv-corpus/cv-corpus-11.0-2022-09-21/en/clips'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    meta_dirs = ['cv-corpus/cv-corpus-11.0-2022-09-21/en/test.tsv', 'cv-corpus/cv-corpus-11.0-2022-09-21/en/train.tsv']

    fs = [pd.read_csv(d, sep='\t') for d in meta_dirs]


    meta = pd.concat(fs)[['path', 'sentence', 'age', 'gender', 'accents']]


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
    preprocess(dataset_name='common_voice', num_process=20)
