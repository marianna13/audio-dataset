import os
import shutil
import argparse
import glob
import random
import numpy as np
from tqdm import tqdm
import threading as td
import multiprocessing as mp

random.seed(1234)

def split_part(files, split_output_dir, file_id):
    for audio_file in tqdm(files):
        json_file = audio_file.replace('.flac', '.json')
        audio_save_path = os.path.join(split_output_dir, f'{file_id}.flac')
        audio_json_save_path = audio_save_path.replace('.flac', '.json')
        shutil.move(audio_file, audio_save_path)
        shutil.move(json_file, audio_json_save_path)
        file_id += 1

def split_dataset(data_dir):
    test_portion = 0.1

    splits = ['train', 'test']

    file_list = glob.glob(f'{data_dir}/**/*.flac', recursive=True)
    random.shuffle(file_list)

    split_idx = int(np.round(len(file_list) * test_portion))
    test_list = file_list[:split_idx]
    train_list = file_list[split_idx:]
    split_file_list = {'train': train_list, 'test': test_list}

    file_id = 1
    for split in splits:
        split_output_dir = os.path.join(data_dir, split)
        os.makedirs(split_output_dir, exist_ok=True)
        N = len(split_file_list[split])
        num_process = 10
        rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
            for i in range(num_process)]
        print(N, rngs)
        processes = []
        for rng in rngs:
            start, end = rng
            p = td.Thread(target=split_part, args=[
                        split_file_list[split][start:end], split_output_dir, file_id])
            p.start()
            processes.append(p)
            file_id += end
        for p in processes:
            p.join()
        # for audio_file in tqdm(split_file_list[split]):
        #     json_file = audio_file.replace('.flac', '.json')
        #     audio_save_path = os.path.join(split_output_dir, f'{file_id}.flac')
        #     audio_json_save_path = audio_save_path.replace('.flac', '.json')
        #     shutil.move(audio_file, audio_save_path)
        #     shutil.move(json_file, audio_json_save_path)
        #     file_id += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default=None, help='data directory')
    args = parser.parse_args()
    data_dir = args.data_dir
    split_dataset(data_dir)

