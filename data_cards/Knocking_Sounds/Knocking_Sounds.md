# Knocking Sound Effects With Emotional Intentions Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|1.2M| 500|11.7 minutes|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [Knocking Sound Effects With Emotional Intentions Website](https://zenodo.org/record/3668503#.Y2duY3ZBxPZ)  |Download audio files from the website  <br>
## Preprocessing Principles

You may refer to [preprocess_knocking_sfx.py](/data_preprocess/preprocess_knocking_sfx.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "sound of knocking with sadness"
    ],
    "tag": [
        "sound of knocking",
        "sadness"
    ],
    "original_data": {
        "title": "Knocking Sound Effects With Emotional Intentions",
        "description": "The dataset was recorded by the professional foley artist Ulf Olausson at the FoleyWorks (http://foleyworks.se/) studios in Stockholm on the 15th October, 2019. Inspired by previous work on knocking sounds [1]. we chose five type of emotions to be portrayed in the dataset: anger, fear, happiness, neutral and sadness.",
        "license": "Creative Commons Attribution 4.0 International",
        "filename": "sadness_73.wav",
        "duration": 1.4817083333333334,
        "emotion": "sadness"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the emotional intention of the knocking sound and create a caption with template `sound of knocking with {emotion}`.
-  **` tag  entry`** We use the emotion intention as tag.
-  **` original data`** We save filename, emotional intentio and duration of audio, the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).