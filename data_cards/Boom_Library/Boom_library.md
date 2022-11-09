# Boom Library Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|613 GB| 104|1.3 hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [Boom Library website](https://www.boomlibrary.com/)  |Download free audio files and meta data from the the Boom Library newsletter of free sounds (as zip archives).  <br>
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
        "the sound of squeak"
    ],
    "tag": [
        "Squeak"
    ],
    "original_data": {
        "title": "Audioset Strong",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "description": "Additional annotation on some of the AudioSet clips, this time using a procedure that instructed the annotators to mark every distinct sound event they perceived (complete annotation), and to indicate the start and end times of each event by dragging out a region on a spectrogram (\u201cstrong\u201d labeling).",
        "url": "https://www.youtube.com/watch?v=--4gqARaEJE",
        "label": "Squeak",
        "start": 5.622000000000001,
        "end": 6.693
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the label for each audio and create a caption with template `the sound of {label}`.
-  **` tag  entry`** We use the label for each vocal imitation as a tag.
-  **` original data`** We save all the data from each row of meta data for every audio as well as timestamps, dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).