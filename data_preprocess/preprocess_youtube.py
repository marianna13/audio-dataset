from tqdm import tqdm
import os
import json
import time
import multiprocessing as mp
import xmltodict
import soundfile as sf
import pandas as pd
import sys
import yt_dlp
from autocorrect import Speller
import glob
from pytube import Channel
# import webvtt
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def get_seconds(dt):
    return dt.hour*3600+dt.minute*60+dt.second


def sub_to_dict(sub) -> list:
    """Convert WebVTT to JSON, optionally removing duplicate lines"""

    with open(sub, 'r', encoding='utf-8') as f:
        captions = xmltodict.parse(f.read())
    # print(captions)
    dicts = []
    prev_s = None
    prev_text = None
    for c in captions['tt']['body']['div']['p']:

        e = c['@end']
        s = c['@begin']
        fmt = '%H:%M:%S.%f'
        if prev_s:
            dicts.append(
            {
                'start': prev_s,
                'end': s,
                'line': prev_text
            }
        )
            
        prev_s = s
        prev_text = c['#text']
        # e = (datetime.strptime(e, fmt)-datetime.strptime(s, fmt)).strftime(fmt)
       
        
    return dicts

def download_channel(URL, audio_dir):
    ydl_opts = {
        "outtmpl": audio_dir+'/' + "%(id)s.%(ext)s", 
        # since ffmpeg can not edit file in place, input and output file name can not be the same
        "format": "bestaudio/best",
        "quiet": True,
        "subtitlesformat":"ttml",
        "postprocessors": [
            {   
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3"
            },
        ],
        "writesubtitles": True,
        "subtitleslangs": ["en"],
        "writeautomaticsub": True,
        "ignore_errors": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as yt:

        # info_dict = yt.extract_info(URL, download=False)
        # sub_url = info_dict["requested_subtitles"]["en"]["url"]
        # res = requests.get(sub_url)
        # sub = io.TextIOWrapper(io.BytesIO(res.content)).read()
        # sub_dict = sub_to_dict(sub)
        yt.download([URL])

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

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)

def process_channel(audios, output_dir, audio_dir, channel_name=None):
    from utils.file_utils import json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    file_id = 0
    
    for audio_path in tqdm(audios, total=len(audios)):

        sub = audio_path.replace('.mp3', '.en.ttml')
        yt_id = audio_path.split('/')[-1].replace('.mp3', '')
        try:
            dicts = sub_to_dict(sub)
        except:
            continue

        segment_times = []
        audio_jsons = []
        for dic in dicts:
            
            # try: 
            #     sf.read(audio_path)
            # except:
            #     continue
            # audio_json_save_path = f'{output_dir}/{file_id}.json'
            # audio_save_path = f'{output_dir}/{file_id}.flac'
            try:
                start = dic['start']
                end = dic['end']
                

                text = dic['line']
                if '[Music]' in text or 'Transcriber' in text or 'Translator' in text:
                    continue

                text = text.replace('\n', '').replace(u'\u2019', "'").replace('\ufeff', '')
                caption = f'a person saying "{text}"'
                if '[' in text and ']' in text:
                    caption = text.replace('[', '').replace(']', '')

        
                audio_json = {
                    'text': [caption],
                    'original_data': {
                        'title': 'YT dataset',
                        'id': yt_id,
                        'caption':text,
                        'channel':channel_name,
                        'start':start,
                        'end':end
                        },
                        }
                
                # json_dump(audio_json, audio_json_save_path)
                # audio_to_flac(audio_path, audio_save_path,
                #             AUDIO_SAVE_SAMPLE_RATE, segment_start=start,  segment_end=end)

            except Exception as err:
                print(err)
                continue
            segment_times.append(get_sec(start))
            audio_jsons.append(audio_json)

        data = pd.DataFrame({
            'st':segment_times,
            'aj':audio_jsons
        })
        data = data.sort_values(['st'])
        start = str(segment_times[0])
        segment_times = ','.join([str(s) for s in list(data['st'].values)])
        os.system(f'ffmpeg  -v error -i {audio_path} -c:a flac -map 0 -flags +bitexact -ar 48000 -ac 1 -segment_times {segment_times} -f segment {output_dir}/{file_id}_%03d.flac')
        flacs = glob.glob(f'{output_dir}/{file_id}_*', recursive=True)
        flacs.sort()
        os.remove(flacs[0])
        os.remove(flacs[-1])
        flacs = flacs[1:-1]
        for f, aj in zip(flacs, list(data['aj'].values)):
            j = f.replace('.flac', '.json')
            json_dump(aj, j)

        file_id +=1

            

def preprocess(channel_name, num_process):

    channel_url = f'https://www.youtube.com/user/{channel_name}'  
    audio_dir = f'YT_DATA/{channel_name}_data'
    output_dir = f'processed/YT_DATASET/{channel_name}_processed'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    c = Channel(channel_url)
    # urls = c.video_urls

    # with mp.Pool(20) as p:
    #     p.starmap(download_channel, [(url, audio_dir) for url in urls])
    audios = glob.glob(f'{audio_dir}/**/*.mp3', recursive=True)
    N = len(audios)
    if num_process >= N:
        num_process = N - 1
    print(N)
    processes = []
    out_dirs = [f'{output_dir}/{i}' for i in range(num_process)]
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
                       audios[start:end], out_dir, audio_dir, channel_name])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
    # os.system(f'rm -rf {audio_dir}')

if __name__=='__main__':

    channels = [
        'tedtalksdirector', 
        'tededucation', 
        'tedxtalks', 
        'powerfuljre', 
        'lexfridman', 
        'theovonk', 
        'Koncrete',
        'koncreteinc',
        'yalecourses',
        'MIT',
        '60minutes',
        'telegraphtv',
        'thelatelateshow',
        'bbcnews',
        'teamcoco',
        'aljazeeraenglish',
        'SKYNEWS',
        'robcesternino',
        'GoogleTechTalks',
        'successtalks',
        'gotoconferences',
        'MunichSecurityConf'
        ]

    channels = channels[3:4]
    for i in range(len(channels)):
        channel = channels[i]
        
        # os.system(f'yt-dlp --print "%(id)s" "https://www.youtube.com/@{channel}" > yt_vids/{channel}.txt')
        print(f'processing channel #{i}: {channel}')
        preprocess(channel_name=channel, num_process=50)
        # break