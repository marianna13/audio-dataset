# YouTube Dataset Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|| |
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [YouTube website](https://youtube.com/)  |1. Scrape audio files from YouTube website with yt_dlp library. 2. Extract English transcriptions with PyTube library for given video URL.<br>
## Preprocessing Principles

You may refer to [preprocess_youtube.py](/data_preprocess/preprocess_youtube.py) for all the details. Here is a concise summary:

We retrieve information
from transcription and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "a person saying Here's what gives me hope for humanity."
    ],
    "tag": [
        "Is Humanity Smart Enough to Survive Itself? | Jeanette Winterson | TED",
        "TED Youtube Video"
    ],
    "original_data": {
        "title": "YT dataset",
        "filename": "KYK6Tfb0snQ.wav",
        "url": "https://www.youtube.com/watch?v=KYK6Tfb0snQ",
        "duration": 2.961,
        "start": 3.792,
        "end": 6.753
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We just take data from transcription and create a caption with template `a person saying {text}`.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).