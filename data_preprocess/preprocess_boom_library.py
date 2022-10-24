from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import soundfile as sf
import pandas as pd
import sys
from pydub import AudioSegment
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def process_part(meta, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    from utils.get_duration import get_flac_duration
    file_id = 0
    
    for row in tqdm(meta.iterrows(), total=len(meta)):
            filename, description, cat, subCat = row[1].values
            audio_path = audio_dir+'/'+filename

       
            try: 
            	f = AudioSegment.from_file(audio_path)
            	duration = int(f.duration_seconds)
       	    except:
           	 continue

       	    tags = [cat, subCat]

     
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [description],
                        'tag': tags,
                        'original_data': {
                            'title': 'Boom Library',
                            'description':'Sound effects library',
                            'description_audio':description,
                            'filename':filename,
                            'category':cat,
                            'sub_category':subCat
                            },
                            }
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(
                audio_path, audio_save_path,
                AUDIO_SAVE_SAMPLE_RATE)

            file_id +=1

def process_part_wo_meta(output_dir, audio_dir, audio_files):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    from utils.get_duration import get_flac_duration
    file_id = 0
    
    for filename in tqdm(audio_files, total=len(audio_files)):
            audio_path = audio_dir+'/'+filename

            f = AudioSegment.from_file(audio_path)
            try: 
            	f = AudioSegment.from_file(audio_path)
       	    except:
           	 continue

       	    tags = [' '.join([ k for k in filename.replace('.wav', '').replace('-', ' ').split() if '_' not in k])]
            description = filename.replace('__', '_').replace('_', ' ').replace('.wav', '').replace('-', ' ')
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [description],
                        'tag': tags,
                        'original_data': {
                            'title': 'Boom Library',
                            'description':'Sound effects library',
                            'description_audio':description,
                            'filename':filename
                            },
                            }
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(
                audio_path, audio_save_path,
                AUDIO_SAVE_SAMPLE_RATE)

            file_id +=1

def preprocess(num_process):

    audio_dir = f'BOOM/BOOM Library Halloween 2021 Free SFX'
    dataset_name = audio_dir.split('/')[-1]

    output_dir = f'{dataset_name}_processed'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # meta_dir = 'BOOM/10 Years Anniversary Addition - Cinematic Metal Impacts/00_Cinematic_Metal_Impacts_Metadata_10_Years_Addition.xls'

    # meta = pd.read_excel(meta_dir)
    # meta = meta[['Filename', 'Description', 'Category', 'SubCategory']]
    

    audio_files = os.listdir(audio_dir)
    N = len(audio_files)
    # N = len(meta)
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
        p = mp.Process(target=process_part_wo_meta, args=[
                        out_dir, audio_dir,audio_files[start:end]])
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
    preprocess(num_process=4)
