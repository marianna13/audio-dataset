from pytube import YouTube
from tqdm import tqdm
import xmltodict
import os
import json
import time
import multiprocessing as mp
from pytube import Channel
import soundfile as sf
import 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def download_from_URL(URL, output_dir):


    # print(wav_path, output_dir)
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

def process_channel(channel_name, channel_url, video_urls, output_dir, audio_dir):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    
    for video_url in tqdm(video_urls, total=len(video_urls)):
        yt = YouTube(video_url)
        print(video_url)

        try:
            caption = yt.captions['en-US']
        except KeyError:
            try:
                caption = yt.captions['en']
            except KeyError:
                try:
                    caption = yt.captions['a.en']
                except kedyError:
                    continue
        title, wav_path = download_from_URL(video_url,audio_dir)

        js = xmltodict.parse(caption.xml_captions)
        timedtext = js['timedtext']['body']['p']
        filename = wav_path
        for dic in timedtext:
            audio_path = audio_dir+filename
            try: 
                sf.read(audio_path)
            except:
                continue
            audio_json_save_path = f'{output_dir}/{file_id}.json'
            audio_save_path = f'{output_dir}/{file_id}.flac'
            try:
                t = int(dic['@t'])/1000
                d = int(dic['@d'])/1000
                end = round(t+d, 3)
                text = dic['#text']
                if '[Music]' in text or 'Transcriber' in text or 'Translator' in text:
                    continue
                text = text.replace('\n', '').replace(u'\u2019', "'").replace('\ufeff', '')
                caption = f'a person saying {text}'
                if '[' in text and ']' in text:
                    caption = text.replece('[', '').replece(']', '')
                audio_json = {
                    'text': [caption],
                    'tag': [title, f'{channel_name} Youtube Video'],
                    'original_data': {
                        'title': 'YT dataset',
                        'filename':filename,
                        'url': video_url,
                        'duration':d,
                        'start':t,
                        'end':end
                        },
                        }
                json_dump(audio_json, audio_json_save_path)
                audio_to_flac(audio_path, audio_save_path,
                            AUDIO_SAVE_SAMPLE_RATE, segment_start=t,  segment_end=end)

                file_id +=1
                break
            except KeyError:
                continue
"/home/ubuntu/marianna/clap/BBCNews/'Monsoon on Steroids'： Investigating Pakistan's unprecedented floods - BBC Newsnight.wav"
def preprocess(channel_name, num_process):

    channel_url = f'hhttps://www.youtube.com/c/{channel_name}'  
    output_dir = f'/home/ubuntu/marianna/clap/{channel_name}_processed'
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    audio_dir = f'/home/ubuntu/marianna/clap/{channel_name}/'
    if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
    c = Channel(channel_url)
    video_urls = c.video_urls
    N = len(video_urls)
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
                       channel_name, channel_url, video_urls[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')

if __name__=='__main__':
    preprocess(channel_name='TED', num_process=10)