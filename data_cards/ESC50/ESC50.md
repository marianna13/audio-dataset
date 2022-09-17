# ESC-50 Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|404M| 2500|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [ESC-50: Dataset for Environmental Sound Classification](https://github.com/karolpiczak/ESC-50)  |Download audio files and meta data from ESC-50 GitHub page.  <br>
## Preprocessing Principles

You may refer to [preprocess_esc50y.py](/data_preprocess/preprocess_esc50.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (esc50.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "The sound of the insects"
    ],
    "tag": [
        "insects"
    ],
    "original_data": {
        "title": "ESC-50",
        "desciption": "ESC-50: Dataset for Environmental Sound Classification",
        "license": "Creative Commons Attribution Non-Commercial license",
        "fname": "1-7973-A-7.wav",
        "fold": 1,
        "target": 7,
        "category": "insects",
        "esc10": false,
        "src_file": 7973,
        "take": "A"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the category of the sound and create a caption with template `The sound of the {category}`.
-  **` tag  entry`** We use the categoryfor each entry in the dataset as a tag.
-  **` original data`** We save filename, fold, target, category, src_file and boolean value esc10 (whether the audio in esc10) of audio, the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).