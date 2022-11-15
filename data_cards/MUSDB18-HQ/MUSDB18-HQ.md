# MUSDB18-HQ Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|5 GB| 598|39.24 hrs|
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
        "playing drums version of the song \"Patrick Talbot\" by Set Me Free"
    ],
    "tag": [
        "music",
        "song",
        "Patrick Talbot",
        "Set Me Free",
        "drums"
    ],
    "original_data": {
        "title": "MUSDB18-HQ",
        "description": "MUSDB18-HQ is the uncompressed version of the MUSDB18 dataset. It consists of a total of 150 full-track songs of different styles and includes both the stereo mixtures and the original sources, divided between a training subset and a test subset.",
        "license": "MUSDBHQ: is provided for educational purposes only and the material contained in them should not be used for any commercial purpose without the express permission of the copyright holders",
        "filename": "train/Patrick Talbot - Set Me Free/drums.wav",
        "split": "train"
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