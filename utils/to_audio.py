
import os
import time
from tqdm import tqdm
import threading as td
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Convert MIDI files into audio')
parser.add_argument('--data_dir', type=str,
                    help='directory where the dataset is located')
parser.add_argument('--audio_dir', type=str,
                    help='directory where audio is located')
parser.add_argument('--num_processes', type=int,
                    help='number of parallel processes')


args = parser.parse_args()


def midi_to_audio(midi_file, audio_file, no_log=True, to_delete=False):
    sample_rate = 44100
    sound_font = os.path.expanduser('/usr/share/sounds/sf2/FluidR3_GM.sf2')
    if no_log:
        subprocess.call(['fluidsynth', '-ni', sound_font, midi_file,
                         '-F', audio_file, '-r', str(sample_rate)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    else:
        subprocess.call(['fluidsynth', '-ni', sound_font, midi_file,
                         '-F', audio_file, '-r', str(sample_rate)])
    if to_delete:
        os.remove(midi_file)

def convert_midi(files, rng, data_dir, audio_dir):
    start, end = rng
    part_files = files[start:end]
    for file in tqdm(part_files):
        midi_path = f'{data_dir}/{file}'
        file_flac = file.replace('.mid', '.flac')
        audio_path = f'{audio_dir}/{file_flac}'
        midi_to_audio(midi_path, audio_path)


if __name__ == '__main__':
    num_proc = args.num_processes
    data_dir = args.data_dir
    audio_dir = args.audio_dir
    files = os.listdir(data_dir)
    processes = []
    N = len(files)
    rngs = [(i*int(N/num_proc), (i+1)*int(N/num_proc))
            for i in range(num_proc)]
    for rng in rngs:
        p = td.Thread(target=convert_midi, args=[
                      files, rng, data_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
