
from tqdm import tqdm
import os
import pandas as pd
import multiprocessing as mp
import time
import sys
import re
import shutil
import zipfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))



def get_audio_path(audio_dir, track_id):
    """
    """
    tid_str = '{:06d}'.format(track_id)
    return os.path.join(audio_dir, tid_str + '.mp3')


def load(filepath):

    filename = os.path.basename(filepath)

    if 'features' in filename:
        return pd.read_csv(filepath, index_col=0, header=[0, 1, 2])

    if 'echonest' in filename:
        return pd.read_csv(filepath, index_col=0, header=[0, 1, 2])

    if 'genres' in filename:
        return pd.read_csv(filepath, index_col=0)

    if 'tracks' in filename:
        tracks = pd.read_csv(filepath, index_col=0, header=[0, 1])

        COLUMNS = [('track', 'tags'), ('album', 'tags'), ('artist', 'tags'),
                   ('track', 'genres'), ('track', 'genres_all')]
        # for column in COLUMNS:
        #     tracks[column] = tracks[column].map(ast.literal_eval)

        COLUMNS = [('track', 'date_created'), ('track', 'date_recorded'),
                   ('album', 'date_created'), ('album', 'date_released'),
                   ('artist', 'date_created'), ('artist', 'active_year_begin'),
                   ('artist', 'active_year_end')]
        for column in COLUMNS:
            tracks[column] = pd.to_datetime(tracks[column])

        SUBSETS = ('small', 'medium', 'large')
        try:
            tracks['set', 'subset'] = tracks['set', 'subset'].astype(
                'category', categories=SUBSETS, ordered=True)
        except (ValueError, TypeError):
            # the categories and ordered arguments were removed in pandas 0.25
            tracks['set', 'subset'] = tracks['set', 'subset'].astype(
                pd.CategoricalDtype(categories=SUBSETS, ordered=True))

        COLUMNS = [('track', 'genre_top'), ('track', 'license'),
                   ('album', 'type'), ('album', 'information'),
                   ('artist', 'bio')]
        for column in COLUMNS:
            tracks[column] = tracks[column].astype('category')

        return tracks


def process_data(track_ids, texts, artists, output_dir, audio_dir):
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    for track_id, text, artist in tqdm(zip(track_ids, texts, artists), total=len(artists)):
        filename = get_audio_path(audio_dir, track_id)
        audio_path = filename
        title, genre, duration = text
        caption = [f"Music, Genre: {genre} , Title: {title}, Artist: {artist}"]
        tag =[title]
        duration = int(duration)
        for j in range(0, duration-10, 10):
            original_data = {
                'title': 'FMA: A Dataset For Music Analysis',
                'description':"Free Music Archive (FMA), an open and easily accessible dataset suitable for evaluating several tasks in MIR, a field concerned with browsing, searching, and organizing large music collections.",
                'license':'MIT License',
                'filename':filename.split('/')[-1],
                'split':[j,j+10]
                }
            audio_json = {
                'text': caption, 
                'tag': tag, 
                'original_data':original_data,
                }

            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(audio_path, audio_save_path,
                          AUDIO_SAVE_SAMPLE_RATE, segment_start=j,  segment_end=j+10)
            file_id += 1

def process_subfolder(subfolder, dataset_name):
    output_dir = f'/home/ubuntu/marianna/clap/processed_datasets/{dataset_name}/{subfolder}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'/home/ubuntu/marianna/clap/raw_dataset/fma_full/fma_full/{subfolder}'
    meta_dir = f'/home/ubuntu/marianna/clap/raw_dataset/fma_metadata/tracks.csv'
    track_ids = [int(re.sub('0','',audio_name.replace('.mp3',''))) for audio_name in os.listdir(audio_dir)]
    meta = load(meta_dir)
    tracks = meta['track'].iloc[track_ids]

    artists = meta['artist']['name'].iloc[track_ids]
    artists = artists.values
    texts = tracks[['title', 'genre_top', 'duration']].values
    N = len(os.listdir(audio_dir))
    texts = texts
    artists = artists

    file_id = 0
    num_process = 50
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
        p = mp.Process(target=process_data, args=[
                       track_ids[start:end], texts[start:end],  artists[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
    return output_dir


if __name__ == '__main__':
    from utils.merge_dirs import merge_dirs
    from utils.unzip import unzip_file
    dataset_name = 'fma'
    src_file = 'fma_full.zip'
    archive = zipfile.ZipFile(src_file)
    subfolders = set([os.path.dirname(x) for x in archive.namelist()])
    subfolders = [subfolder.replace('fma_full/', '') for subfolder in subfolders]

    for subfolder in subfolders:
        unzip_file(src_file, target_dir='raw_dataset', folder='fma_full/'+subfolder)
        output_dir = process_subfolder(subfolder, dataset_name)
        merge_dirs(root_dir=output_dir, to_rename=True)



