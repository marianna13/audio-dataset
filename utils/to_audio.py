
import os
import time
from tqdm import tqdm
import threading as td
import subprocess

data_dir = '/opt/marianna/clap/raw_datasets/clean_midi/data/clean_midi'
audio_dir = '/opt/marianna/clap/raw_datasets/clean_midi/AUDIO'


def midi_to_audio(midi_file, audio_file, no_log=True):
    sample_rate = 44100
    sound_font = os.path.expanduser('/usr/share/sounds/sf2/FluidR3_GM.sf2')
    if no_log:
        subprocess.call(['fluidsynth', '-ni', sound_font, midi_file,
                         '-F', audio_file, '-r', str(sample_rate)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    else:
        subprocess.call(['fluidsynth', '-ni', sound_font, midi_file,
                         '-F', audio_file, '-r', str(sample_rate)])


def convert_midi(files, rng):
    start, end = rng
    part_files = files[start:end]
    for file in tqdm(part_files):
        midi_path = f'{data_dir}/{file}'
        file_flac = file.replace('.mid', '.flac')
        audio_path = f'{audio_dir}/{file_flac}'
        midi_to_audio(midi_path, audio_path)


if __name__ == '__main__':
    num_proc = 70
    files = os.listdir(data_dir)
    processes = []
    N = len(files)
    rngs = [(i*int(N/num_proc), (i+1)*int(N/num_proc))
            for i in range(num_proc)]
    for rng in rngs:
        p = td.Thread(target=convert_midi, args=[files, rng])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
