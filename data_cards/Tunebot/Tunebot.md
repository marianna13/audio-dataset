# Tunebot Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|7 GB| 10000|66.1 hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------
| [Tunebot Website](https://interactiveaudiolab.github.io/resources/datasets/tunebot.html)  | Request access and download the archive of audio files and the meta data from the website  <br>
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
        "playing song \"Hey There Delilah\" by Plain White T's, in the \"All That We Needed\" album"
    ],
    "tag": [
        "music",
        "song",
        "Hey There Delilah",
        "Plain White T's",
        "All That We Needed"
    ],
    "original_data": {
        "title": "Tunebot",
        "description": "The dataset is a collection of 10,000 sung contributions to the Tunebot search engine. Each contribution is a recording of a contributor singing a song to Tunebot. In addition to the 10,000 contributions, there is an associated Google spreadsheet to look up the artist, album, and song for any file. ",
        "song": "Hey There Delilah",
        "artist": "Plain White T's",
        "album": "All That We Needed",
        "filename": "2008/01/01/1199167200101_48496.wav"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the song, artist and album and create a caption with template `playing song "{song}" by {artist}, in the "{album}" album`.
-  **` tag  entry`** We use thesong, artist and album as well as `music` and `song` as tags.
-  **` original data`** We save filename, song name, artist and album name as well as the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).