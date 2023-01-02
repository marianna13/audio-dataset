from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import soundfile as sf
import pandas as pd
import sys
from datasets import load_dataset
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def process_part(meta, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    

    for row in tqdm(meta.iterrows(), total=len(meta)):
            filename, text = row[1].values
            _, acc, gender = filename.split('_')[:3]
            gender = gender.split('/')[0]
            audio_path = audio_dir+'/'+filename
            try:    
                sf.read(audio_path)
            except:
                continue

            caption = f'A person saying "{text}"'

     
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [caption],
                        'tag': [gender,f'{accents[acc]} accent'],
                        'original_data': {
                            'title': 'CMU_Arctic',
                            'description':'The databases consist of around 1150 utterances carefully selected from out-of-copyright texts from Project Gutenberg. The databses include US English male (bdl) and female (slt) speakers (both experinced voice talent) as well as other accented speakers.',
                            'license':'BSD',
                            'text': text,
                            'accent': accents[acc],
                            'gender': gender,
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
    audio_dir = 'CMU_Arctic_extracted'

    meta = load_dataset('MLCommons/peoples_speech', split='test')
    print(meta)


    # N = len(meta)
    # print(N)
    # processes = []
    # out_dirs = [f'{output_dir}/{i}' for i in range(num_process)]
    # for out_dir in out_dirs:
    #     if not os.path.exists(out_dir):
    #         os.makedirs(out_dir)
    # rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
    #         for i in range(num_process)]
    # print(rngs)
    # s = time.time()
    # for rng, out_dir in zip(rngs, out_dirs):
    #     start, end = rng
    #     p = mp.Process(target=process_part, args=[
    #                    meta[start:end], out_dir, audio_dir])
    #     p.start()
    #     processes.append(p)
    # for p in processes:
    #     p.join()
    # e = time.time()
    # print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(dataset_name='Peoples_speech', num_process=1)
