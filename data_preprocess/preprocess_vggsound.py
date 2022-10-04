from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import soundfile as sf
import pandas as pd
import sys
import yt_dlp
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def download_from_URL(URL, output_dir):

    ydl_opts = {
        "outtmpl": output_dir + "%(id)s.%(ext)s", 
        # since ffmpeg can not edit file in place, input and output file name can not be the same
        "format": "bestaudio/best",
        "postprocessors": [
            {   
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav"
            },
        ]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
        info = ydl.extract_info(URL, download=False)
        return info['title'], info['id']+'.wav'

def process_channel(meta, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    
    for row in tqdm(meta.iterrows(), total=len(meta)):
        yt_id, start, label, split = row[1].values
        video_url = f'https://www.youtube.com/watch?v={yt_id}'

        try:
            title, wav_path = download_from_URL(video_url,audio_dir)
        except:
            continue
        time.sleep(1)
        filename = wav_path
        audio_path = audio_dir+filename
        try: 
            sf.read(audio_path)
        except:
            continue
        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        text = f'the sound of {label}'
        audio_json = {
                    'text': [text],
                    'tag': label.split(', '),
                    'original_data': {
                        'title': 'VGG-Sound',
                        'license': 'Creative Commons Attribution 4.0 International License',
                        'description':'VGG-Sound is an audio-visual correspondent dataset consisting of short clips of audio sounds, extracted from videos uploaded to YouTube',
                        'filename':filename,
                        'url': video_url,
                        'label':label,
                        'start':start,
                        'split':split
                        },
                        }
        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(
            audio_path, audio_save_path,
            AUDIO_SAVE_SAMPLE_RATE, segment_start=start,  segment_end=start+10)

        file_id +=1
        os.remove(audio_path)

def preprocess(dataset_name, num_process):

    channel_url = f'hhttps://www.youtube.com/c/{dataset_name}'  
    output_dir = f'/home/ubuntu/marianna/clap/{dataset_name}_processed'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    audio_dir = f'/home/ubuntu/marianna/clap/{dataset_name}/'
    if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
    meta_dir = '/home/ubuntu/marianna/clap/raw_datasets/VGGSound/vggsound.csv'

    meta = pd.read_csv(meta_dir)

    N = len(meta)
    print(N)
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
        p = mp.Process(target=process_channel, args=[
                       meta[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(dataset_name='VGGSound', num_process=20)