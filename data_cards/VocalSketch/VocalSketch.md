# VocalSketch Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|1.7 GB| 10700|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [VocalSketch GitHup repo](https://github.com/interactiveaudiolab/VocalSketchDataSet)  |Download audio files and meta data from the GitHub repo <br>
## Preprocessing Principles

You may refer to [preprocess_vocalsketch.py](/data_preprocess/preprocess_vocalsketch.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (vocal_imitations.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "playing a vocal imitation of seal"
    ],
    "tag": [
        "seal"
    ],
    "original_data": {
        "title": "VocalSketch Data Set 1.1.2",
        "description": "This dataset contains thousands of vocal imitations of a large set of diverse sounds. These imitations were collected from hundreds of contributors via Amazon's Mechanical Turk website.",
        "license": "",
        "filename": "seal - 4895922609717248.wav",
        "id": "4895922609717248",
        "stimulus_type": "sound recording",
        "duration": "1.492154",
        "included": true,
        "draft": false,
        "sound_label": "seal",
        "sound_label_id": "nan",
        "sound_recording": "seal_barking.wav",
        "recording_description": "seal"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the label for each vocal imitation and create a caption with template `playing a vocal imitation of {label}`.
-  **` tag  entry`** We use the label for each vocal imitation as a tag.
-  **` original data`** We save all the data from each row of vocal_imitations.csv for every audio as well as duration of the audio, dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).