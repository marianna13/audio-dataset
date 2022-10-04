# VGG-Sound Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|74 GB| 180 879|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [VGG-Sound website](https://www.robots.ox.ac.uk/~vgg/data/vggsound/)  |1. Download meta data fro m the website. 2. For every row in meta data download corresponding youtube audio and extract a specific segment. <br>
## Preprocessing Principles

You may refer to [preprocess_vggsound.py](/data_preprocess/preprocess_vggsound.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (vggsound.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "the sound of waterfall burbling"
    ],
    "tag": [
        "waterfall burbling"
    ],
    "original_data": {
        "title": "VGG-Sound",
        "license": "Creative Commons Attribution 4.0 International License",
        "description": "VGG-Sound is an audio-visual correspondent dataset consisting of short clips of audio sounds, extracted from videos uploaded to YouTube",
        "filename": "--0PQM4-hqg.wav",
        "url": "https://www.youtube.com/watch?v=--0PQM4-hqg",
        "label": "waterfall burbling",
        "start": 30,
        "split": "train"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the label for each audio and create a caption with template `the sound of {label}`.
-  **` tag  entry`** We use the label for each vocal imitation as a tag.
-  **` original data`** We save all the data from each row of vggsound.csv for every audio as well as timestamp, dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
