from datasets import load_dataset
from tqdm import tqdm
import librosa
import soundfile as sf
import os
import subprocess
import pandas as pd
import multiprocessing as mp
import time
import sys
import math
import re
import shutil
import zipfile
import yaml
import random
from split_and_rename import split_dataset


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))



def process_data(d, output_dir, N):
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    import numpy as np
    file_id = random.randint(0, N*100)
    audio_path = d['file']  
    try:    
        sf.read(audio_path)
    except:
        return
    text = d['text']
    caption = [f'a person saying {text.lower()}']
    filename = d['audio']['path'].split('/')[-1]
    chapter_id = d['chapter_id']
    speaker_id = d['speaker_id']
    audio_path = '/home/ubuntu/.cache/huggingface/datasets/downloads/extracted/1518e53a04065e72f6a0ae1d1870267e3949ae94f8bce3f4652e174dc10e27c2/LibriSpeech/train-clean-100/'
    dir1, dir2,_ = filename.split('-')
    audio_path += f'{dir1}/{dir2}/{filename}'
    id = d['id']
    original_data = {
                'title': 'librispeech_asr',
                'description':"LibriSpeech is a corpus of approximately 1000 hours of 16kHz read English speech, prepared by Vassil Panayotov with the assistance of Daniel Povey. ",
                'license':'CC BY 4.0',
                'filename':filename,
                'text':text,
                'speaker_id':speaker_id,
                'chapter_id':chapter_id,
                'id': id
                }
    audio_json = {
                'text': caption,
                'original_data':original_data,
                }

    audio_json_save_path = f'{output_dir}/{file_id}.json'
    audio_save_path = f'{output_dir}/{file_id}.flac'
    json_dump(audio_json, audio_json_save_path)
    audio_to_flac(audio_path, audio_save_path,AUDIO_SAVE_SAMPLE_RATE)

def process(dataset_name):
    output_dir = f'/home/ubuntu/marianna/clap/processed_dataset/{dataset_name}'
    dataset = load_dataset("librispeech_asr", split='train.clean.100')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    N = len(dataset)

    file_id = 0
    num_process = 5
    processes = []
    out_dirs = [f'{output_dir}/{i} 'for i in range(num_process)]
    for out_dir in out_dirs:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
  
    s = time.time()
    dataset.map(lambda d:process_data(d, output_dir, N), num_proc=num_process)
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
    return output_dir


if __name__ == '__main__':
    from utils.merge_dirs import merge_dirs
    from utils.unzip import unzip_file
    dataset_name = 'librispeech_asr'
    process(dataset_name)
