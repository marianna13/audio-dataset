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
    from utils.get_duration import get_flac_duration
    file_id = 0
    
    for row in tqdm(meta.iterrows(), total=len(meta)):
        filename, description, library, category, subcategory, keywords, bwdescription = row[1].values
        audio_path = audio_dir+'/'+filename

        
        try: 
            sf.read(audio_path)
            duration = len(f) / f.samplerate
            duration = int(duration)
        except:
            continue

        tags = [ k for k in keywords.split() if '_' not in k]

        for j in range(0, duration-10, 10):
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [description],
                        'tag': tags,
                        'original_data': {
                            'title': 'Boom Library',
                            'description':'Sound effects library',
                            'description_audio':description,
                            'library':library,
                            'category':category,
                            'subcategory':subcategory,
                            'keywords':keywords,
                            'bwdescription':bwdescription,
                            'start':j,
                            'filename':filename
                            },
                            }
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(
                audio_path, audio_save_path,
                AUDIO_SAVE_SAMPLE_RATE, segment_start=j,  segment_end=j+10)

            file_id +=1

def preprocess(dataset_name, num_process):

    output_dir = f'{dataset_name}_processed'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    audio_dir = f'520m'

    meta_dir = '520m/00_Death_Whistle_Metadata.xlsx'

    meta = pd.read_excel(meta_dir)[['Filename', 'Description', 'Library', 'Category', 'SubCategory', 'Keywords', 'BWDescription']]

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
    data_dir = 'BoomLibary'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    os.system(f'aws s3 cp s3://s-laion-audio/raw_dataset/BoomLibrary_Free_Datasets {data_dir}')
    os.sytem(f'unzip {data_dir}/fsdw_520mb.zip -d 620m')
    preprocess(dataset_name='boom_library_520m', num_process=4)