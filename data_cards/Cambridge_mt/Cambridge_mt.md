# Cambridge-mt Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|38 GB| 6020|279.24 hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------
| [Cambridge-mt Multitrack Dataset Website](https://multitracksearch.cambridge-mt.com/ms-mtk-search.htm)  | Scrape meta data from Cambridge mt website. Download archives/audio.  <br>
## Preprocessing Principles

You may refer to [preprocess_tunebot.py](/data_preprocess/preprocess_tunebot.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "playing song \"Jesse Joy  Release\" by Jesse Joy, in project \"'Release'\""
    ],
    "tag": [
        "music",
        "song",
        "Jesse Joy  Release",
        "Jesse Joy",
        "'Release'"
    ],
    "original_data": {
        "title": "Cambridge-mt Multitrack Dataset",
        "description": "Here's a list of multitrack projects which can be freely downloaded for mixing practice purposes. All these projects are presented as ZIP archives containing uncompressed WAV files (24-bit or 16-bit resolution and 44.1kHz sample rate).",
        "song1": "Jesse Joy  Release",
        "artist": "Jesse Joy",
        "project": "'Release'",
        "filename": "JesseJoy_Release",
        "url": "https://multitracks.cambridge-mt.com/JesseJoy_Release.zip",
        "project_type": "Excerpt"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the song, artist and project and create a caption with template `playing song "{song}" by {artist}, in project "{project}"`.
-  **` tag  entry`** We use thesong, artist and album as well as `music` and `song` as tags.
-  **` original data`** We save filename, song name, artist and album name as well as the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).