from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import soundfile as sf
import sys
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def process_part(audio_files, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    
    for audio_path in tqdm(audio_files, total=len(audio_files)):
            _, _, split, track, source = audio_path.split('/')
            title, artist = track.split(' - ')
            filename = '/'.join(audio_path.split('/')[2:])
       
            try:    
                sf.read(audio_path)
            except:
                continue
            
            if 'other' in source:
                continue
            if 'vocals' in source:
                caption = f'singing vocals of the song "{title}" by {artist}'
            elif 'mixture' not in source:
                caption = f'playing {source.replace(".wav", "")} version of the song "{title}" by {artist}'
            else:
                caption = f'playing "{title}" by {artist}'

     
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            audio_json = {
                        'text': [caption],
                        'tag': ['music', 'song', title, artist, source.replace(".wav", "")],
                        'original_data': {
                            'title': 'MUSDB18-HQ',
                            'description':'MUSDB18-HQ is the uncompressed version of the MUSDB18 dataset. It consists of a total of 150 full-track songs of different styles and includes both the stereo mixtures and the original sources, divided between a training subset and a test subset.',
                            'license':'MUSDBHQ: is provided for educational purposes only and the material contained in them should not be used for any commercial purpose without the express permission of the copyright holders',
                            'filename':filename,
                            'split':split
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
    audio_dir = 'raw_dataset/musdb18hq'

    audio_files = glob.glob(f'{audio_dir}/**/*.wav', recursive=True)
    print(audio_files[:10])

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
                       audio_files[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(dataset_name='MUSDB18-HQ', num_process=4)
