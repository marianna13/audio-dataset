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
            filename, cat_index, cat1, cat2, cat3, cat4, cat5, cat6, reference_fname, included, draft, training, participant_id,satisfaction, participants_sound_recording_description, participants_sound_recording_description_confidence = row[1].values
            audio_path = audio_dir+'/'+filename
      
            try: 
            	f = AudioSegment.from_file(audio_path)
            	duration = int(f.duration_seconds)
       	    except:
           	 continue

            description = participants_sound_recording_description

       	    tags = [cat1, cat2, cat3]
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [description.lstrip()],
                        'tag': tags,
                        'original_data': {
                            'title': 'Fine-grained Vocal Imitation Set',
                            'description':'This dataset includes 763 vocal imitations of 108 sound events. The sound event recordings were taken from a subset of Vocal Imitation Set.',
                            'license': 'Creative Commons Attribution 4.0 International',
                            'category_d1': cat1,
                            'category_d2': cat2,
                            'category_d3': cat3,
                            'filename':filename,
                            'duration':duration,
                            'participants_sound_recording_description':participants_sound_recording_description,
                            'participants_sound_recording_description_confidence':participants_sound_recording_description_confidence
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
    audio_dir = 'FineGrained/Fine-grained_VocalImitationSet/AUDIO'

    meta_dir = 'FineGrained/Fine-grained_VocalImitationSet/vocal_imitations.txt'

    meta = pd.read_csv(meta_dir, sep='\t', index_col=0)

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
    preprocess(dataset_name='Fine_grained_VocalImitationSet', num_process=4)
