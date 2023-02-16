import librosa
import glob
from tqdm import tqdm
import os
import multiprocessing as mp
import threading as td
import soundfile as sf
from get_duration import get_flac_duration

def get_dur(file_list, return_dict):
    total_duration = 0
    for file in tqdm(file_list):
        try:
            arr = sf.read(file)
            # if arr[0].all() == 0:
            #     print('zeros: ',file)
                # os.remove(file)
                # os.remove(file.replace('.flac', '.json'))
            # d = librosa.get_duration(filename=file)
            # d = get_flac_duration(file)
            # total_duration += d
        except Exception as e:
            print(e)
            print(file)
            os.remove(file)
            os.remove(file.replace('.flac', '.json'))
    return_dict['dur'] += total_duration





if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--end', type=int, default=-1)
    args = parser.parse_args()
    start = args.start
    end = args.end
    manager = mp.Manager()
    return_dict = manager.dict()
    return_dict['dur'] = 0
    data_dir = 'fma_full/fma_full'
    file_extension = 'flac'
    file_list = glob.glob(f'{data_dir}/**/*.{file_extension}', recursive=True)
    file_list.sort()
    file_list = file_list[start:end]
    # total_duration = 0
    # for file in tqdm(file_list):
    #     d = librosa.get_duration(filename=file)
    #     total_duration += d
    # print(total_duration)
    N = len(file_list)
    num_process = 100
    rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
        for i in range(num_process)]
    print(N, rngs)
    processes = []
    for rng in rngs:
        start, end = rng
        p = mp.Process(target=get_dur, args=[
                    file_list[start:end], return_dict])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
        
    print(return_dict['dur'])
