# BOOM Dataset Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|222 MB| 760|1.3hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [BOOM Library website website](https://www.boomlibrary.com/)  |Download audio files and meta data from the the website. 2. For every row in the dataset download audio file from YouTube.  <br>
## Preprocessing Principles

You may refer to [preprocess_boom_library.py](/data_preprocess/preprocess_boom_library.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (vocal_imitations.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "DSGNErie Heartbeat Jump Scare B00M Halloween21"
    ],
    "tag": [
        "Jump"
    ],
    "original_data": {
        "title": "Boom Library",
        "description": "Sound effects library",
        "description_audio": "DSGNErie Heartbeat Jump Scare B00M Halloween21",
        "filename": "DSGNErie_Heartbeat Jump Scare_B00M_Halloween21.wav"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We use `participants_sound_recording_description` as a text.
-  **` tag  entry`** We use `category_d1`, `category_d2` and  `category_d3` for each vocal imitation as tags.
-  **` original data`** We save all the data from each row of meta data for every audio as well as timestamps, dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).