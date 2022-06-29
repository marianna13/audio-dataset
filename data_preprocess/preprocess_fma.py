
from tqdm import tqdm
import os
import pandas as pd
import multiprocessing as mp
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

AUDIO_DIR = '/mnt/marianna/clap/raw_datasets/fma/fma_small/data/fma_small'


def get_audio_path(audio_dir, track_id):
    """
    """
    tid_str = '{:06d}'.format(track_id)
    return os.path.join(audio_dir, tid_str[:3], tid_str + '.mp3')


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


def process_data(track_ids, texts, artists, output_dir):
    file_id = 0
    for track_id, text, artist in tqdm(zip(track_ids, texts, artists), total=len(artists)):
        filename = get_audio_path(AUDIO_DIR, track_id)
        audio_path = filename
        title, genre, duration = text
        caption = f"Music , Genre: {genre} , Title: {title}, Artist: {artist}"
        audio_json = {'text': caption, 'tag': 'fma'}
        duration = int(duration)
        for j in range(0, duration-10, 10):

            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            json_dump(audio_json, audio_json_save_path)
            audio_to_flac(audio_path, audio_save_path,
                          AUDIO_SAVE_SAMPLE_RATE, segment_start=j,  segment_end=j+10)
            file_id += 1


if __name__ == '__main__':
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    dataset_name = 'fma'
    data_dir = f'/mnt/marianna/clap/raw_datasets/{dataset_name}'
    output_dir = f'/mnt/marianna/clap/processed_datasets/{dataset_name}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'{data_dir}/audio'
    meta_dir = f'/mnt/marianna/clap/raw_datasets/fma/meta/fma_metadata/tracks.csv'
    meta = load(meta_dir)
    subset = meta['set']
    small_ids = list(subset.loc[subset['subset'] == 'small'].index)
    tracks = meta['track']

    tracks = tracks[tracks.index.isin(small_ids)]
    artists = meta['artist']['name']
    artists = artists[artists.index.isin(small_ids)].values
    track_ids = tracks.index
    texts = tracks[['title', 'genre_top', 'duration']].values
    N = 1000
    track_ids = track_ids[:N]
    texts = texts[:N]
    artists = artists[:N]

    file_id = 0
    num_process = 20
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
                       track_ids[start:end], texts[start:end],  artists[start:end], out_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
