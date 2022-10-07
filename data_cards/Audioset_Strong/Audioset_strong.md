# Audioset Strong Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|613 GB| 1652224|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [Audioset Strong website](https://research.google.com/audioset/download_strong.html)  |Download audio files and meta data from the the website (audioset_eval_strong.tsv, audioset_train_strong.tsv, mid_to_display_name.tsv). Concatenate train and eval sets and join them with mid_to_display_name.tsv to get label names. 2. For every row in the dataset download audio file from YouTube.  <br>
## Preprocessing Principles

You may refer to [preprocess_audioset_strong.py](/data_preprocess/preprocess_audioset_strong.py) for all the details. Here is a concise summary:

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