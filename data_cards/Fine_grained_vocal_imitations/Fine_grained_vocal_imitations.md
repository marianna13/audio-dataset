# Fine-grained Vocal Imitation Set Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|129 MB| 547|0.9 hrs|
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
        "a dog growling"
    ],
    "tag": [
        "Animal",
        "Domestic animals, pets",
        "Dog"
    ],
    "original_data": {
        "title": "Fine-grained Vocal Imitation Set",
        "description": "This dataset includes 763 vocal imitations of 108 sound events. The sound event recordings were taken from a subset of Vocal Imitation Set.",
        "license": "Creative Commons Attribution 4.0 International",
        "category_d1": "Animal",
        "category_d2": "Domestic animals, pets",
        "category_d3": "Dog",
        "filename": "005Animal_Domestic animals_ pets_Dog_Growling-322.wav",
        "duration": 10,
        "participants_sound_recording_description": "a dog growling",
        "participants_sound_recording_description_confidence": "Very confident"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the `participants_sound_recording_description` as audio secription.
-  **` tag  entry`** We add categories (`category_d1`, `category_d2`, `category_d3`) to the list of tags.
-  **` original data`** We save categories, filename, duration, participants_sound_recording_description and participants_sound_recording_description_confidence for the audio.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).