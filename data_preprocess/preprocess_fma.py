
from tqdm import tqdm
import os
import subprocess
import pandas as pd
import multiprocessing as mp
import threading as td
import time
import sys
import re
import shutil
import py7zr
import zipfile
import random
from split_and_rename import split_dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def get_audio_path(audio_dir, track_id):
    """
    """
    tid_str = f'{track_id:06}'
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


def process_data(track_ids, texts, artists, albums, output_dir, audio_dir):
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    import numpy as np
    file_id = 0
    for track_id, text, artist, album in tqdm(zip(track_ids, texts, artists, albums), total=len(artists)):
        filename = get_audio_path(audio_dir, track_id)
        audio_path = filename
        title, genre, duration, composer, language_code, date_recorded = text
        composer_str = f'the composer is {composer}' if isinstance(composer, str) else ''
        genre_str = f'the genre is {genre}' if isinstance(genre, str) else ''
        album_str = f'in album {album}' if isinstance(album, str) else ''
        title_str = f'titled {title}'
        date_str = f'the date created is {date_recorded}'
        language_code_str = f'the language code is {language_code}'
        artist_str = f'by {artist}'
        song_info = [title_str, artist_str, album_str]
        extra_info = [composer_str, genre_str, date_str, language_code_str]
        song_info = [info for info in song_info if info!='']
        extra_info = [info for info in extra_info if info!='']
        random.shuffle(song_info)
        random.shuffle(extra_info)
        song_info = ', '.join(song_info)
        extra_info = ', '.join(extra_info)
        caption = f'playing song {song_info}, of which {extra_info}'
        duration = int(duration)
        # for j in range(0, duration-10, 10):
        original_data = {
            'title': 'FMA: A Dataset For Music Analysis',
            'description':"Free Music Archive (FMA), an open and easily accessible dataset suitable for evaluating several tasks in MIR, a field concerned with browsing, searching, and organizing large music collections.",
            'license':'MIT License',
            'filename':filename.split('/')[-1],
            'genre': str(genre),
            'album': str(album),
            'song_title': str(title),
            'artist':str(artist),
            'duration':duration,
            'composer': str(composer),
            'date_recorded': str(date_recorded),
            'language_code': language_code,
            }
        audio_json = {
            'text': caption, 
            'original_data':original_data,
            }

        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path,
                        AUDIO_SAVE_SAMPLE_RATE)
        file_id += 1

def process_subfolder(subfolder, dataset_name):
    output_dir = f'{dataset_name}_full/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'FMA'
    meta_dir = f'FMA_metadata/fma_metadata/fma_metadata/tracks.csv'
    audios = os.listdir(audio_dir)

    track_ids = [int(audio_name.replace('.mp3','')) for audio_name in audios]
    track_ids.sort()
    meta = load(meta_dir)
    tracks = meta['track']
    tracks = tracks[tracks.index.isin(track_ids)]
    artists = meta['artist']['name']
    artists = artists[artists.index.isin(track_ids)]
    albums = meta['album']['title']
    albums = albums[albums.index.isin(track_ids)].values
    artists = artists.values

    texts = tracks[['title', 'genre_top', 'duration', 'composer', 'language_code', 'date_created']].values
    N = len(audios)
    

    file_id = 0
    num_process = 50
    processes = []
    out_dirs = [f'{output_dir}/{i}' for i in range(num_process)]
    for out_dir in out_dirs:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
            for i in range(num_process)]
    print(N, rngs)
    s = time.time()
    for rng, out_dir in zip(rngs, out_dirs):
        start, end = rng
        p = td.Thread(target=process_data, args=[
                       track_ids[start:end], texts[start:end],  artists[start:end], albums[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
    return output_dir


if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int)
    parser.add_argument('--end', type=int)
    args = parser.parse_args()
    start = args.start
    end = args.end
    dataset_name = 'fma'
    src_file = 'fma_full.zip'    # archive = py7zr.SevenZipFile(src_file)
    subfolders = [f'/fma_full/{i:03d}' for i in range(start, end)]


    # for subfolder in subfolders:
    #     print(subfolder)
    #     cmd = f'7z x fma_full.zip -oFMA {subfolder[1:]}/*'
    #     os.system(cmd)
    #     output_dir = process_subfolder(subfolder, dataset_name)
    #     os.system(f'rm -rf FMA/{subfolder}')
       